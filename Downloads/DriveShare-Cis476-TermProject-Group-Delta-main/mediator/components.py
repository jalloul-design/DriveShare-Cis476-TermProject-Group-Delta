# Owned By Mohammed
# Base Component class for the Mediator pattern.


class Component:
    def __init__(self, name):
        self.name = name
        self.mediator = None

    def send(self, event, data=None):
        if self.mediator is not None:
            self.mediator.notify(self, event, data or {})

    def receive(self, event, data=None):
        # Subclasses can override this method.
        print(f"{self.name} received event: {event} with data: {data}")
