import threading
import typing
import uuid

from fate_arch.abc import CSessionABC, FederationABC
from fate_arch.common import Backend, WorkMode
from fate_arch.common.file_utils import load_json_conf
from fate_arch.computing import ComputingType
from fate_arch.federation import FederationType
from fate_arch.session._parties import PartiesInfo
from fate_arch.storage import StorageType


class Session(object):

    @staticmethod
    def create(backend: typing.Union[Backend, int] = Backend.EGGROLL,
               work_mode: typing.Union[WorkMode, int] = WorkMode.CLUSTER):
        if isinstance(work_mode, int):
            work_mode = WorkMode(work_mode)
        if isinstance(backend, int):
            backend = Backend(backend)

        if backend == Backend.EGGROLL:
            if work_mode == WorkMode.CLUSTER:
                return Session(ComputingType.EGGROLL, FederationType.EGGROLL, StorageType.EGGROLL)
            else:
                return Session(ComputingType.STANDALONE, FederationType.STANDALONE, StorageType.STANDALONE)
        if backend == Backend.SPARK:
            return Session(ComputingType.SPARK, FederationType.MQ, StorageType.HDFS)

    def __init__(self, computing_type: ComputingType,
                 federation_type: FederationType,
                 storage_type: StorageType):
        self._computing_type = computing_type
        self._federation_type = federation_type
        self._storage_type = storage_type
        self._computing_session: typing.Optional[CSessionABC] = None
        self._federation_session: typing.Optional[FederationABC] = None
        self._storage_session = None
        self._parties_info: typing.Optional[PartiesInfo] = None
        self._session_id = str(uuid.uuid1())

        # add to session environment
        _RuntimeSessionEnvironment.add_session(self)

    @property
    def session_id(self) -> str:
        return self._session_id

    def as_default(self):
        _RuntimeSessionEnvironment.as_default_opened(self)
        return self

    def _open(self):
        _RuntimeSessionEnvironment.open_non_default_session(self)
        return self

    def _close(self):
        _RuntimeSessionEnvironment.close_non_default_session(self)
        return self

    def __enter__(self):
        return self._open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._close()

    def init_computing(self,
                       computing_session_id: str,
                       **kwargs):
        if self.is_computing_valid:
            raise RuntimeError(f"computing session already valid")

        if self._computing_type == ComputingType.EGGROLL:
            from fate_arch.computing.eggroll import CSession
            work_mode = kwargs.get("work_mode", 1)
            options = kwargs.get("options", {})
            self._computing_session = CSession(session_id=computing_session_id,
                                               work_mode=work_mode,
                                               options=options)
            return self

        if self._computing_type == ComputingType.SPARK:
            from fate_arch.computing.spark import CSession
            self._computing_session = CSession(session_id=computing_session_id)
            self._computing_type = ComputingType.SPARK
            return self

        if self._computing_type == ComputingType.STANDALONE:
            from fate_arch.computing.standalone import CSession
            self._computing_session = CSession(session_id=computing_session_id)
            self._computing_type = ComputingType.STANDALONE
            return self

        raise RuntimeError(f"{self._computing_type} not supported")

    def init_federation(self,
                        federation_session_id: str,
                        *,
                        runtime_conf: typing.Optional[dict] = None,
                        parties_info: typing.Optional[PartiesInfo] = None,
                        server_conf: typing.Optional[dict] = None):

        if parties_info is None:
            if runtime_conf is None:
                raise RuntimeError(f"`party_info` and `runtime_conf` are both `None`")
            parties_info = PartiesInfo.from_conf(runtime_conf)
        self._parties_info = parties_info

        if server_conf is None:
            server_conf = load_json_conf("conf/server_conf.json")

        if self.is_federation_valid:
            raise RuntimeError("federation session already valid")

        if self._federation_type == FederationType.EGGROLL:
            from fate_arch.computing.eggroll import CSession
            from fate_arch.federation.eggroll import Federation
            from fate_arch.federation.eggroll import Proxy

            if not self.is_computing_valid or not isinstance(self._computing_session, CSession):
                raise RuntimeError(f"require computing with type {ComputingType.EGGROLL} valid")

            proxy = Proxy.from_conf(server_conf)
            self._federation_session = Federation(rp_ctx=self._computing_session.get_rpc(),
                                                  rs_session_id=federation_session_id,
                                                  party=parties_info.local_party,
                                                  proxy=proxy)
            return self

        if self._federation_type == FederationType.MQ:
            from fate_arch.computing.spark import CSession
            from fate_arch.federation.spark import Federation

            if not self.is_computing_valid or not isinstance(self._computing_session, CSession):
                raise RuntimeError(f"require computing with type {ComputingType.SPARK} valid")

            self._federation_session = Federation.from_conf(federation_session_id=federation_session_id,
                                                            party=parties_info.local_party,
                                                            runtime_conf=runtime_conf,
                                                            server_conf=server_conf)
            return self

        if self._federation_type == FederationType.STANDALONE:
            from fate_arch.computing.standalone import CSession
            from fate_arch.federation.standalone import Federation

            if not self.is_computing_valid or not isinstance(self._computing_session, CSession):
                raise RuntimeError(f"require computing with type {ComputingType.STANDALONE} valid")

            self._federation_session = \
                Federation(standalone_session=self._computing_session.get_standalone_session(),
                           federation_session_id=federation_session_id,
                           party=parties_info.local_party)
            return self

        raise RuntimeError(f"{self._federation_type} not supported")

    def init_storage(self, storage_type: StorageType = FederationType.EGGROLL):
        pass

    @property
    def computing(self) -> CSessionABC:
        return self._computing_session

    @property
    def federation(self) -> FederationABC:
        return self._federation_session

    @property
    def storage(self):
        return self._storage_session

    @property
    def parties(self):
        return self._parties_info

    @property
    def is_computing_valid(self):
        return self._computing_session is not None

    @property
    def is_federation_valid(self):
        return self._federation_session is not None

    @property
    def is_storage_valid(self):
        return self._storage_session is not None


