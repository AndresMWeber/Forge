import forge
import transform


@forge.register_node
class AbstractCurve(transform.AbstractTransform):
    """
        Base Class for manipulating transforms of a given node.
    """
    TYPE = 'curve'

    def __init__(self, node_dag='', *args, **kwargs):
        super(AbstractCurve, self).__init__(node_dag=node_dag, *args, **kwargs)
