# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: feature-scale-meta.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='feature-scale-meta.proto',
  package='com.webank.ai.fate.core.mlmodel.buffer',
  syntax='proto3',
  serialized_options=b'B\016ScaleMetaProto',
  serialized_pb=b'\n\x18\x66\x65\x61ture-scale-meta.proto\x12&com.webank.ai.fate.core.mlmodel.buffer\"\xac\x01\n\tScaleMeta\x12\x0e\n\x06method\x18\x01 \x01(\t\x12\x0c\n\x04mode\x18\x02 \x01(\t\x12\x0c\n\x04\x61rea\x18\x03 \x01(\t\x12\x14\n\x0cscale_column\x18\x04 \x03(\t\x12\x12\n\nfeat_upper\x18\x05 \x03(\t\x12\x12\n\nfeat_lower\x18\x06 \x03(\t\x12\x11\n\twith_mean\x18\x07 \x01(\x08\x12\x10\n\x08with_std\x18\x08 \x01(\x08\x12\x10\n\x08need_run\x18\t \x01(\x08\x42\x10\x42\x0eScaleMetaProtob\x06proto3'
)




_SCALEMETA = _descriptor.Descriptor(
  name='ScaleMeta',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.ScaleMeta',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='method', full_name='com.webank.ai.fate.core.mlmodel.buffer.ScaleMeta.method', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mode', full_name='com.webank.ai.fate.core.mlmodel.buffer.ScaleMeta.mode', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='area', full_name='com.webank.ai.fate.core.mlmodel.buffer.ScaleMeta.area', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='scale_column', full_name='com.webank.ai.fate.core.mlmodel.buffer.ScaleMeta.scale_column', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='feat_upper', full_name='com.webank.ai.fate.core.mlmodel.buffer.ScaleMeta.feat_upper', index=4,
      number=5, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='feat_lower', full_name='com.webank.ai.fate.core.mlmodel.buffer.ScaleMeta.feat_lower', index=5,
      number=6, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='with_mean', full_name='com.webank.ai.fate.core.mlmodel.buffer.ScaleMeta.with_mean', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='with_std', full_name='com.webank.ai.fate.core.mlmodel.buffer.ScaleMeta.with_std', index=7,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='need_run', full_name='com.webank.ai.fate.core.mlmodel.buffer.ScaleMeta.need_run', index=8,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=69,
  serialized_end=241,
)

DESCRIPTOR.message_types_by_name['ScaleMeta'] = _SCALEMETA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ScaleMeta = _reflection.GeneratedProtocolMessageType('ScaleMeta', (_message.Message,), {
  'DESCRIPTOR' : _SCALEMETA,
  '__module__' : 'feature_scale_meta_pb2'
  # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.ScaleMeta)
  })
_sym_db.RegisterMessage(ScaleMeta)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
