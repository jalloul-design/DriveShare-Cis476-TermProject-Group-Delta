# Owned By Mohammed
# Basic tests for messaging and mediator structure.

from mediator.ui_mediator import UIMediator
from mediator.components import Component


class TestComponent(Component):
    def __init__(self, name):
        super().__init__(name)
        self.received_events = []

    def receive(self, event, data=None):
        self.received_events.append((event, data))


def test_mediator_routes_events_between_components():
    mediator = UIMediator()
    sender = TestComponent("sender")
    receiver = TestComponent("receiver")

    mediator.register("sender", sender)
    mediator.register("receiver", receiver)

    sender.send("booking_confirmed", {"booking_id": 1})

    assert len(receiver.received_events) == 1
    assert receiver.received_events[0][0] == "booking_confirmed"
