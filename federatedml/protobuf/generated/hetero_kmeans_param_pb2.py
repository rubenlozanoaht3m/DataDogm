# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hetero-kmeans-param.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='hetero-kmeans-param.proto',
  package='com.webank.ai.fate.core.mlmodel.buffer',
  syntax='proto3',
  serialized_options=_b('B\025KmeansModelParamProto'),
  serialized_pb=_b('\n\x19hetero-kmeans-param.proto\x12&com.webank.ai.fate.core.mlmodel.buffer\"\xf8\x01\n\x10KmeansModelParam\x12\x19\n\x11\x63ount_of_clusters\x18\x01 \x01(\x03\x12\x16\n\x0emax_interation\x18\x02 \x01(\x03\x12\x11\n\tconverged\x18\x03 \x01(\x08\x12M\n\x0e\x63luster_detail\x18\x04 \x03(\x0b\x32\x35.com.webank.ai.fate.core.mlmodel.buffer.Clusterdetail\x12O\n\x0f\x63\x65ntroid_detail\x18\x05 \x03(\x0b\x32\x36.com.webank.ai.fate.core.mlmodel.buffer.Centroiddetail\" \n\rClusterdetail\x12\x0f\n\x07\x63luster\x18\x01 \x03(\x01\"\"\n\x0e\x43\x65ntroiddetail\x12\x10\n\x08\x63\x65ntroid\x18\x01 \x03(\x01\x42\x17\x42\x15KmeansModelParamProtob\x06proto3')
)




_KMEANSMODELPARAM = _descriptor.Descriptor(
  name='KmeansModelParam',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.KmeansModelParam',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='count_of_clusters', full_name='com.webank.ai.fate.core.mlmodel.buffer.KmeansModelParam.count_of_clusters', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='max_interation', full_name='com.webank.ai.fate.core.mlmodel.buffer.KmeansModelParam.max_interation', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='converged', full_name='com.webank.ai.fate.core.mlmodel.buffer.KmeansModelParam.converged', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cluster_detail', full_name='com.webank.ai.fate.core.mlmodel.buffer.KmeansModelParam.cluster_detail', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='centroid_detail', full_name='com.webank.ai.fate.core.mlmodel.buffer.KmeansModelParam.centroid_detail', index=4,
      number=5, type=11, cpp_type=10, label=3,
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
  serialized_start=70,
  serialized_end=318,
)


_CLUSTERDETAIL = _descriptor.Descriptor(
  name='Clusterdetail',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.Clusterdetail',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster', full_name='com.webank.ai.fate.core.mlmodel.buffer.Clusterdetail.cluster', index=0,
      number=1, type=1, cpp_type=5, label=3,
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
  serialized_start=320,
  serialized_end=352,
)


_CENTROIDDETAIL = _descriptor.Descriptor(
  name='Centroiddetail',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.Centroiddetail',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='centroid', full_name='com.webank.ai.fate.core.mlmodel.buffer.Centroiddetail.centroid', index=0,
      number=1, type=1, cpp_type=5, label=3,
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
  serialized_start=354,
  serialized_end=388,
)

_KMEANSMODELPARAM.fields_by_name['cluster_detail'].message_type = _CLUSTERDETAIL
_KMEANSMODELPARAM.fields_by_name['centroid_detail'].message_type = _CENTROIDDETAIL
DESCRIPTOR.message_types_by_name['KmeansModelParam'] = _KMEANSMODELPARAM
DESCRIPTOR.message_types_by_name['Clusterdetail'] = _CLUSTERDETAIL
DESCRIPTOR.message_types_by_name['Centroiddetail'] = _CENTROIDDETAIL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

KmeansModelParam = _reflection.GeneratedProtocolMessageType('KmeansModelParam', (_message.Message,), {
  'DESCRIPTOR' : _KMEANSMODELPARAM,
  '__module__' : 'hetero_kmeans_param_pb2'
  # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.KmeansModelParam)
  })
_sym_db.RegisterMessage(KmeansModelParam)

Clusterdetail = _reflection.GeneratedProtocolMessageType('Clusterdetail', (_message.Message,), {
  'DESCRIPTOR' : _CLUSTERDETAIL,
  '__module__' : 'hetero_kmeans_param_pb2'
  # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.Clusterdetail)
  })
_sym_db.RegisterMessage(Clusterdetail)

Centroiddetail = _reflection.GeneratedProtocolMessageType('Centroiddetail', (_message.Message,), {
  'DESCRIPTOR' : _CENTROIDDETAIL,
  '__module__' : 'hetero_kmeans_param_pb2'
  # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.Centroiddetail)
  })
_sym_db.RegisterMessage(Centroiddetail)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
