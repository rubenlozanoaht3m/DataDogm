# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: boosting-tree-model-param.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='boosting-tree-model-param.proto',
  package='com.webank.ai.fate.core.mlmodel.buffer',
  syntax='proto3',
  serialized_options=_b('B\030BoostTreeModelParamProto'),
  serialized_pb=_b('\n\x1f\x62oosting-tree-model-param.proto\x12&com.webank.ai.fate.core.mlmodel.buffer\"\xa4\x01\n\tNodeParam\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x10\n\x08sitename\x18\x02 \x01(\t\x12\x0b\n\x03\x66id\x18\x03 \x01(\x05\x12\x0b\n\x03\x62id\x18\x04 \x01(\x01\x12\x0e\n\x06weight\x18\x05 \x01(\x01\x12\x0f\n\x07is_leaf\x18\x06 \x01(\x08\x12\x13\n\x0bleft_nodeid\x18\x07 \x01(\x05\x12\x14\n\x0cright_nodeid\x18\x08 \x01(\x05\x12\x13\n\x0bmissing_dir\x18\t \x01(\x05\"\xac\x03\n\x16\x44\x65\x63isionTreeModelParam\x12@\n\x05tree_\x18\x01 \x03(\x0b\x32\x31.com.webank.ai.fate.core.mlmodel.buffer.NodeParam\x12i\n\x0esplit_maskdict\x18\x02 \x03(\x0b\x32Q.com.webank.ai.fate.core.mlmodel.buffer.DecisionTreeModelParam.SplitMaskdictEntry\x12t\n\x14missing_dir_maskdict\x18\x03 \x03(\x0b\x32V.com.webank.ai.fate.core.mlmodel.buffer.DecisionTreeModelParam.MissingDirMaskdictEntry\x1a\x34\n\x12SplitMaskdictEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\x01:\x02\x38\x01\x1a\x39\n\x17MissingDirMaskdictEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\"\\\n\x15\x46\x65\x61tureImportanceInfo\x12\x10\n\x08sitename\x18\x01 \x01(\t\x12\x0b\n\x03\x66id\x18\x02 \x01(\x05\x12\x12\n\nimportance\x18\x03 \x01(\x01\x12\x10\n\x08\x66ullname\x18\x04 \x01(\t\"\xe4\x05\n\x16\x42oostingTreeModelParam\x12\x10\n\x08tree_num\x18\x01 \x01(\x05\x12N\n\x06trees_\x18\x02 \x03(\x0b\x32>.com.webank.ai.fate.core.mlmodel.buffer.DecisionTreeModelParam\x12\x12\n\ninit_score\x18\x03 \x03(\x01\x12\x0e\n\x06losses\x18\x04 \x03(\x01\x12\x10\n\x08tree_dim\x18\x05 \x01(\x05\x12\x13\n\x0bnum_classes\x18\x06 \x01(\x05\x12\x10\n\x08\x63lasses_\x18\x07 \x03(\t\x12Z\n\x13\x66\x65\x61ture_importances\x18\x08 \x03(\x0b\x32=.com.webank.ai.fate.core.mlmodel.buffer.FeatureImportanceInfo\x12{\n\x18\x66\x65\x61ture_name_fid_mapping\x18\t \x03(\x0b\x32Y.com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam.FeatureNameFidMappingEntry\x12\x16\n\x0e\x62\x65st_iteration\x18\n \x01(\x05\x12\x11\n\ttree_plan\x18\x0b \x03(\t\x12\x12\n\nmodel_name\x18\x0c \x01(\t\x12x\n\x16\x61nonymous_name_mapping\x18\r \x03(\x0b\x32X.com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam.AnonymousNameMappingEntry\x1a<\n\x1a\x46\x65\x61tureNameFidMappingEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a;\n\x19\x41nonymousNameMappingEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\x1a\x42\x18\x42oostTreeModelParamProtob\x06proto3')




