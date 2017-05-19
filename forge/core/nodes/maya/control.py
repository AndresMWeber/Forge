import forge
from forge.core.nodes.maya.curve import MayaCurve
from forge.core.nodes.base.control import AbstractControl


@forge.register_node
class MayaControl(MayaCurve, AbstractControl):
    """
    class for building templates control
    """
    INTERNAL_TYPE = 'control'
    ENGINE_TYPE = 'group'
