# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: poisson-model-param.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import sshe_cipher_param_pb2 as sshe__cipher__param__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='poisson-model-param.proto',
  package='com.webank.ai.fate.core.mlmodel.buffer',
  syntax='proto3',
  serialized_options=_b('B\026PoissonModelParamProto'),
  serialized_pb=_b('\n\x19poisson-model-param.proto\x12&com.webank.ai.fate.core.mlmodel.buffer\x1a\x17sshe-cipher-param.proto\"\xa5\x04\n\x11PoissonModelParam\x12\r\n\x05iters\x18\x01 \x01(\x05\x12\x14\n\x0closs_history\x18\x02 \x03(\x01\x12\x14\n\x0cis_converged\x18\x03 \x01(\x08\x12U\n\x06weight\x18\x04 \x03(\x0b\x32\x45.com.webank.ai.fate.core.mlmodel.buffer.PoissonModelParam.WeightEntry\x12\x11\n\tintercept\x18\x05 \x01(\x01\x12\x0e\n\x06header\x18\x06 \x03(\t\x12\x16\n\x0e\x62\x65st_iteration\x18\x07 \x01(\x05\x12h\n\x10\x65ncrypted_weight\x18\x08 \x03(\x0b\x32N.com.webank.ai.fate.core.mlmodel.buffer.PoissonModelParam.EncryptedWeightEntry\x12>\n\x06\x63ipher\x18\t \x01(\x0b\x32..com.webank.ai.fate.core.mlmodel.buffer.Cipher\x1a-\n\x0bWeightEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x01:\x02\x38\x01\x1aj\n\x14\x45ncryptedWeightEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x41\n\x05value\x18\x02 \x01(\x0b\x32\x32.com.webank.ai.fate.core.mlmodel.buffer.CipherText:\x02\x38\x01\x42\x18\x42\x16PoissonModelParamProtob\x06proto3')
  ,
  dependencies=[sshe__cipher__param__pb2.DESCRIPTOR,])




_POISSONMODELPARAM_WEIGHTENTRY = _descriptor.Descriptor(
  name='WeightEntry',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.PoissonModelParam.WeightEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='com.webank.ai.fate.core.mlmodel.buffer.PoissonModelParam.WeightEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='com.webank.ai.fate.core.mlmodel.buffer.PoissonModelParam.WeightEntry.value', index=1,
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
  serialized_start=491,
  serialized_end=536,
)

_POISSONMODELPARAM_ENCRYPTEDWEIGHTENTRY = _descriptor.Descriptor(
  name='EncryptedWeightEntry',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.PoissonModelParam.EncryptedWeightEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='com.webank.ai.fate.core.mlmodel.buffer.PoissonModelParam.EncryptedWeightEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='com.webank.ai.fate.core.mlmodel.buffer.PoissonModelParam.EncryptedWeightEntry.value', index=1,
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
  serialized_start=538,
  serialized_end=644,
)

_POISSONMODELPARAM = _descriptor.Descriptor(
  name='PoissonModelParam',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.PoissonModelParam',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iters', full_name='com.webank.ai.fate.core.mlmodel.buffer.PoissonModelParam.iters', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='loss_history', full_name='com.webank.ai.fate.core.mlmodel.buffer.PoissonModelParam.loss_history', index=1,
      number=2, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_converged', full_name='com.webank.ai.fate.core.mlmodel.buffer.PoissonModelParam.is_converged', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='weight', full_name='com.webank.ai.fate.core.mlmodel.buffer.PoissonModelParam.weight', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='intercept', full_name='com.webank.ai.fate.core.mlmodel.buffer.PoissonModelParam.intercept', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='header', full_name='com.webank.ai.fate.core.mlmodel.buffer.PoissonModelParam.header', index=5,
      number=6, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='best_iteration', full_name='com.webank.ai.fate.core.mlmodel.buffer.PoissonModelParam.best_iteration', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='encrypted_weight', full_name='com.webank.ai.fate.core.mlmodel.buffer.PoissonModelParam.encrypted_weight', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cipher', full_name='com.webank.ai.fate.core.mlmodel.buffer.PoissonModelParam.cipher', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_POISSONMODELPARAM_WEIGHTENTRY, _POISSONMODELPARAM_ENCRYPTEDWEIGHTENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=95,
  serialized_end=644,
)

_POISSONMODELPARAM_WEIGHTENTRY.containing_type = _POISSONMODELPARAM
_POISSONMODELPARAM_ENCRYPTEDWEIGHTENTRY.fields_by_name['value'].message_type = sshe__cipher__param__pb2._CIPHERTEXT
_POISSONMODELPARAM_ENCRYPTEDWEIGHTENTRY.containing_type = _POISSONMODELPARAM
_POISSONMODELPARAM.fields_by_name['weight'].message_type = _POISSONMODELPARAM_WEIGHTENTRY
_POISSONMODELPARAM.fields_by_name['encrypted_weight'].message_type = _POISSONMODELPARAM_ENCRYPTEDWEIGHTENTRY
_POISSONMODELPARAM.fields_by_name['cipher'].message_type = sshe__cipher__param__pb2._CIPHER
DESCRIPTOR.message_types_by_name['PoissonModelParam'] = _POISSONMODELPARAM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PoissonModelParam = _reflection.GeneratedProtocolMessageType('PoissonModelParam', (_message.Message,), {

  'WeightEntry' : _reflection.GeneratedProtocolMessageType('WeightEntry', (_message.Message,), {
    'DESCRIPTOR' : _POISSONMODELPARAM_WEIGHTENTRY,
    '__module__' : 'poisson_model_param_pb2'
    # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.PoissonModelParam.WeightEntry)
    })
  ,

  'EncryptedWeightEntry' : _reflection.GeneratedProtocolMessageType('EncryptedWeightEntry', (_message.Message,), {
    'DESCRIPTOR' : _POISSONMODELPARAM_ENCRYPTEDWEIGHTENTRY,
    '__module__' : 'poisson_model_param_pb2'
    # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.PoissonModelParam.EncryptedWeightEntry)
    })
  ,
  'DESCRIPTOR' : _POISSONMODELPARAM,
  '__module__' : 'poisson_model_param_pb2'
  # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.PoissonModelParam)
  })
_sym_db.RegisterMessage(PoissonModelParam)
_sym_db.RegisterMessage(PoissonModelParam.WeightEntry)
_sym_db.RegisterMessage(PoissonModelParam.EncryptedWeightEntry)


DESCRIPTOR._options = None
_POISSONMODELPARAM_WEIGHTENTRY._options = None
_POISSONMODELPARAM_ENCRYPTEDWEIGHTENTRY._options = None
# @@protoc_insertion_point(module_scope)
