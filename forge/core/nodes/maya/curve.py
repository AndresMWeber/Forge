from itertools import chain

import maya.cmds as mc
from forge.core.core_utils.maya_utils import curve as util_curve
from forge.core.nodes.base.curve import AbstractCurve

import forge
from forge.core.nodes.maya.transform import MayaTransform


@forge.register_node
class MayaCurve(MayaTransform, AbstractCurve):
    """
    class for building templates control
    """
    TYPE = 'nurbs_curve'
    ENGINE_TYPE = 'nurbsCurve'

    def __init__(self, node_dag='', *args, **kwargs):
        super(MayaCurve, self).__init__(node_dag=node_dag, *args, **kwargs)

    @property
    def all_curve_cvs(self):
        shapes = self.get_shapes(types='nurbsCurve')
        if shapes:
            cvs = [util_curve.get_cvs(child) for child in shapes]
            if cvs:
                return list(chain.from_iterable(cvs))

    def transform_shapes(self, translation=None, rotation=None, scale=None, relative=True):
        if translation:
            self.translate_shapes(translation, relative)
        if rotation:
            self.rotate_shapes(rotation, relative)
        if scale:
            self.scale_shapes(scale, relative)

    def scale_shapes(self, scale=1.0, relative=True):
        mc.xform(self.all_curve_cvs, relative=relative, scale=[scale] * 3)
        self.scale = scale

    def rotate_shapes(self, rotation=(0, 0, 0), relative=True):
        mc.xform(self.all_curve_cvs, relative=relative, rotation=rotation)

    def translate_shapes(self, translation=(0, 0, 0), relative=True):
        mc.xform(self.all_curve_cvs, relative=relative, translation=translation)

    def swap_shape(self, shape='cube', maintain_offset=True, add=False):
        """
        Swaps the shape with an alternative predefined control shape
        :param shape: str, given shape from list in rig_lib.core.nodes.maya_utils.factory.MayaControlShapeFactory
        :param maintain_offset: whether or not we want it to be centered where the original control was
        :param add: if we want to add to the shapes or not
        :return: None
        """
        if not add:
            mc.delete(self.get_shapes(types=MayaCurve.ENGINE_TYPE))

        target_shape = forge.registry.curve(getattr(forge.shapes, shape)())
        shapes = target_shape.get_children(type=MayaCurve.ENGINE_TYPE)
        print('Shapes to reparent...', [shape.node for shape in shapes])
        mc.parent([shape.node for shape in shapes], self.node, relative=not maintain_offset, shape=True)
        print('New parents: ', [shape.get_parent() for shape in shapes])
        if maintain_offset:
            for shape in shapes:
                parent = shape.get_parent()
                forge.registry.utils.transformation.zero_local_space(parent.node,
                                                                     apply=True,
                                                                     translate=True,
                                                                     rotate=True,
                                                                     scale=True)
                target_shape.parent(self.node, relative=maintain_offset, shape=True)

        forge.registry.utils.scene.safe_delete(target_shape)