class _RuntimeSessionEnvironment(object):
    __DEFAULT = None
    __SESSIONS = threading.local()

    @classmethod
    def add_session(cls, session: 'Session'):
        if not hasattr(cls.__SESSIONS, "CREATED"):
            cls.__SESSIONS.CREATED = {}
        cls.__SESSIONS.CREATED[session.session_id] = session

    @classmethod
    def has_non_default_session_opened(cls):
        if getattr(cls.__SESSIONS, 'OPENED_STACK', None) is not None and cls.__SESSIONS.OPENED_STACK:
            return True
        return False

    @classmethod
    def get_non_default_session(cls):
        return cls.__SESSIONS.OPENED_STACK[-1]

    @classmethod
    def open_non_default_session(cls, session):
        if not hasattr(cls.__SESSIONS, 'OPENED_STACK'):
            cls.__SESSIONS.OPENED_STACK = []
        cls.__SESSIONS.OPENED_STACK.append(session)

    @classmethod
    def close_non_default_session(cls, session: Session):
        if not hasattr(cls.__SESSIONS, 'OPENED_STACK') or len(cls.__SESSIONS.OPENED_STACK) == 0:
            raise RuntimeError(f"non_default_session stack empty, nothing to close")
        least: Session = cls.__SESSIONS.OPENED_STACK.pop()
        if least.session_id != session.session_id:
            raise RuntimeError(f"least opened session({least.session_id}) should be close first! "
                               f"while try to close {session.session_id}. all session: {cls.__SESSIONS.OPENED_STACK}")

    @classmethod
    def has_default_session_opened(cls):
        return cls.__DEFAULT is not None

    @classmethod
    def get_default_session(cls):
        return cls.__DEFAULT

    @classmethod
    def as_default_opened(cls, session):
        cls.__DEFAULT = session

    @classmethod
    def get_latest_opened(cls) -> Session:
        if not cls.has_non_default_session_opened():
            if not cls.has_default_session_opened():
                raise RuntimeError(f"no session opened")
            else:
                return cls.get_default_session()
        else:
            return cls.get_non_default_session()


def get_latest_opened():
    return _RuntimeSessionEnvironment.get_latest_opened()
