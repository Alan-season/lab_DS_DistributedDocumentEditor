# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/group.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12protos/group.proto\" \n\x04User\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\x05\"\xf4\x01\n\x05Group\x12\x10\n\x08group_id\x18\x01 \x01(\x05\x12\x12\n\ngroup_name\x18\x02 \x01(\t\x12\x16\n\x07members\x18\x03 \x03(\x0b\x32\x05.User\x12$\n\x07version\x18\x04 \x03(\x0b\x32\x13.Group.VersionEntry\x12&\n\x08\x64ocument\x18\x05 \x03(\x0b\x32\x14.Group.DocumentEntry\x1a.\n\x0cVersionEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a/\n\rDocumentEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.group_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GROUP_VERSIONENTRY._options = None
  _GROUP_VERSIONENTRY._serialized_options = b'8\001'
  _GROUP_DOCUMENTENTRY._options = None
  _GROUP_DOCUMENTENTRY._serialized_options = b'8\001'
  _USER._serialized_start=22
  _USER._serialized_end=54
  _GROUP._serialized_start=57
  _GROUP._serialized_end=301
  _GROUP_VERSIONENTRY._serialized_start=206
  _GROUP_VERSIONENTRY._serialized_end=252
  _GROUP_DOCUMENTENTRY._serialized_start=254
  _GROUP_DOCUMENTENTRY._serialized_end=301
# @@protoc_insertion_point(module_scope)