# Owned By Sleman
# Subject class for the Observer pattern

class CarSubject:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def detach(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify(self, event_type, data):
        for observer in self.observers:
            observer.update(event_type, data)