# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: label-transform-param.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='label-transform-param.proto',
  package='com.webank.ai.fate.core.mlmodel.buffer',
  syntax='proto3',
  serialized_options=_b('B\030LabelTransformParamProto'),
  serialized_pb=_b('\n\x1blabel-transform-param.proto\x12&com.webank.ai.fate.core.mlmodel.buffer\"\xfa\x03\n\x13LabelTransformParam\x12\x64\n\rlabel_encoder\x18\x01 \x03(\x0b\x32M.com.webank.ai.fate.core.mlmodel.buffer.LabelTransformParam.LabelEncoderEntry\x12i\n\x10\x65ncoder_key_type\x18\x02 \x03(\x0b\x32O.com.webank.ai.fate.core.mlmodel.buffer.LabelTransformParam.EncoderKeyTypeEntry\x12m\n\x12\x65ncoder_value_type\x18\x03 \x03(\x0b\x32Q.com.webank.ai.fate.core.mlmodel.buffer.LabelTransformParam.EncoderValueTypeEntry\x1a\x33\n\x11LabelEncoderEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\x35\n\x13\x45ncoderKeyTypeEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\x37\n\x15\x45ncoderValueTypeEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\x1a\x42\x18LabelTransformParamProtob\x06proto3')
)




_LABELTRANSFORMPARAM_LABELENCODERENTRY = _descriptor.Descriptor(
  name='LabelEncoderEntry',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.LabelTransformParam.LabelEncoderEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='com.webank.ai.fate.core.mlmodel.buffer.LabelTransformParam.LabelEncoderEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='com.webank.ai.fate.core.mlmodel.buffer.LabelTransformParam.LabelEncoderEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=415,
  serialized_end=466,
)

_LABELTRANSFORMPARAM_ENCODERKEYTYPEENTRY = _descriptor.Descriptor(
  name='EncoderKeyTypeEntry',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.LabelTransformParam.EncoderKeyTypeEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='com.webank.ai.fate.core.mlmodel.buffer.LabelTransformParam.EncoderKeyTypeEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='com.webank.ai.fate.core.mlmodel.buffer.LabelTransformParam.EncoderKeyTypeEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=468,
  serialized_end=521,
)

_LABELTRANSFORMPARAM_ENCODERVALUETYPEENTRY = _descriptor.Descriptor(
  name='EncoderValueTypeEntry',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.LabelTransformParam.EncoderValueTypeEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='com.webank.ai.fate.core.mlmodel.buffer.LabelTransformParam.EncoderValueTypeEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='com.webank.ai.fate.core.mlmodel.buffer.LabelTransformParam.EncoderValueTypeEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=523,
  serialized_end=578,
)

_LABELTRANSFORMPARAM = _descriptor.Descriptor(
  name='LabelTransformParam',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.LabelTransformParam',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='label_encoder', full_name='com.webank.ai.fate.core.mlmodel.buffer.LabelTransformParam.label_encoder', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='encoder_key_type', full_name='com.webank.ai.fate.core.mlmodel.buffer.LabelTransformParam.encoder_key_type', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='encoder_value_type', full_name='com.webank.ai.fate.core.mlmodel.buffer.LabelTransformParam.encoder_value_type', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_LABELTRANSFORMPARAM_LABELENCODERENTRY, _LABELTRANSFORMPARAM_ENCODERKEYTYPEENTRY, _LABELTRANSFORMPARAM_ENCODERVALUETYPEENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=72,
  serialized_end=578,
)

_LABELTRANSFORMPARAM_LABELENCODERENTRY.containing_type = _LABELTRANSFORMPARAM
_LABELTRANSFORMPARAM_ENCODERKEYTYPEENTRY.containing_type = _LABELTRANSFORMPARAM
_LABELTRANSFORMPARAM_ENCODERVALUETYPEENTRY.containing_type = _LABELTRANSFORMPARAM
_LABELTRANSFORMPARAM.fields_by_name['label_encoder'].message_type = _LABELTRANSFORMPARAM_LABELENCODERENTRY
_LABELTRANSFORMPARAM.fields_by_name['encoder_key_type'].message_type = _LABELTRANSFORMPARAM_ENCODERKEYTYPEENTRY
_LABELTRANSFORMPARAM.fields_by_name['encoder_value_type'].message_type = _LABELTRANSFORMPARAM_ENCODERVALUETYPEENTRY
DESCRIPTOR.message_types_by_name['LabelTransformParam'] = _LABELTRANSFORMPARAM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LabelTransformParam = _reflection.GeneratedProtocolMessageType('LabelTransformParam', (_message.Message,), {

  'LabelEncoderEntry' : _reflection.GeneratedProtocolMessageType('LabelEncoderEntry', (_message.Message,), {
    'DESCRIPTOR' : _LABELTRANSFORMPARAM_LABELENCODERENTRY,
    '__module__' : 'label_transform_param_pb2'
    # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.LabelTransformParam.LabelEncoderEntry)
    })
  ,

  'EncoderKeyTypeEntry' : _reflection.GeneratedProtocolMessageType('EncoderKeyTypeEntry', (_message.Message,), {
    'DESCRIPTOR' : _LABELTRANSFORMPARAM_ENCODERKEYTYPEENTRY,
    '__module__' : 'label_transform_param_pb2'
    # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.LabelTransformParam.EncoderKeyTypeEntry)
    })
  ,

  'EncoderValueTypeEntry' : _reflection.GeneratedProtocolMessageType('EncoderValueTypeEntry', (_message.Message,), {
    'DESCRIPTOR' : _LABELTRANSFORMPARAM_ENCODERVALUETYPEENTRY,
    '__module__' : 'label_transform_param_pb2'
    # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.LabelTransformParam.EncoderValueTypeEntry)
    })
  ,
  'DESCRIPTOR' : _LABELTRANSFORMPARAM,
  '__module__' : 'label_transform_param_pb2'
  # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.LabelTransformParam)
  })
_sym_db.RegisterMessage(LabelTransformParam)
_sym_db.RegisterMessage(LabelTransformParam.LabelEncoderEntry)
_sym_db.RegisterMessage(LabelTransformParam.EncoderKeyTypeEntry)
_sym_db.RegisterMessage(LabelTransformParam.EncoderValueTypeEntry)


DESCRIPTOR._options = None
_LABELTRANSFORMPARAM_LABELENCODERENTRY._options = None
_LABELTRANSFORMPARAM_ENCODERKEYTYPEENTRY._options = None
_LABELTRANSFORMPARAM_ENCODERVALUETYPEENTRY._options = None
# @@protoc_insertion_point(module_scope)
