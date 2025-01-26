EVENT_ADD_VALUE_NODE = 0
EVENT_FLASH_INFO = 1
EVENT_NEW_POPUP = 2
EVENT_SOUND = 3
EVENT_EVENT_BURST = 4
EVENT_MUL_VALUE_NODE = 5
EVENT_TRIGGER_CHOICES = 6

EVENT_PLAY_NORMAL = 7
EVENT_PLAY_CRITICAL = 8

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

    def add_observables(self, observables):
        for ob in observables:
            self.add_observable(ob)