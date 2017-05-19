import forge
import forge.core.channels as channels
import forge.exception as exception
import node


@forge.register_node
class AbstractTransform(node.AbstractNode):
    """
        Base Class for manipulating transforms of a given node.
    """
    INTERNAL_TYPE = 'group'

    def __init__(self, node_dag='', *args, **kwargs):
        super(AbstractTransform, self).__init__(node_dag=node_dag, **kwargs)

    @property
    def r_ws(self):
        return self.rotation(q=True)

    @property
    def r(self):
        return self.rotation(world_space=False, q=True)

    @property
    def t_ws(self):
        return self.position(q=True)

    @property
    def t(self):
        return self.position(world_space=False, q=True)

    def translate_to_obj(self, target):
        raise NotImplementedError

    def rotate_to_obj(self, target):
        raise NotImplementedError

    def move_to_obj(self, target):
        raise NotImplementedError

    def transform(self, move_style, ref_xform):
        try:
            self.validate_node(ref_xform)
            if move_style == channels.MOVE.MATCH:
                self.move_to_obj(ref_xform)
            if move_style == channels.MOVE.POSITION:
                self.translate_to_obj(ref_xform)
            if move_style == channels.MOVE.ROTATION:
                self.rotate_to_obj(ref_xform)

        except exception.ValidationError:
            forge.LOG.error("Invalid move type specified.")
            raise

    def rotation(self, t=(0.0, 0.0, 0.0), world_space=True, q=True):
        raise NotImplementedError

    def position(self, t=(0.0, 0.0, 0.0), world_space=True, q=True):
        raise NotImplementedError
