from __future__ import annotations
import yaml._yaml
import typing
from yaml.events import AliasEvent
from yaml.tokens import AliasToken
from yaml.tokens import AnchorToken
from yaml.tokens import BlockEndToken
from yaml.tokens import BlockEntryToken
from yaml.tokens import BlockMappingStartToken
from yaml.tokens import BlockSequenceStartToken
from yaml.composer import ComposerError
from yaml.constructor import ConstructorError
from yaml.tokens import DirectiveToken
from yaml.events import DocumentEndEvent
from yaml.tokens import DocumentEndToken
from yaml.events import DocumentStartEvent
from yaml.tokens import DocumentStartToken
from yaml.emitter import EmitterError
from yaml.tokens import FlowEntryToken
from yaml.tokens import FlowMappingEndToken
from yaml.tokens import FlowMappingStartToken
from yaml.tokens import FlowSequenceEndToken
from yaml.tokens import FlowSequenceStartToken
from yaml.tokens import KeyToken
from yaml.events import MappingEndEvent
from yaml.nodes import MappingNode
from yaml.events import MappingStartEvent
from yaml.parser import ParserError
from yaml.reader import ReaderError
from yaml.representer import RepresenterError
from yaml.events import ScalarEvent
from yaml.nodes import ScalarNode
from yaml.tokens import ScalarToken
from yaml.scanner import ScannerError
from yaml.events import SequenceEndEvent
from yaml.nodes import SequenceNode
from yaml.events import SequenceStartEvent
from yaml.serializer import SerializerError
from yaml.events import StreamEndEvent
from yaml.tokens import StreamEndToken
from yaml.events import StreamStartEvent
from yaml.tokens import StreamStartToken
from yaml.tokens import TagToken
from yaml.tokens import ValueToken
from yaml.error import YAMLError
import _cython_3_0_11
import yaml

__all__ = [
    "AliasEvent",
    "AliasToken",
    "AnchorToken",
    "BlockEndToken",
    "BlockEntryToken",
    "BlockMappingStartToken",
    "BlockSequenceStartToken",
    "CEmitter",
    "CParser",
    "ComposerError",
    "ConstructorError",
    "DirectiveToken",
    "DocumentEndEvent",
    "DocumentEndToken",
    "DocumentStartEvent",
    "DocumentStartToken",
    "EmitterError",
    "FlowEntryToken",
    "FlowMappingEndToken",
    "FlowMappingStartToken",
    "FlowSequenceEndToken",
    "FlowSequenceStartToken",
    "KeyToken",
    "MappingEndEvent",
    "MappingNode",
    "MappingStartEvent",
    "Mark",
    "ParserError",
    "ReaderError",
    "RepresenterError",
    "ScalarEvent",
    "ScalarNode",
    "ScalarToken",
    "ScannerError",
    "SequenceEndEvent",
    "SequenceNode",
    "SequenceStartEvent",
    "SerializerError",
    "StreamEndEvent",
    "StreamEndToken",
    "StreamStartEvent",
    "StreamStartToken",
    "TagToken",
    "ValueToken",
    "YAMLError",
    "get_version",
    "get_version_string",
    "yaml"
]


class CEmitter():
    __pyx_vtable__: typing.Any  # PyCapsule()
    pass
class CParser():
    __pyx_vtable__: typing.Any  # PyCapsule()
    pass
class Mark():
    buffer: getset_descriptor # value = <attribute 'buffer' of 'yaml._yaml.Mark' objects>
    column: getset_descriptor # value = <attribute 'column' of 'yaml._yaml.Mark' objects>
    index: getset_descriptor # value = <attribute 'index' of 'yaml._yaml.Mark' objects>
    line: getset_descriptor # value = <attribute 'line' of 'yaml._yaml.Mark' objects>
    name: getset_descriptor # value = <attribute 'name' of 'yaml._yaml.Mark' objects>
    pointer: getset_descriptor # value = <attribute 'pointer' of 'yaml._yaml.Mark' objects>
    pass
__pyx_unpickle_Mark: _cython_3_0_11.cython_function_or_method # value = <cyfunction __pyx_unpickle_Mark>
__reduce_cython__: _cython_3_0_11.cython_function_or_method # value = <cyfunction CEmitter.__reduce_cython__>
__setstate_cython__: _cython_3_0_11.cython_function_or_method # value = <cyfunction CEmitter.__setstate_cython__>
__test__ = {}
get_version: _cython_3_0_11.cython_function_or_method # value = <cyfunction get_version>
get_version_string: _cython_3_0_11.cython_function_or_method # value = <cyfunction get_version_string>
yaml = yaml