_NODEPARAM = _descriptor.Descriptor(
  name='NodeParam',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.NodeParam',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='com.webank.ai.fate.core.mlmodel.buffer.NodeParam.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sitename', full_name='com.webank.ai.fate.core.mlmodel.buffer.NodeParam.sitename', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fid', full_name='com.webank.ai.fate.core.mlmodel.buffer.NodeParam.fid', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bid', full_name='com.webank.ai.fate.core.mlmodel.buffer.NodeParam.bid', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='weight', full_name='com.webank.ai.fate.core.mlmodel.buffer.NodeParam.weight', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_leaf', full_name='com.webank.ai.fate.core.mlmodel.buffer.NodeParam.is_leaf', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='left_nodeid', full_name='com.webank.ai.fate.core.mlmodel.buffer.NodeParam.left_nodeid', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='right_nodeid', full_name='com.webank.ai.fate.core.mlmodel.buffer.NodeParam.right_nodeid', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='missing_dir', full_name='com.webank.ai.fate.core.mlmodel.buffer.NodeParam.missing_dir', index=8,
      number=9, type=5, cpp_type=1, label=1,
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
  serialized_start=76,
  serialized_end=240,
)


_DECISIONTREEMODELPARAM_SPLITMASKDICTENTRY = _descriptor.Descriptor(
  name='SplitMaskdictEntry',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.DecisionTreeModelParam.SplitMaskdictEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='com.webank.ai.fate.core.mlmodel.buffer.DecisionTreeModelParam.SplitMaskdictEntry.key', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='com.webank.ai.fate.core.mlmodel.buffer.DecisionTreeModelParam.SplitMaskdictEntry.value', index=1,
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
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=560,
  serialized_end=612,
)

_DECISIONTREEMODELPARAM_MISSINGDIRMASKDICTENTRY = _descriptor.Descriptor(
  name='MissingDirMaskdictEntry',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.DecisionTreeModelParam.MissingDirMaskdictEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='com.webank.ai.fate.core.mlmodel.buffer.DecisionTreeModelParam.MissingDirMaskdictEntry.key', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='com.webank.ai.fate.core.mlmodel.buffer.DecisionTreeModelParam.MissingDirMaskdictEntry.value', index=1,
      number=2, type=5, cpp_type=1, label=1,
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
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=614,
  serialized_end=671,
)

_DECISIONTREEMODELPARAM = _descriptor.Descriptor(
  name='DecisionTreeModelParam',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.DecisionTreeModelParam',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='tree_', full_name='com.webank.ai.fate.core.mlmodel.buffer.DecisionTreeModelParam.tree_', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='split_maskdict', full_name='com.webank.ai.fate.core.mlmodel.buffer.DecisionTreeModelParam.split_maskdict', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='missing_dir_maskdict', full_name='com.webank.ai.fate.core.mlmodel.buffer.DecisionTreeModelParam.missing_dir_maskdict', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_DECISIONTREEMODELPARAM_SPLITMASKDICTENTRY, _DECISIONTREEMODELPARAM_MISSINGDIRMASKDICTENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=243,
  serialized_end=671,
)


_FEATUREIMPORTANCEINFO = _descriptor.Descriptor(
  name='FeatureImportanceInfo',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.FeatureImportanceInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sitename', full_name='com.webank.ai.fate.core.mlmodel.buffer.FeatureImportanceInfo.sitename', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fid', full_name='com.webank.ai.fate.core.mlmodel.buffer.FeatureImportanceInfo.fid', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='importance', full_name='com.webank.ai.fate.core.mlmodel.buffer.FeatureImportanceInfo.importance', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fullname', full_name='com.webank.ai.fate.core.mlmodel.buffer.FeatureImportanceInfo.fullname', index=3,
      number=4, type=9, cpp_type=9, label=1,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=673,
  serialized_end=765,
)


