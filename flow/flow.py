class Flow(object):
    def __init__(self, material):
        self._actions = []
        self._material = material

    def add_action(self, action):
        self._actions.append(action)

    def run(self):
        for action in self._actions:
            effect = action.execute()
            effect.apply_to(self._material)

    @property
    def material(self):
        return self._material
