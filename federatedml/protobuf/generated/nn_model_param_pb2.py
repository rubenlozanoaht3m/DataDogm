# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nn-model-param.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='nn-model-param.proto',
  package='com.webank.ai.fate.core.mlmodel.buffer',
  syntax='proto3',
  serialized_options=_b('B\021NNModelParamProto'),
  serialized_pb=_b('\n\x14nn-model-param.proto\x12&com.webank.ai.fate.core.mlmodel.buffer\"}\n\x0cNNModelParam\x12\x16\n\x0e\x61ggregate_iter\x18\x01 \x01(\x05\x12\x19\n\x11saved_model_bytes\x18\x02 \x01(\x0c\x12\x14\n\x0closs_history\x18\x03 \x03(\x01\x12\x14\n\x0cis_converged\x18\x04 \x01(\x08\x12\x0e\n\x06header\x18\x05 \x03(\tB\x13\x42\x11NNModelParamProtob\x06proto3')
)




_NNMODELPARAM = _descriptor.Descriptor(
  name='NNModelParam',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.NNModelParam',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='aggregate_iter', full_name='com.webank.ai.fate.core.mlmodel.buffer.NNModelParam.aggregate_iter', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='saved_model_bytes', full_name='com.webank.ai.fate.core.mlmodel.buffer.NNModelParam.saved_model_bytes', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='loss_history', full_name='com.webank.ai.fate.core.mlmodel.buffer.NNModelParam.loss_history', index=2,
      number=3, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_converged', full_name='com.webank.ai.fate.core.mlmodel.buffer.NNModelParam.is_converged', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='header', full_name='com.webank.ai.fate.core.mlmodel.buffer.NNModelParam.header', index=4,
      number=5, type=9, cpp_type=9, label=3,
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
  serialized_start=64,
  serialized_end=189,
)

DESCRIPTOR.message_types_by_name['NNModelParam'] = _NNMODELPARAM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

NNModelParam = _reflection.GeneratedProtocolMessageType('NNModelParam', (_message.Message,), dict(
  DESCRIPTOR = _NNMODELPARAM,
  __module__ = 'nn_model_param_pb2'
  # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.NNModelParam)
  ))
_sym_db.RegisterMessage(NNModelParam)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
