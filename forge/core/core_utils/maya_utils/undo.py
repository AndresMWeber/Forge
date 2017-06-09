
import maya.cmds as mc
import contextlib


class UndoChunk():
    def __enter__(self):
        print('opening chunk and turning undo queue on.')
        mc.undoInfo(stateWithoutFlush=True)
        mc.undoInfo(openChunk=True)

    def __exit__(self, type, exception, traceback):
        mc.undoInfo(closeChunk=True)
        if exception is not None:
            mc.undo()

class UnitContext(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.oldlin, self.oldang, self.oldtim = None, None, None
    def __enter__(self):
        self.oldlin = pmc.currentUnit(q=True, linear=True)
        self.oldang = pmc.currentUnit(q=True, angle=True)
        self.oldtim = pmc.currentUnit(q=True, time=True)
        pmc.currentUnit(*self.args, **self.kwargs)
    def __exit__(self, *_):
        if self.oldlin is not None:
            pmc.currentUnit(linear=self.oldlin)
        if self.oldang is not None:
            pmc.currentUnit(angle=self.oldang)
        if self.oldtim is not None:
            pmc.currentUnit(time=self.oldtim)

class RenderLayerContext(object):
    def __init__(self, renderlayer):
        self.renderlayer = renderlayer
        self.orig_layer = None
    def __enter__(self):
        self.orig_layer = pmc.nodetypes.RenderLayer.currentLayer()
        self.renderlayer.setCurrent()
    def __exit__(self, *_):
        if self.orig_layer is not None:
            self.orig_layer.setCurrent()

class NamespaceContext(object):
    def __init__(self, ns):
        if ns == '':
            # This would be too ambiguous, so prohibit it
            raise ValueError('argument cannot be an empty string')
        self.ns = ns
        self.oldns = None
    def __enter__(self):
        self.oldns = pmc.namespaceInfo(currentNamespace=True)
        pmc.namespace(setNamespace=self.ns)
    def __exit__(self, *_):
        if self.oldns is not None:
            oldns = ':' + self.oldns.lstrip(':')
            pmc.namespace(setNamespace=oldns)
