# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pearson-model-meta.proto

import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name='pearson-model-meta.proto',
    package='com.webank.ai.fate.core.mlmodel.buffer',
    syntax='proto3',
    serialized_options=_b('B\025PearsonModelMetaProto'),
    serialized_pb=_b('\n\x18pearson-model-meta.proto\x12&com.webank.ai.fate.core.mlmodel.buffer\"\"\n\x10PearsonModelMeta\x12\x0e\n\x06shapes\x18\x01 \x03(\x05\x42\x17\x42\x15PearsonModelMetaProtob\x06proto3')
)


_PEARSONMODELMETA = _descriptor.Descriptor(
    name='PearsonModelMeta',
    full_name='com.webank.ai.fate.core.mlmodel.buffer.PearsonModelMeta',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='shapes', full_name='com.webank.ai.fate.core.mlmodel.buffer.PearsonModelMeta.shapes', index=0,
            number=1, type=5, cpp_type=1, label=3,
            has_default_value=False, default_value=[],
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            serialized_options=None, file=DESCRIPTOR),
    ],
    extensions=[
    ],
    nested_types=[],
    enum_types=[
    ],
    serialized_options=None,
    is_extendable=False,
    syntax='proto3',
    extension_ranges=[],
    oneofs=[
    ],
    serialized_start=68,
    serialized_end=102,
)

DESCRIPTOR.message_types_by_name['PearsonModelMeta'] = _PEARSONMODELMETA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PearsonModelMeta = _reflection.GeneratedProtocolMessageType('PearsonModelMeta', (_message.Message,), dict(
    DESCRIPTOR=_PEARSONMODELMETA,
    __module__='pearson_model_meta_pb2'
    # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.PearsonModelMeta)
))
_sym_db.RegisterMessage(PearsonModelMeta)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
