import forge
import chain


@forge.register_node
class ChainJoint(chain.Chain):
    NODE_TYPE = forge.registry.joint
