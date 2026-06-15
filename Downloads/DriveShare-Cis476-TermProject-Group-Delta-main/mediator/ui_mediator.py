# Owned By Mohammed
# Mediator Pattern
# UIMediator lets modules communicate without directly depending on each other.


class UIMediator:
    def __init__(self):
        self.components = {}

    def register(self, name, component):
        self.components[name] = component
        component.mediator = self

    def notify(self, sender, event, data=None):
        data = data or {}

        for name, component in self.components.items():
            if component != sender:
                component.receive(event, data)
