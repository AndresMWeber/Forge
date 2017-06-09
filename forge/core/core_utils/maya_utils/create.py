import maya.cmds as mc
from . import curve as util_curve


def joint(*args, **kwargs):
    return mc.joint(*args, **kwargs)


def group(em=True, *args, **kwargs):
    return mc.group(em=em)


def curve(**kwargs):
    try:
        mc.curve(**kwargs)
    except RuntimeError:
        return mc.curve(d=1, p=[(1, 0, 0), (0, 0, -1), (-1, 0, 0), (0, 0, 1), (1, 0, 0)])


def locator(*args, **kwargs):
    return mc.spaceLocator(*args, **kwargs)


def semi_circle(constructionHistory=True, *args, **kwargs):
    circle = mc.circle(constructionHistory=constructionHistory, *args, **kwargs)[0]
    median_cv = int(round(util_curve.get_num_cvs(circle) / 2))
    mc.xform(util_curve.get_cvs(circle, slice_start=median_cv), r=1, s=[0, 0, 1])
    return circle


def circle(constructionHistory=True, *args, **kwargs):
    return mc.circle(constructionHistory=constructionHistory, *args, **kwargs)[0]


def meta_node(*args, **kwargs):
    return mc.createNode('network', *args, **kwargs)
