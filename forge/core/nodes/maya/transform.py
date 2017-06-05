import maya.cmds as mc
from forge.core.nodes.base.transform import AbstractTransform
from forge.core.nodes.maya.node import MayaNode

import forge
from forge.core import channels
from forge.exception import exception, ValidationError


@forge.register_node
class MayaTransform(MayaNode, AbstractTransform):
    """
         Wraps a dag_path with generic functions to manipulate a maya_utils node and transform functions
    """

    def __init__(self, node_dag='', **kwargs):
        super(MayaTransform, self).__init__(node_dag=node_dag, **kwargs)

    @staticmethod
    def create_engine_instance(node_type='group', *args, **kwargs):
        if node_type in ['group']:
            node = forge.registry.maya_group(*args, **kwargs)
        elif node_type in ['locator']:
            node = forge.registry.maya_locator(*args, **kwargs)
        else:
            raise ValidationError("Unsupported transform type input %s." % node_type)
        return node

    @classmethod
    def create(cls, node_type='group', move_style='match', reference_transform_dag='', parent=None, *args, **kwargs):
        maya_transform = super(MayaTransform, cls).create(node_type='group', *args, **kwargs)
        if reference_transform_dag:
            reference_transform_dag = cls.factory(reference_transform_dag)
            maya_transform.transform(move_style, reference_transform_dag)

        if parent:
            cls.LOG.debug('Setting parent to %s' % parent)
            maya_transform.parent(parent)

        return maya_transform

    def transform(self, move_style, reference_transform_dag):
        if reference_transform_dag.exists:
            if move_style == 'match':
                self._move_to_obj(reference_transform_dag)
            elif (move_style == 'position') or (move_style == 'translation'):
                self._translate_to_obj(reference_transform_dag)
            elif move_style == 'rotation':
                self._rotate_to_obj(reference_transform_dag)

    def position(self, t=(0.0, 0.0, 0.0), world_space=True, q=False):
        t = t if not q else q
        return mc.xform(self.node, q=q, os=not world_space, ws=world_space, t=t)

    def rotation(self, r=(0.0, 0.0, 0.0), world_space=True, q=False):
        r = r if not q else q
        return mc.xform(self.node, q=q, os=not world_space, ws=world_space, ro=r)

    def _translate_to_obj(self, target_dag_path):
        pos = mc.xform(target_dag_path.node, q=True, ws=True, t=True)
        self.pos(q=False, t=pos)

    def _rotate_to_obj(self, target_dag_path):
        null = MayaTransform.create(name='NULL')
        null.set_attr('r', self.r)

        target_mtransform = self.__class__(target_dag_path)
        parent = target_mtransform.get_parent()
        if parent:
            null.parent(parent)

        mc.orientConstraint(target_mtransform.node, null.node)

        parent = self.get_parent()
        if parent:
            null.parent(parent)

        self.set_attr('r', null.r, type=channels.TYPES.DOUBLE3)
        null.delete()

    def _move_to_obj(self, target_dag_path):
        self._translate_to_obj(target_dag_path)
        self._rotate_to_obj(target_dag_path)

    def __str__(self):
        return self.name_long
