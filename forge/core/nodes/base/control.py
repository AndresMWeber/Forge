import forge
from .curve import AbstractCurve
from forge.core.channels import (VISIBILITY, LEVEL_PRIMARY, SCALE)
import inspect


@forge.register_node
class AbstractControl(AbstractCurve):
    """
    class for building templates control
    """
    INTERNAL_TYPE = 'control'

    def __init__(self, node_dag='', control_offset_grp='', control_con_grp='', scale=1.0, rename=False, **kwargs):
        """
        Encapsulates a given transform with templates control functionality.
        :param maya_transform: str, transform for control
        :param control_offset_grp: str, transform for parent offset group
        :param control_con_grp: str, transform for child connection group
        :param scale: float, value for scale of control
        :param kwargs: dict, any possible extra naming kwargs for renaming this node as defined in env.yml in nomenclate
        """
        self.LOG.info('Initializing <%s> with node_dag=%r, control_offset_grp=%r, control_con_grp=%r, kwargs=%s' % (
            self.__class__.__name__, node_dag, control_offset_grp, control_con_grp, kwargs))

        super(AbstractControl, self).__init__(node_dag=node_dag, **kwargs)

        self.group_offset = None
        self.group_connection = None
        self.scale = float(scale)  # Ensuring we cast back to float in case it was serialized

        if control_offset_grp:
            self.group_offset = forge.registry.Transform.factory(control_offset_grp)
            self.group_offset.INTERNAL_TYPE = 'offset_group'

        if control_con_grp:
            self.group_connection = forge.registry.Transform.factory(control_con_grp)
            self.group_connection.INTERNAL_TYPE = 'connection_group'

        if rename:
            self.rename(**kwargs)

        if scale != 1.0:
            self.scale_shapes(scale)

    @classmethod
    def create(cls, shape='cube', scale=1.0, lock_channelbox=None, parent='', **kwargs):
        """
        Creates a Control object with given name
        :param name: str, starting main name of the control
        :param shape: str, given shape from list in rig_lib.core.nodes.maya_utils.factory.MayaControlShapeFactory
        :param scale: float, scale of control to create
        :param lock_channelbox: list(str), list of attributes to lock and hide
        :param parent: str, possible parent transform for the control
        :param kwargs: dict, any possible extra naming kwargs for renaming this node as defined in env.yml in nomenclate
        :return: Control
        """
        cls.LOG.info('Creating <%s> with shape=%s, parent=%r, kwargs=%s' % (cls.__name__, shape, parent, kwargs))
        control = super(AbstractControl, cls).create()
        offset = forge.registry.Transform.create()
        connection = forge.registry.Transform.create()

        control.parent(offset)
        connection.parent(control)
        offset.parent(parent)

        control_instance = cls(node_dag=control.node,
                               control_offset_grp=offset,
                               control_con_grp=connection,
                               scale=scale,
                               **kwargs)

        control_instance.rename(**kwargs)
        control_instance.set_color(level=kwargs.get('level', LEVEL_PRIMARY))
        control_instance.swap_shape(shape=shape)

        lock_channelbox = [SCALE, VISIBILITY] if lock_channelbox is None else lock_channelbox
        flattened_channels = control_instance.flatten_compound_channels(control_instance.node, lock_channelbox)
        control_instance.lock_channels(flattened_channels)
        control_instance.scale_shapes(scale)

        cls.LOG.info('Created <%s>: %s' % (cls.__name__, control_instance))
        return control_instance

    def rename(self, **kwargs):
        """
        Renames the Control transform, connection group and offset groups with the given nomenclate kwargs 
        :param kwargs: dict, any possible extra naming kwargs for renaming this node as defined in env.yml in nomenclate
        :return: None
        """
        self.LOG.debug('Renaming this control with kwargs %s' % kwargs)
        super(AbstractControl, self).rename(**kwargs)

        if self.group_connection:
            self.group_connection.rename(**self.nom.state)

        if self.group_offset:
            self.group_offset.rename(**self.nom.state)

    def get_parent(self, level=0):
        if self.group_offset:
            return self.group_offset.get_parent()
        else:
            return super(AbstractControl, self).get_parent()

    def parent(self, target_parent, use_offset_group=True, **kwargs):
        target_parent = target_parent.group_connection if isinstance(target_parent, self.__class__) else target_parent

        if use_offset_group and self.group_offset:
            self.group_offset.parent(target_parent=target_parent)
            self.LOG.debug('Parenting control offset group to %r' % target_parent)
        else:
            super(AbstractControl, self).parent(target_parent=target_parent)
            self.LOG.debug('Parenting control transform to %r' % target_parent)

    def serialize(self):
        return {self.__class__.__name__: {
            'node_dag': self.node,
            'control_offset_grp': self.group_offset.serialize(),
            'control_con_grp': self.group_connection.serialize(),
            'scale': self.scale}}

    def setup_hierarchy(self, parent=None):
        """ Sets up a hierarchical pattern for instance between its constituent nodes.

        :param parent: str, forge.core.nodes.maya.MayaNode, either a subclass of MayaNode or a string to a maya dag.
        :return: None
        """
        self.parent(self.group_offset, use_offset_group=False)
        self.group_connection.parent(self)
        self.parent(parent)

    def __repr__(self):
        nodes = [self.node]
        if self.group_connection is not None:
            nodes.append(self.group_connection.name_short)
        if self.group_offset:
            nodes.insert(0, self.group_offset.name_short)
        return '|'.join(nodes)
