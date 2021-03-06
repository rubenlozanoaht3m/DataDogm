# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hetero-kmeans-meta.proto

import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(name='hetero-kmeans-meta.proto', package='com.webank.ai.fate.core.mlmodel.buffer', syntax='proto3', serialized_options=_b('B\024KmeansModelMetaProto'), serialized_pb=_b(
    '\n\x18hetero-kmeans-meta.proto\x12&com.webank.ai.fate.core.mlmodel.buffer\";\n\x0fKmeansModelMeta\x12\t\n\x01k\x18\x01 \x01(\x03\x12\x0b\n\x03tol\x18\x02 \x01(\x01\x12\x10\n\x08max_iter\x18\x03 \x01(\x03\x42\x16\x42\x14KmeansModelMetaProtob\x06proto3'))


_KMEANSMODELMETA = _descriptor.Descriptor(
    name='KmeansModelMeta',
    full_name='com.webank.ai.fate.core.mlmodel.buffer.KmeansModelMeta',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='k', full_name='com.webank.ai.fate.core.mlmodel.buffer.KmeansModelMeta.k', index=0,
            number=1, type=3, cpp_type=2, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            serialized_options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='tol', full_name='com.webank.ai.fate.core.mlmodel.buffer.KmeansModelMeta.tol', index=1,
            number=2, type=1, cpp_type=5, label=1,
            has_default_value=False, default_value=float(0),
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            serialized_options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='max_iter', full_name='com.webank.ai.fate.core.mlmodel.buffer.KmeansModelMeta.max_iter', index=2,
            number=3, type=3, cpp_type=2, label=1,
            has_default_value=False, default_value=0,
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
    serialized_end=127,
)

DESCRIPTOR.message_types_by_name['KmeansModelMeta'] = _KMEANSMODELMETA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

KmeansModelMeta = _reflection.GeneratedProtocolMessageType('KmeansModelMeta', (_message.Message,), {
    'DESCRIPTOR': _KMEANSMODELMETA,
    '__module__': 'hetero_kmeans_meta_pb2'
    # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.KmeansModelMeta)
})
_sym_db.RegisterMessage(KmeansModelMeta)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
