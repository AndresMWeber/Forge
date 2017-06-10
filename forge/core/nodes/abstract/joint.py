import forge
import transform


@forge.register_node
class AbstractJoint(transform.AbstractTransform):
    """
    class for building templates control
    """
    INTERNAL_TYPE = 'joint'
    NAME_DEFAULTS = {'name': 'untitled', 'var': 'A'}

    def __init__(self, node_dag='', *args, **kwargs):
        super(AbstractJoint, self).__init__(node_dag=node_dag, *args, **kwargs)

    @staticmethod
    def create_engine_instance(*args, **kwargs):
        return forge.registry.joint(*args, **kwargs)
