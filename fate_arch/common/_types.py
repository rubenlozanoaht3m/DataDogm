from enum import IntEnum


class WorkMode(IntEnum):
    STANDALONE = 0
    CLUSTER = 1

    def is_standalone(self):
        return self.value == self.STANDALONE

    def is_cluster(self):
        return self.value == self.CLUSTER


class Backend(IntEnum):
    EGGROLL = 0
    SPARK = 1

    def is_spark(self):
        return self.value == self.SPARK

    def is_eggroll(self):
        return self.value == self.EGGROLL


class FederatedMode(object):
    SINGLE = "SINGLE"
    MULTIPLE = "MULTIPLE"

    def is_single(self, value):
        return value == self.SINGLE

    def is_multiple(self, value):
        return value == self.MULTIPLE


class FederatedComm(object):
    PUSH = "PUSH"
    PULL = "PULL"


class Party(object):
    """
    Uniquely identify
    """

    def __init__(self, role, party_id):
        self.role = str(role)
        self.party_id = str(party_id)

    def __hash__(self):
        return (self.role, self.party_id).__hash__()

    def __str__(self):
        return f"Party(role={self.role}, party_id={self.party_id})"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return (self.role, self.party_id) < (other.role, other.party_id)

    def __eq__(self, other):
        return self.party_id == other.party_id and self.role == other.role
