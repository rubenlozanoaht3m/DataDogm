# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: lr-model-param.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='lr-model-param.proto',
  package='com.webank.ai.fate.core.mlmodel.buffer',
  syntax='proto3',
  serialized_options=_b('B\021LRModelParamProto'),
  serialized_pb=_b('\n\x14lr-model-param.proto\x12&com.webank.ai.fate.core.mlmodel.buffer\"\xdc\x02\n\x0cLRModelParam\x12\r\n\x05iters\x18\x01 \x01(\x05\x12\x14\n\x0closs_history\x18\x02 \x03(\x01\x12\x14\n\x0cis_converged\x18\x03 \x01(\x08\x12P\n\x06weight\x18\x04 \x03(\x0b\x32@.com.webank.ai.fate.core.mlmodel.buffer.LRModelParam.WeightEntry\x12\x11\n\tintercept\x18\x05 \x01(\x01\x12\x0e\n\x06header\x18\x06 \x03(\t\x12S\n\x12one_vs_rest_result\x18\x07 \x01(\x0b\x32\x37.com.webank.ai.fate.core.mlmodel.buffer.OneVsRestResult\x12\x18\n\x10need_one_vs_rest\x18\x08 \x01(\x08\x1a-\n\x0bWeightEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x01:\x02\x38\x01\"\xeb\x01\n\x0bSingleModel\x12\r\n\x05iters\x18\x01 \x01(\x05\x12\x14\n\x0closs_history\x18\x02 \x03(\x01\x12\x14\n\x0cis_converged\x18\x03 \x01(\x08\x12O\n\x06weight\x18\x04 \x03(\x0b\x32?.com.webank.ai.fate.core.mlmodel.buffer.SingleModel.WeightEntry\x12\x11\n\tintercept\x18\x05 \x01(\x01\x12\x0e\n\x06header\x18\x06 \x03(\t\x1a-\n\x0bWeightEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x01:\x02\x38\x01\"}\n\x0fOneVsRestResult\x12M\n\x10\x63ompleted_models\x18\x01 \x03(\x0b\x32\x33.com.webank.ai.fate.core.mlmodel.buffer.SingleModel\x12\x1b\n\x13one_vs_rest_classes\x18\x02 \x03(\tB\x13\x42\x11LRModelParamProtob\x06proto3')
)




_LRMODELPARAM_WEIGHTENTRY = _descriptor.Descriptor(
  name='WeightEntry',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.LRModelParam.WeightEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='com.webank.ai.fate.core.mlmodel.buffer.LRModelParam.WeightEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='com.webank.ai.fate.core.mlmodel.buffer.LRModelParam.WeightEntry.value', index=1,
      number=2, type=1, cpp_type=5, label=1,
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
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=368,
  serialized_end=413,
)

_LRMODELPARAM = _descriptor.Descriptor(
  name='LRModelParam',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.LRModelParam',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iters', full_name='com.webank.ai.fate.core.mlmodel.buffer.LRModelParam.iters', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='loss_history', full_name='com.webank.ai.fate.core.mlmodel.buffer.LRModelParam.loss_history', index=1,
      number=2, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_converged', full_name='com.webank.ai.fate.core.mlmodel.buffer.LRModelParam.is_converged', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='weight', full_name='com.webank.ai.fate.core.mlmodel.buffer.LRModelParam.weight', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='intercept', full_name='com.webank.ai.fate.core.mlmodel.buffer.LRModelParam.intercept', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='header', full_name='com.webank.ai.fate.core.mlmodel.buffer.LRModelParam.header', index=5,
      number=6, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='one_vs_rest_result', full_name='com.webank.ai.fate.core.mlmodel.buffer.LRModelParam.one_vs_rest_result', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='need_one_vs_rest', full_name='com.webank.ai.fate.core.mlmodel.buffer.LRModelParam.need_one_vs_rest', index=7,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_LRMODELPARAM_WEIGHTENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=65,
  serialized_end=413,
)


_SINGLEMODEL_WEIGHTENTRY = _descriptor.Descriptor(
  name='WeightEntry',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.SingleModel.WeightEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='com.webank.ai.fate.core.mlmodel.buffer.SingleModel.WeightEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='com.webank.ai.fate.core.mlmodel.buffer.SingleModel.WeightEntry.value', index=1,
      number=2, type=1, cpp_type=5, label=1,
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
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=368,
  serialized_end=413,
)

