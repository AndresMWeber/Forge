from six import class_types, integer_types, string_types, text_type, binary_type

BASE_TYPES = list(class_types) + list(integer_types) + list(string_types) + [text_type] + [binary_type]
SERIALIZABLE_TYPES = BASE_TYPES + [list]

MODEL_TYPE = 'model'
JOINT_TYPE = 'joint'
CONTROL_TYPE = 'control'
HIERARCHY_TYPE = 'hierarchy'
METADATA_TYPE = 'metadata'

MAYA = 'maya'
NUKE = 'nuke'
HOUDINI = 'houdini'

MODE = MAYA
DEFAULT_TAG_ATTR = 'forge'
