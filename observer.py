EVENT_ADD_VALUE_NODE = 0
EVENT_FLASH_INFO = 1
EVENT_NEW_POPUP = 2
EVENT_SOUND = 3
EVENT_EVENT_BURST = 4
EVENT_MUL_VALUE_NODE = 5
EVENT_TRIGGER_CHOICES = 6

EVENT_INVESTED = 7
EVENT_PULLED_OUT = 8
EVENT_PLAY_NORMAL = 8298
EVENT_PLAY_CRITICAL = 935
EVENT_APPLY_FUNC_NODE = 48589

EVENT_REQUEST_QUESTION = 20
EVENT_RIGHT_ANSWER = 21
EVENT_WRONG_ANSWER = 22

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