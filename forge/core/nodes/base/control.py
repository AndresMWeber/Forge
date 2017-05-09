import forge
from forge.core.channels import (VISIBILITY, SCALE)
from .transform import AbstractTransform


@forge.register_node
class AbstractControl(AbstractTransform):
    """
    class for building templates control
    """

    def __init__(self, maya_transform, control_offset_grp='', control_con_grp='', scale=1.0, rename=False, **kwargs):
        """
        Encapsulates a given transform with templates control functionality.
        :param maya_transform: str, transform for control
        :param control_offset_grp: str, transform for parent offset group
        :param control_con_grp: str, transform for child connection group
        :param scale: float, value for scale of control
        :param kwargs: dict, any possible extra naming kwargs for renaming this node as defined in env.yml in nomenclate
        """
        super(AbstractControl, self).__init__(maya_transform, type='control', **kwargs)

        self.group_offset = None
        self.group_connection = None

        if control_offset_grp:
            self.group_offset = AbstractTransform(control_offset_grp)

        if control_con_grp:
            self.group_connection = AbstractTransform(control_con_grp)

        if rename:
            self.rename(**kwargs)

    @classmethod
    def create(cls, name='untitled', shape='cube', scale=1.0, lock_channelbox=None, parent='', **kwargs):
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
        parent = AbstractTransform(parent)
        offset = forge.registry.group(em=True)
        control = forge.registry.control(shape)
        connection = forge.registry.group(em=True, parent=control)

        control.parent(offset)
        if parent.exists:
            offset.parent(parent)

        control_instance = cls(control,
                               control_offset_grp=offset,
                               control_con_grp=connection,
                               scale=scale,
                               rename=True,
                               **kwargs)
        control_instance.rename()

        lock_channelbox = [SCALE, VISIBILITY] if lock_channelbox is None else lock_channelbox
        flattened_channels = control_instance.flatten_compound_channels(control_instance.node, lock_channelbox)
        control_instance.lock_channels(control_instance.node, flattened_channels)

        return control_instance

    def rename(self, **kwargs):
        """
        Renames the Control transform, connection group and offset groups with the given nomenclate kwargs 
        :param kwargs: dict, any possible extra naming kwargs for renaming this node as defined in env.yml in nomenclate
        :return: None
        """
        super(AbstractControl, self).rename(**kwargs)
        kwargs.update(self.nom.state)
        if self.group_connection:
            kwargs['type'] = 'connection_group'
            self.group_connection.rename(**kwargs)
        if self.group_offset:
            kwargs['type'] = 'offset_group'
            self.group_offset.rename(**kwargs)

    def scale_shapes(self, scale_value):
        raise NotImplementedError

    def swap_shape(self, shape='cube', maintain_offset=True, add=False):
        raise NotImplementedError


    @classmethod
    def factory(cls,maya_transform='', control_offset_grp='', control_con_grp='', *args, **kwargs):
        if isinstance(maya_transform, dict):
            forge.LOG.info('detected serialzation, deserializing and instancing with args %s' % maya_transform)
            kwargs.update(maya_transform)
            return cls(*args, **kwargs)
        elif issubclass(type(maya_transform), cls):
            forge.LOG.info('Detected subclass of %s...using this' % cls.__name__)
            return maya_transform
        else:
            forge.LOG.info('We are going with %r' % maya_transform)
            return cls(maya_transform, *args, **kwargs)