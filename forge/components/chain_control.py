import forge
import chain


@forge.register_node
class ChainControl(chain.Chain):
    NODE_TYPE = forge.registry.Control
