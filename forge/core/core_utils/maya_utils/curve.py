import maya.cmds as mc


def get_cvs(curve_transform, slice_start='', slice_end=''):
    slicer = '{START}:{END}'.format(START=str(slice_start), END=str(slice_end))
    return mc.ls('{CURVE_TRANSFORM}.cv[{SLICE}]'.format(CURVE_TRANSFORM=curve_transform, SLICE=slicer), fl=True)


def get_num_cvs(curve_transform):
    return len(mc.ls('{CURVE_TRANSFORM}.cv[:]'.format(CURVE_TRANSFORM=curve_transform), fl=True))
