from six import class_types, integer_types, string_types, text_type, binary_type
from vendor.cgLogging.cgLogging import (
    getLogger,
    DEBUG,
    INFO,
    CRITICAL,
    WARNING,
    ERROR,
    FATAL
)

PACKAGE_LOGGER_LEVEL = CRITICAL

CRITICAL = CRITICAL
INFO = INFO
DEBUG = DEBUG
WARNING = WARNING
ERROR = ERROR
FATAL = FATAL


def get_module_logger(module_name, module_override_level=None):
    module_logger_level = module_override_level or PACKAGE_LOGGER_LEVEL
    return getLogger(module_name, level=module_logger_level, shell=False)


BASE_TYPES = list(class_types) + list(integer_types) + list(string_types) + [text_type] + [binary_type]
SERIALIZABLE_TYPES = BASE_TYPES + [list]

MODEL_TYPE = 'model'
JOINT_TYPE = 'joint'
CONTROL_TYPE = 'control'
HIERARCHY_TYPE = 'hierarchy'
METADATA_TYPE = 'metadata'

BASE = 'abstract'
MAYA = 'maya'
NUKE = 'nuke'
HOUDINI = 'houdini'

MODE = MAYA
DEFAULT_TAG_ATTR = 'metaforge'