_SINGLEMODEL = _descriptor.Descriptor(
  name='SingleModel',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.SingleModel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iters', full_name='com.webank.ai.fate.core.mlmodel.buffer.SingleModel.iters', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='loss_history', full_name='com.webank.ai.fate.core.mlmodel.buffer.SingleModel.loss_history', index=1,
      number=2, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_converged', full_name='com.webank.ai.fate.core.mlmodel.buffer.SingleModel.is_converged', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='weight', full_name='com.webank.ai.fate.core.mlmodel.buffer.SingleModel.weight', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='intercept', full_name='com.webank.ai.fate.core.mlmodel.buffer.SingleModel.intercept', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='header', full_name='com.webank.ai.fate.core.mlmodel.buffer.SingleModel.header', index=5,
      number=6, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_SINGLEMODEL_WEIGHTENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=416,
  serialized_end=651,
)


_ONEVSRESTRESULT = _descriptor.Descriptor(
  name='OneVsRestResult',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.OneVsRestResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='completed_models', full_name='com.webank.ai.fate.core.mlmodel.buffer.OneVsRestResult.completed_models', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='one_vs_rest_classes', full_name='com.webank.ai.fate.core.mlmodel.buffer.OneVsRestResult.one_vs_rest_classes', index=1,
      number=2, type=9, cpp_type=9, label=3,
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
  serialized_start=653,
  serialized_end=778,
)

_LRMODELPARAM_WEIGHTENTRY.containing_type = _LRMODELPARAM
_LRMODELPARAM.fields_by_name['weight'].message_type = _LRMODELPARAM_WEIGHTENTRY
_LRMODELPARAM.fields_by_name['one_vs_rest_result'].message_type = _ONEVSRESTRESULT
_SINGLEMODEL_WEIGHTENTRY.containing_type = _SINGLEMODEL
_SINGLEMODEL.fields_by_name['weight'].message_type = _SINGLEMODEL_WEIGHTENTRY
_ONEVSRESTRESULT.fields_by_name['completed_models'].message_type = _SINGLEMODEL
DESCRIPTOR.message_types_by_name['LRModelParam'] = _LRMODELPARAM
DESCRIPTOR.message_types_by_name['SingleModel'] = _SINGLEMODEL
DESCRIPTOR.message_types_by_name['OneVsRestResult'] = _ONEVSRESTRESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LRModelParam = _reflection.GeneratedProtocolMessageType('LRModelParam', (_message.Message,), dict(

  WeightEntry = _reflection.GeneratedProtocolMessageType('WeightEntry', (_message.Message,), dict(
    DESCRIPTOR = _LRMODELPARAM_WEIGHTENTRY,
    __module__ = 'lr_model_param_pb2'
    # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.LRModelParam.WeightEntry)
    ))
  ,
  DESCRIPTOR = _LRMODELPARAM,
  __module__ = 'lr_model_param_pb2'
  # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.LRModelParam)
  ))
_sym_db.RegisterMessage(LRModelParam)
_sym_db.RegisterMessage(LRModelParam.WeightEntry)

SingleModel = _reflection.GeneratedProtocolMessageType('SingleModel', (_message.Message,), dict(

  WeightEntry = _reflection.GeneratedProtocolMessageType('WeightEntry', (_message.Message,), dict(
    DESCRIPTOR = _SINGLEMODEL_WEIGHTENTRY,
    __module__ = 'lr_model_param_pb2'
    # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.SingleModel.WeightEntry)
    ))
  ,
  DESCRIPTOR = _SINGLEMODEL,
  __module__ = 'lr_model_param_pb2'
  # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.SingleModel)
  ))
_sym_db.RegisterMessage(SingleModel)
_sym_db.RegisterMessage(SingleModel.WeightEntry)

OneVsRestResult = _reflection.GeneratedProtocolMessageType('OneVsRestResult', (_message.Message,), dict(
  DESCRIPTOR = _ONEVSRESTRESULT,
  __module__ = 'lr_model_param_pb2'
  # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.OneVsRestResult)
  ))
_sym_db.RegisterMessage(OneVsRestResult)


DESCRIPTOR._options = None
_LRMODELPARAM_WEIGHTENTRY._options = None
_SINGLEMODEL_WEIGHTENTRY._options = None
# @@protoc_insertion_point(module_scope)