_BOOSTINGTREEMODELPARAM_FEATURENAMEFIDMAPPINGENTRY = _descriptor.Descriptor(
  name='FeatureNameFidMappingEntry',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam.FeatureNameFidMappingEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam.FeatureNameFidMappingEntry.key', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam.FeatureNameFidMappingEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1387,
  serialized_end=1447,


_BOOSTINGTREEMODELPARAM_ANONYMOUSNAMEMAPPINGENTRY = _descriptor.Descriptor(
  name='AnonymousNameMappingEntry',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam.AnonymousNameMappingEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam.AnonymousNameMappingEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam.AnonymousNameMappingEntry.value', index=1,
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
  serialized_start=1449,
  serialized_end=1508,
)

_BOOSTINGTREEMODELPARAM = _descriptor.Descriptor(
  name='BoostingTreeModelParam',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='tree_num', full_name='com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam.tree_num', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trees_', full_name='com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam.trees_', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='init_score', full_name='com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam.init_score', index=2,
      number=3, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='losses', full_name='com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam.losses', index=3,
      number=4, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tree_dim', full_name='com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam.tree_dim', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='num_classes', full_name='com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam.num_classes', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='classes_', full_name='com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam.classes_', index=6,
      number=7, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='feature_importances', full_name='com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam.feature_importances', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='feature_name_fid_mapping', full_name='com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam.feature_name_fid_mapping', index=8,
      number=9, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='best_iteration', full_name='com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam.best_iteration', index=9,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tree_plan', full_name='com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam.tree_plan', index=10,
      number=11, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='model_name', full_name='com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam.model_name', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='anonymous_name_mapping', full_name='com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam.anonymous_name_mapping', index=12,
      number=13, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='anonymous_name_mapping', full_name='com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam.anonymous_name_mapping', index=12,
      number=13, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_BOOSTINGTREEMODELPARAM_FEATURENAMEFIDMAPPINGENTRY, _BOOSTINGTREEMODELPARAM_ANONYMOUSNAMEMAPPINGENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=768,
  serialized_end=1508,
)

_DECISIONTREEMODELPARAM_SPLITMASKDICTENTRY.containing_type = _DECISIONTREEMODELPARAM
_DECISIONTREEMODELPARAM_MISSINGDIRMASKDICTENTRY.containing_type = _DECISIONTREEMODELPARAM
_DECISIONTREEMODELPARAM.fields_by_name['tree_'].message_type = _NODEPARAM
_DECISIONTREEMODELPARAM.fields_by_name['split_maskdict'].message_type = _DECISIONTREEMODELPARAM_SPLITMASKDICTENTRY
_DECISIONTREEMODELPARAM.fields_by_name['missing_dir_maskdict'].message_type = _DECISIONTREEMODELPARAM_MISSINGDIRMASKDICTENTRY
_BOOSTINGTREEMODELPARAM_FEATURENAMEFIDMAPPINGENTRY.containing_type = _BOOSTINGTREEMODELPARAM
_BOOSTINGTREEMODELPARAM_ANONYMOUSNAMEMAPPINGENTRY.containing_type = _BOOSTINGTREEMODELPARAM
_BOOSTINGTREEMODELPARAM.fields_by_name['trees_'].message_type = _DECISIONTREEMODELPARAM
_BOOSTINGTREEMODELPARAM.fields_by_name['feature_importances'].message_type = _FEATUREIMPORTANCEINFO
_BOOSTINGTREEMODELPARAM.fields_by_name['feature_name_fid_mapping'].message_type = _BOOSTINGTREEMODELPARAM_FEATURENAMEFIDMAPPINGENTRY
_BOOSTINGTREEMODELPARAM.fields_by_name['anonymous_name_mapping'].message_type = _BOOSTINGTREEMODELPARAM_ANONYMOUSNAMEMAPPINGENTRY
DESCRIPTOR.message_types_by_name['NodeParam'] = _NODEPARAM
DESCRIPTOR.message_types_by_name['DecisionTreeModelParam'] = _DECISIONTREEMODELPARAM
DESCRIPTOR.message_types_by_name['FeatureImportanceInfo'] = _FEATUREIMPORTANCEINFO
DESCRIPTOR.message_types_by_name['BoostingTreeModelParam'] = _BOOSTINGTREEMODELPARAM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

NodeParam = _reflection.GeneratedProtocolMessageType('NodeParam', (_message.Message,), {
  'DESCRIPTOR' : _NODEPARAM,
  '__module__' : 'boosting_tree_model_param_pb2'
  # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.NodeParam)
  })
_sym_db.RegisterMessage(NodeParam)

DecisionTreeModelParam = _reflection.GeneratedProtocolMessageType('DecisionTreeModelParam', (_message.Message,), {

  'SplitMaskdictEntry' : _reflection.GeneratedProtocolMessageType('SplitMaskdictEntry', (_message.Message,), {
    'DESCRIPTOR' : _DECISIONTREEMODELPARAM_SPLITMASKDICTENTRY,
    '__module__' : 'boosting_tree_model_param_pb2'
    # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.DecisionTreeModelParam.SplitMaskdictEntry)
    })
  ,

  'MissingDirMaskdictEntry' : _reflection.GeneratedProtocolMessageType('MissingDirMaskdictEntry', (_message.Message,), {
    'DESCRIPTOR' : _DECISIONTREEMODELPARAM_MISSINGDIRMASKDICTENTRY,
    '__module__' : 'boosting_tree_model_param_pb2'
    # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.DecisionTreeModelParam.MissingDirMaskdictEntry)
    })
  ,
  'DESCRIPTOR' : _DECISIONTREEMODELPARAM,
  '__module__' : 'boosting_tree_model_param_pb2'
  # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.DecisionTreeModelParam)
  })
_sym_db.RegisterMessage(DecisionTreeModelParam)
_sym_db.RegisterMessage(DecisionTreeModelParam.SplitMaskdictEntry)
_sym_db.RegisterMessage(DecisionTreeModelParam.MissingDirMaskdictEntry)

FeatureImportanceInfo = _reflection.GeneratedProtocolMessageType('FeatureImportanceInfo', (_message.Message,), {
  'DESCRIPTOR' : _FEATUREIMPORTANCEINFO,
  '__module__' : 'boosting_tree_model_param_pb2'
  # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.FeatureImportanceInfo)
  })
_sym_db.RegisterMessage(FeatureImportanceInfo)

BoostingTreeModelParam = _reflection.GeneratedProtocolMessageType('BoostingTreeModelParam', (_message.Message,), {

  'FeatureNameFidMappingEntry' : _reflection.GeneratedProtocolMessageType('FeatureNameFidMappingEntry', (_message.Message,), {
    'DESCRIPTOR' : _BOOSTINGTREEMODELPARAM_FEATURENAMEFIDMAPPINGENTRY,
    '__module__' : 'boosting_tree_model_param_pb2'
    # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam.FeatureNameFidMappingEntry)
    })
  ,

  'AnonymousNameMappingEntry' : _reflection.GeneratedProtocolMessageType('AnonymousNameMappingEntry', (_message.Message,), {
    'DESCRIPTOR' : _BOOSTINGTREEMODELPARAM_ANONYMOUSNAMEMAPPINGENTRY,
    '__module__' : 'boosting_tree_model_param_pb2'
    # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam.AnonymousNameMappingEntry)
    })
  ,
  'DESCRIPTOR' : _BOOSTINGTREEMODELPARAM,
  '__module__' : 'boosting_tree_model_param_pb2'
  # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.BoostingTreeModelParam)
  })
_sym_db.RegisterMessage(BoostingTreeModelParam)
_sym_db.RegisterMessage(BoostingTreeModelParam.FeatureNameFidMappingEntry)
_sym_db.RegisterMessage(BoostingTreeModelParam.AnonymousNameMappingEntry)


DESCRIPTOR._options = None
_DECISIONTREEMODELPARAM_SPLITMASKDICTENTRY._options = None
_DECISIONTREEMODELPARAM_MISSINGDIRMASKDICTENTRY._options = None
_BOOSTINGTREEMODELPARAM_FEATURENAMEFIDMAPPINGENTRY._options = None
_BOOSTINGTREEMODELPARAM_ANONYMOUSNAMEMAPPINGENTRY._options = None
# @@protoc_insertion_point(module_scope)
