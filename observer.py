EVENT_ADD_VALUE_NODE = 0
EVENT_FLASH_INFO = 1
EVENT_NEW_POPUP = 2

EVENT_SOUND = 3


class Observer:
    """
    Permet de l'echange d'information entre deux classes eloignees.
    Un observable est une instance avec la methode notify(event, notifications)
    """
    def __init__(self):
        self.observables = []

    def notify(self, event, notifications):
        for observable in self.observables:
            observable.notify(event, notifications)

    def add_observable(self, observable):
        self.observables.append(observable)

