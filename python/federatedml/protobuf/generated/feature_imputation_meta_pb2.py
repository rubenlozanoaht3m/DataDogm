# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: feature-imputation-meta.proto

import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name='feature-imputation-meta.proto',
    package='com.webank.ai.fate.core.mlmodel.buffer',
    syntax='proto3',
    serialized_options=_b('B\032FeatureImputationMetaProto'),
    serialized_pb=_b('\n\x1d\x66\x65\x61ture-imputation-meta.proto\x12&com.webank.ai.fate.core.mlmodel.buffer\"\x87\x02\n\x12\x46\x65\x61tureImputerMeta\x12\x12\n\nis_imputer\x18\x01 \x01(\x08\x12\x10\n\x08strategy\x18\x02 \x01(\t\x12\x15\n\rmissing_value\x18\x03 \x03(\t\x12\x1a\n\x12missing_value_type\x18\x04 \x03(\t\x12\x63\n\rcols_strategy\x18\x05 \x03(\x0b\x32L.com.webank.ai.fate.core.mlmodel.buffer.FeatureImputerMeta.ColsStrategyEntry\x1a\x33\n\x11\x43olsStrategyEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"{\n\x15\x46\x65\x61tureImputationMeta\x12P\n\x0cimputer_meta\x18\x01 \x01(\x0b\x32:.com.webank.ai.fate.core.mlmodel.buffer.FeatureImputerMeta\x12\x10\n\x08need_run\x18\x02 \x01(\x08\x42\x1c\x42\x1a\x46\x65\x61tureImputationMetaProtob\x06proto3')
)


_FEATUREIMPUTERMETA_COLSSTRATEGYENTRY = _descriptor.Descriptor(
    name='ColsStrategyEntry',
    full_name='com.webank.ai.fate.core.mlmodel.buffer.FeatureImputerMeta.ColsStrategyEntry',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='key',
            full_name='com.webank.ai.fate.core.mlmodel.buffer.FeatureImputerMeta.ColsStrategyEntry.key',
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode('utf-8'),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='value',
            full_name='com.webank.ai.fate.core.mlmodel.buffer.FeatureImputerMeta.ColsStrategyEntry.value',
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode('utf-8'),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=_b('8\001'),
    is_extendable=False,
    syntax='proto3',
    extension_ranges=[],
    oneofs=[],
    serialized_start=286,
    serialized_end=337,
)

_FEATUREIMPUTERMETA = _descriptor.Descriptor(
    name='FeatureImputerMeta',
    full_name='com.webank.ai.fate.core.mlmodel.buffer.FeatureImputerMeta',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='is_imputer', full_name='com.webank.ai.fate.core.mlmodel.buffer.FeatureImputerMeta.is_imputer', index=0,
            number=1, type=8, cpp_type=7, label=1,
            has_default_value=False, default_value=False,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            serialized_options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='strategy', full_name='com.webank.ai.fate.core.mlmodel.buffer.FeatureImputerMeta.strategy', index=1,
            number=2, type=9, cpp_type=9, label=1,
            has_default_value=False, default_value=_b("").decode('utf-8'),
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            serialized_options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='missing_value', full_name='com.webank.ai.fate.core.mlmodel.buffer.FeatureImputerMeta.missing_value', index=2,
            number=3, type=9, cpp_type=9, label=3,
            has_default_value=False, default_value=[],
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            serialized_options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='missing_value_type', full_name='com.webank.ai.fate.core.mlmodel.buffer.FeatureImputerMeta.missing_value_type', index=3,
            number=4, type=9, cpp_type=9, label=3,
            has_default_value=False, default_value=[],
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            serialized_options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='cols_strategy', full_name='com.webank.ai.fate.core.mlmodel.buffer.FeatureImputerMeta.cols_strategy', index=4,
            number=5, type=11, cpp_type=10, label=3,
            has_default_value=False, default_value=[],
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            serialized_options=None, file=DESCRIPTOR),
    ],
    extensions=[
    ],
    nested_types=[_FEATUREIMPUTERMETA_COLSSTRATEGYENTRY, ],
    enum_types=[
    ],
    serialized_options=None,
    is_extendable=False,
    syntax='proto3',
    extension_ranges=[],
    oneofs=[
    ],
    serialized_start=74,
    serialized_end=337,
)


_FEATUREIMPUTATIONMETA = _descriptor.Descriptor(
    name='FeatureImputationMeta',
    full_name='com.webank.ai.fate.core.mlmodel.buffer.FeatureImputationMeta',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='imputer_meta',
            full_name='com.webank.ai.fate.core.mlmodel.buffer.FeatureImputationMeta.imputer_meta',
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='need_run',
            full_name='com.webank.ai.fate.core.mlmodel.buffer.FeatureImputationMeta.need_run',
            index=1,
            number=2,
            type=8,
            cpp_type=7,
            label=1,
            has_default_value=False,
            default_value=False,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax='proto3',
    extension_ranges=[],
    oneofs=[],
    serialized_start=339,
    serialized_end=462,
)

_FEATUREIMPUTERMETA_COLSSTRATEGYENTRY.containing_type = _FEATUREIMPUTERMETA
_FEATUREIMPUTERMETA.fields_by_name['cols_strategy'].message_type = _FEATUREIMPUTERMETA_COLSSTRATEGYENTRY
_FEATUREIMPUTATIONMETA.fields_by_name['imputer_meta'].message_type = _FEATUREIMPUTERMETA
DESCRIPTOR.message_types_by_name['FeatureImputerMeta'] = _FEATUREIMPUTERMETA
DESCRIPTOR.message_types_by_name['FeatureImputationMeta'] = _FEATUREIMPUTATIONMETA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FeatureImputerMeta = _reflection.GeneratedProtocolMessageType('FeatureImputerMeta', (_message.Message,), {

    'ColsStrategyEntry': _reflection.GeneratedProtocolMessageType('ColsStrategyEntry', (_message.Message,), {
        'DESCRIPTOR': _FEATUREIMPUTERMETA_COLSSTRATEGYENTRY,
        '__module__': 'feature_imputation_meta_pb2'
        # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.FeatureImputerMeta.ColsStrategyEntry)
    }),
    'DESCRIPTOR': _FEATUREIMPUTERMETA,
    '__module__': 'feature_imputation_meta_pb2'
    # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.FeatureImputerMeta)
})
_sym_db.RegisterMessage(FeatureImputerMeta)
_sym_db.RegisterMessage(FeatureImputerMeta.ColsStrategyEntry)

FeatureImputationMeta = _reflection.GeneratedProtocolMessageType('FeatureImputationMeta', (_message.Message,), {
    'DESCRIPTOR': _FEATUREIMPUTATIONMETA,
    '__module__': 'feature_imputation_meta_pb2'
    # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.FeatureImputationMeta)
})
_sym_db.RegisterMessage(FeatureImputationMeta)


DESCRIPTOR._options = None
_FEATUREIMPUTERMETA_COLSSTRATEGYENTRY._options = None
# @@protoc_insertion_point(module_scope)
