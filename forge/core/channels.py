
# Attributes
SCALE = 'scale'
ROTATE = 'rotate'
TRANSLATE = 'translate'
VISIBILITY = 'visibility'

OVERRIDE_RGB_COLOR = 'overrideColorRGB'
OVERRIDE_RGB = 'overrideRGBColors'
OVERRIDE_ENABLED = 'overrideEnabled'

LEVEL_PRIMARY = 'primary'
LEVEL_SECONDARY = 'secondary'
LEVEL_TERTIARY = 'tertiary'

WORLD_SPACE = 'world'
OBJECT_SPACE = 'object'
TRANSFORM_SPACE = 'transform'

COORDINATE_AXES = ['X', 'Y', 'Z']

ROTATE_ORDERS = ['xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx']

LEVEL_LOOKUP = {
    0: LEVEL_PRIMARY,
    1: LEVEL_SECONDARY,
    2: LEVEL_TERTIARY,
}


# Attribute Types
class TYPES:
    DOUBLE3 = 'double3'
    STRING = 'string'


class DIRECTIONS:
    LEFT = 'left'
    RIGHT = 'right'
    CENTER = 'center'
    NA = ''


class LEVEL:
    PRIMARY = LEVEL_LOOKUP[0]
    SECONDARY = LEVEL_LOOKUP[1]
    TERTIARY = LEVEL_LOOKUP[2]


class INT_SPACES:
    WORLD_SPACE = 0
    OBJECT_SPACE = 1
    TRANSFORM_SPACE = 2


class STR_SPACES:
    WORLD_SPACE = WORLD_SPACE
    OBJECT_SPACE = OBJECT_SPACE
    TRANSFORM_SPACE = TRANSFORM_SPACE


class MOVE:
    MATCH = 'match'
    POSITION = 'position'
    ROTATION = 'rotation'
