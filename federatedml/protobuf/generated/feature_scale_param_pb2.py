# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: feature-scale-param.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='feature-scale-param.proto',
  package='com.webank.ai.fate.core.mlmodel.buffer',
  syntax='proto3',
  serialized_options=_b('B\017ScaleParamProto'),
  serialized_pb=_b('\n\x19\x66\x65\x61ture-scale-param.proto\x12&com.webank.ai.fate.core.mlmodel.buffer\"\xec\x01\n\nScaleParam\x12^\n\x0f\x63ol_scale_param\x18\x01 \x03(\x0b\x32\x45.com.webank.ai.fate.core.mlmodel.buffer.ScaleParam.ColScaleParamEntry\x12\x0e\n\x06header\x18\x02 \x03(\t\x1an\n\x12\x43olScaleParamEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12G\n\x05value\x18\x02 \x01(\x0b\x32\x38.com.webank.ai.fate.core.mlmodel.buffer.ColumnScaleParam:\x02\x38\x01\"Y\n\x10\x43olumnScaleParam\x12\x14\n\x0c\x63olumn_upper\x18\x03 \x01(\x01\x12\x14\n\x0c\x63olumn_lower\x18\x04 \x01(\x01\x12\x0c\n\x04mean\x18\x05 \x01(\x01\x12\x0b\n\x03std\x18\x06 \x01(\x01\x42\x11\x42\x0fScaleParamProtob\x06proto3')
)




_SCALEPARAM_COLSCALEPARAMENTRY = _descriptor.Descriptor(
  name='ColScaleParamEntry',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.ScaleParam.ColScaleParamEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='com.webank.ai.fate.core.mlmodel.buffer.ScaleParam.ColScaleParamEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='com.webank.ai.fate.core.mlmodel.buffer.ScaleParam.ColScaleParamEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=196,
  serialized_end=306,
)

_SCALEPARAM = _descriptor.Descriptor(
  name='ScaleParam',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.ScaleParam',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='col_scale_param', full_name='com.webank.ai.fate.core.mlmodel.buffer.ScaleParam.col_scale_param', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='header', full_name='com.webank.ai.fate.core.mlmodel.buffer.ScaleParam.header', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_SCALEPARAM_COLSCALEPARAMENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=70,
  serialized_end=306,
)


_COLUMNSCALEPARAM = _descriptor.Descriptor(
  name='ColumnScaleParam',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.ColumnScaleParam',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='column_upper', full_name='com.webank.ai.fate.core.mlmodel.buffer.ColumnScaleParam.column_upper', index=0,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='column_lower', full_name='com.webank.ai.fate.core.mlmodel.buffer.ColumnScaleParam.column_lower', index=1,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mean', full_name='com.webank.ai.fate.core.mlmodel.buffer.ColumnScaleParam.mean', index=2,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='std', full_name='com.webank.ai.fate.core.mlmodel.buffer.ColumnScaleParam.std', index=3,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=308,
  serialized_end=397,
)

_SCALEPARAM_COLSCALEPARAMENTRY.fields_by_name['value'].message_type = _COLUMNSCALEPARAM
_SCALEPARAM_COLSCALEPARAMENTRY.containing_type = _SCALEPARAM
_SCALEPARAM.fields_by_name['col_scale_param'].message_type = _SCALEPARAM_COLSCALEPARAMENTRY
DESCRIPTOR.message_types_by_name['ScaleParam'] = _SCALEPARAM
DESCRIPTOR.message_types_by_name['ColumnScaleParam'] = _COLUMNSCALEPARAM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ScaleParam = _reflection.GeneratedProtocolMessageType('ScaleParam', (_message.Message,), dict(

  ColScaleParamEntry = _reflection.GeneratedProtocolMessageType('ColScaleParamEntry', (_message.Message,), dict(
    DESCRIPTOR = _SCALEPARAM_COLSCALEPARAMENTRY,
    __module__ = 'feature_scale_param_pb2'
    # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.ScaleParam.ColScaleParamEntry)
    ))
  ,
  DESCRIPTOR = _SCALEPARAM,
  __module__ = 'feature_scale_param_pb2'
  # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.ScaleParam)
  ))
_sym_db.RegisterMessage(ScaleParam)
_sym_db.RegisterMessage(ScaleParam.ColScaleParamEntry)

ColumnScaleParam = _reflection.GeneratedProtocolMessageType('ColumnScaleParam', (_message.Message,), dict(
  DESCRIPTOR = _COLUMNSCALEPARAM,
  __module__ = 'feature_scale_param_pb2'
  # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.ColumnScaleParam)
  ))
_sym_db.RegisterMessage(ColumnScaleParam)


DESCRIPTOR._options = None
_SCALEPARAM_COLSCALEPARAMENTRY._options = None
# @@protoc_insertion_point(module_scope)
