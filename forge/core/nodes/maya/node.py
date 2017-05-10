import maya.api.OpenMaya as oM
import maya.cmds as mc
import simplejson
from forge.core import colors
from forge.core.nodes.base.node import AbstractNode

import forge
from forge.core import channels
from forge.exception import exception, ValidationError
from forge.settings import DEFAULT_TAG_ATTR

utils = forge.registry.utils


@forge.register_node
class MayaNode(AbstractNode):
    """
         Wraps a dag_path with generic functions to manipulate a maya_utils node
    """

    def __init__(self, node_dag='', rename=False, parent='', **kwargs):
        super(MayaNode, self).__init__(node_dag, **kwargs)
        self._dag_path = self.get_dag_node(node_dag)

        if rename:
            self.rename(**kwargs)

        if forge.registry.utils.scene.exists(parent):
            self.parent(parent)

    @staticmethod
    def create_engine_instance(*args, **kwargs):
        node = forge.registry.group(em=True, *args, **kwargs)
        return node

    @staticmethod
    def validate_node(node_name):
        if not node_name:
            raise ValidationError('Blank input provided %r' % str(node_name), None)

        if not mc.objExists(str(node_name)):
            raise ValidationError('Node does not exist %r' % str(node_name), None)

    @property
    def shapes(self):
        return mc.listRelatives(self.node, c=True, s=True)

    @property
    def name_long(self):
        return str(self._dag_path.fullPathName())

    def get_shapes(self, types=None):
        kwargs = {'shapes': True, 'children': True, 'fullPath': True}
        if types:
            kwargs['type'] = types
        return mc.listRelatives(self.node, **kwargs)

    def lock_channels(self, channels_to_lock):
        for attr in self.flatten_compound_channels(self.node, channels_to_lock):
            utils.attr.set_attr(self.get_attr_dag(attr), lock=True, keyable=False)

    def set_attr(self, attr, value, **kwargs):
        value = simplejson.dumps(value) if isinstance(value, dict) else value
        attr_dag = self.get_attr_dag(attr)

        if isinstance(value, (list, tuple)):
            utils.attr.set_attr(attr_dag, *value, **kwargs)
        elif isinstance(value, str):
            utils.attr.set_attr(attr_dag, value, type='string')
        else:
            utils.attr.set_attr(attr_dag, value, **kwargs)

        return self.get_attr(attr)

    def get_attr(self, attr):
        value = utils.attr.set_attr(self.get_attr_dag(attr))
        try:
            return simplejson.loads(value)
        except (ValueError, TypeError):
            return value

    def add_attr(self, attr, value, **kwargs):
        try:
            utils.attr.add_attr(self.node, ln=attr, **kwargs)
        except RuntimeError:
            pass
        self.set_attr(attr, value)

    @exception(forge.LOG)
    def parent(self, target_parent, **kwargs):
        forge.LOG.debug('Parenting a node %r to parent %r' % (self.node, target_parent))
        try:
            mc.parent(self.node, MayaNode.factory(target_parent).node, **kwargs)
            return self.node
        except (RuntimeError, forge.exception.ValidationError):
            forge.LOG.debug('Parenting unsuccessful')

    def unparent(self):
        mc.parent(self.node, world=True)
        return self.node

    def get_parent(self, level=1):
        parent = self.node
        for _ in range(level):
            parents = mc.listRelatives(parent, p=True, f=True)
            if parents:
                parent = parents[0]
            else:
                break

        if parent != self.node:
            return self.factory(parent)
        else:
            return None

    def get_children(self, type='transform'):
        children = mc.listRelatives(self.node, c=True, type=type, fullPath=True) or []
        return [self.factory(child) for child in children]

    def set_color(self, nomenclate_object=None, level=channels.LEVEL_PRIMARY):
        if nomenclate_object is None:
            nomenclate_object = self.nom
        mc.setAttr(self.get_attr_dag(channels.OVERRIDE_ENABLED), 1)
        mc.setAttr(self.get_attr_dag(channels.OVERRIDE_RGB), 1)
        mc.setAttr(self.get_attr_dag(channels.OVERRIDE_RGB_COLOR),
                   *colors.color_lookup.get(str(nomenclate_object.side.label)).get(level))

    @staticmethod
    def flatten_compound_channels(xform, compound_channels):
        flattened_channels = []

        for lock_channel in compound_channels:
            if mc.attributeQuery(lock_channel, node=xform, attributeType=True) == channels.TYPES.DOUBLE3:
                for axis in channels.COORDINATE_AXES:
                    flattened_channels.append(lock_channel + axis)
            else:
                flattened_channels.append(lock_channel)
        return flattened_channels

    @staticmethod
    def get_dag_node(maya_transform):
        selection_list = oM.MSelectionList()
        selection_list.add(maya_transform)
        return selection_list.getDagPath(0)

    def remove(self):
        children = self.get_children()
        parent = self.get_parent()
        for child in children:
            child.parent(parent)
        self.delete()

    def insert_parent(self, replacement_parent_node):
        replacement_parent_mtransform = self.factory(replacement_parent_node)
        replacement_parent_mtransform.parent(self.get_parent())
        self.parent(replacement_parent_mtransform)

    def refresh_meta_attrs(self):
        self.meta_attrs = mc.listAttr(self.metadata_network, userDefined=True)

    def __getattr__(self, item):
        if not item in ['node', '_dag_path']:
            try:
                return mc.getAttr('%s.%s' % (super(MayaNode, self).__getattribute__('node'), item))
            except (ValueError, AttributeError):
                pass
        return super(MayaNode, self).__getattr__(item)

    def tag(self, tag_attr=DEFAULT_TAG_ATTR):
        self.top_group.set_attr(tag_attr, self.serialize())
