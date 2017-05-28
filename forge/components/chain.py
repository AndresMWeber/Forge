import forge
scene = forge.registry.utils.scene


@forge.register_node
class Chain(object):
    NODE_TYPE = forge.registry.transform

    def __init__(self, nodes):
        self.nodes = []
        for node in nodes:
            self.nodes.append(node)

    @classmethod
    def create(cls, reference_transforms, move_style='match'):
        reference_chain = cls.factory(reference_transforms)

        created_nodes = []
        for reference_transform in reference_chain:
            created_nodes.append(cls.NODE_TYPE.create(move_style=move_style,
                                                      reference_transform_dag=reference_transform))
        return cls(created_nodes)

    @classmethod
    def factory(cls, transforms):
        transform_instances = [cls.NODE_TYPE.factory(transform) for transform in transforms
                               if scene.is_exact_type(transform, cls.NODE_TYPE.ENGINE_TYPE)]
        return transform_instances

    def set_hierarchy(self):
        for transform_a, transform_b in zip(self.nodes[:-1], self.nodes[1:]):
            transform_b.parent(transform_a)

    def reverse_hierarchy(self):
        self.unparent_hierarchy()
        for transform_a, transform_b in zip(reversed(self.nodes[:-1]), reversed(self.nodes[1:])):
            transform_b.parent(transform_a)
        self.nodes = list(reversed(self.nodes))

    def unparent_hierarchy(self, parent=None):
        for node in self.nodes:
            if parent is None:
                node.unparent()
            else:
                node.parent(parent)

    def __iter__(self):
        for node in self.nodes:
            yield node

    def __len__(self):
        return len(self.nodes)

    def __getitem__(self, index):
        return self.nodes[index]


