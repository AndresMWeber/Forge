import maya.cmds as mc


def zero_local_space(transform_dag, **kwargs):
    return mc.makeIdentity(transform_dag, **kwargs)


def spatial_interpolate(start, end, samples):
    """ Interpolate between two points with a given number of samples
        Usage:
            spatial_interpolate([0,0,0],[0,-10,0], 5)
            spatial_interpolate([24.28, 0.0, 10.72], [26.87, 0.0, -6.72], 5)

    :param start: list(float, float, float), 3d point
    :param end: list(float, float, float), 3d point
    :param samples: int, number of output points including start and end
    :returns: list(list(float, float, float)): list of 3d points
    """
    spx, spy, spz = [abs(x - y) / float(samples - 1) for x, y in zip(start, end)]
    dirX, dirY, dirZ = [-1 if sp > ep else 1 for sp, ep in zip(start, end)]
    mid_points = [[(start[0] + index * spx * dirX),
                   (start[1] + index * spy * dirY),
                   (start[2] + index * spz * dirZ)] for index in range(1, samples - 1)]
    mid_points.insert(0, [float(i) for i in start])
    mid_points.append([float(i) for i in end])
    return mid_points


""" TODO: Need to refactor without numpy.
def slerp_quaternion(p0, p1, t):
    omega = np.arccos(np.dot(p0/norm(p0), p1/norm(p1)))
    so = np.sin(omega)
    return np.sin((1.0-t)*omega) / so * p0 + np.sin(t*omega)/so * p1
"""
