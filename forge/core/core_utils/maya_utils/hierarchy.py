import pymel.core as pm
import maya.cmds as mc

def list_relatives(node, **kwargs):
    return mc.listRelatives(node, **kwargs)

def shortest_name(name):
    return name.rpartition('|')[-1].rpartition(':')[-1]


def find_match(top_node, target_node):
    name = shortest_name(target_node.name())
    for node in [top_node] + top_node.listRelatives(ad=True):
        # Just need to see if removing one character (if we have a duplicate name) finds a match (e.g. node1 and node)
        if shortest_name(node.name()) == name or shortest_name(node.name())[:-1] == name or shortest_name(
                node.name()) == name[:-1]:
            return node
    return None


def replace_model(top_group_source, top_group_target, delete=True):
    """ Meant for simple prop replacement and constraint replacements
    :param top_group_source: pm.nt.Transform, transform node of top group you want to replace with
    :param top_group_target: pm.nt.Transform, transform node of top group you want to replace
    :param delete: bool, delete the top_group_target or not
    :return: 
    """
    top_group_orig_name = shortest_name(top_group_target.name())
    constraint_types = ['parentConstraint', 'scaleConstraint', 'pointConstraint', 'scaleConstraint']
    constraints = find_in_hierarchy(top_group_target, type=constraint_types)
    pm.parent(top_group_source, top_group_target.getParent())

    for constraint in constraints:
        constraint_source = constraint.getTargetList()[0]
        constraint_target = find_match(top_group_source, list(set(constraint.listConnections(d=True)))[0])
        recreate_constraint(constraint, constraint_source, constraint_target)

    replace_set_members(top_group_target, top_group_source, delete=delete)

    if delete:
        pm.delete(top_group_target)
    top_group_source.rename(top_group_orig_name)
    return top_group_source


def find_in_hierarchy(top_node, type=None, connections=True):
    """
    
    :param top_node: 
    :param type: str|list(str), list of types of nodes to look for or just nodes to look for
    :param connections: bool): whether to search through connections or not
    :return: 
    """
    """ Goes through a hierarchy and gets all connected objects of a specific type
    Args:
        type 
        connections (
    Returns [pm.nt.type]: list of nodes of type specified in args
    Usage:
        find_in_hierarchy(type='parentConstraint')
    """
    connected_objects = []
    for obj in top_node.listRelatives(c=True, ad=True):
        if connections:
            connected_objects += obj.listConnections(type=type)
        else:
            connected_objects += obj.listRelatives(type=type)
    # return list while removing doubles
    return list(set(connected_objects))


def recreate_constraint(constraint_in, source, target, mo=True):
    """ Recreates a constraint from the given example to a source and target
    Args:
        constraint_in (pm.PyNode): constraint to model after
        source (pm.nt.Transform): object to do the constraining
        target (pm.nt.Transform): object to be constrained
        mo (bool): maintain offset
    Usage:
        recreate_constraint(*pm.ls(sl=True)[:3])
    """
    constraint_types = ['parentConstraint', 'scaleConstraint', 'pointConstraint', 'scaleConstraint']
    constraint_parent = constraint_in.getParent()
    constraint_type = constraint_in.type()
    constraint_func = getattr(pm, constraint_type)

    # Create the constraint and parent if it's not an "auto parent"
    if source and target:
        constraint = constraint_func(source, target, mo=mo)
        if not shortest_name(constraint_parent.name()) in shortest_name(target.name()):
            pm.parent(constraint, constraint_parent)

        if constraint_type in constraint_types:
            for attr in constraint_in.listAttr():
                try:
                    constraint.attr(attr.name(includeNode=False)).set(attr.get())
                except (RuntimeError, pm.MayaAttributeError) as e:
                    pass
                    # print constraint_parent, constraint_type
        else:
            pm.error('Constraint type not supported yet, sorry')


def replace_set_members(top_group_source, top_group_target, starts_with='cacheSet', delete=True):
    """ This script assumes that only ONE set is the actual set that these objects are added to 
        and that it's an ftrack cache set by default
    Args:
        top_group_source (pm.nt.Transform): top group of the source objects to get sets
        top_group_target (pm.nt.Transform): top group of the target objects to add to sets
    Returns: [pm.nt.ObjectSet]: list of object sets we added to
    Usage:
        replace_set_members(*pm.ls(sl=True)[:2])
    """

    top_group_source_hierarchy = [xform for xform in top_group_source.listRelatives(type='transform', ad=True) if
                                  xform.getShape()]
    top_group_target_hierarchy = [xform for xform in top_group_target.listRelatives(type='transform', ad=True) if
                                  xform.getShape()]

    source_sets = []
    for xform in top_group_source_hierarchy:
        source_sets.extend(xform.listConnections(type='objectSet'))
    source_sets = list(set(source_sets))

    target_sets = []
    for xform in top_group_target_hierarchy:
        target_sets.extend(xform.listConnections(type='objectSet'))
    target_sets = list(set(target_sets))

    for set_m in source_sets:
        if set_m.startswith(starts_with):
            for xform in top_group_target_hierarchy:
                pm.sets(set_m, add=xform)
            for xform in top_group_source_hierarchy:
                pm.sets(set_m, rm=xform)

    for target_set in target_sets:
        if not target_set in source_sets and delete:
            pm.delete(target_set)

    return source_sets