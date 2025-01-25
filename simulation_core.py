import random
import numpy as np

def clamp(val, min_, max_):
    return min(max(val, min_), max_)

def getNewValue(value, bonus, max_value):
    clamped_bonus = clamp(bonus, -max_value, max_value)
    return value + clamped_bonus - value * abs(clamped_bonus) / max_value

def string_shown_capital(val):
    return f"Shown capital: {val:.2f}$"
    
def string_true_capital(val):
    return f"True capital: {val:.2f}$"

class BaseNode:
    def __init__(self, bubble):
        self._value = 0
        self._stability = 0
        self.max_value = 10_000
        self.bubble = bubble
        self.parents = []
    
    def addParent(self, node):
        self.parents.append(node)
        
    def addParents(self, nodes_list):
        for e in nodes_list:
            self.addParent(e)

    def update(self):
        for node in self.parents:
            self.influencedBy(node)
    
    def draw(self, view, inputs):
        self.bubble.update(inputs)
        self.bubble.draw(view)


class TrueCapitalNode(BaseNode):
    def __init__(self, bubble):
        super().__init__(bubble)
        self.shares = 0 # Ratio of investment, between 0 and 1
    
    def update(self):
        super().update()
        self.bubble.set_text(string_true_capital(self._value))
    
    def influencedBy(self, parent):
        if type(parent) == MarketNode:
            self._value += parent._value * parent.mult
        elif type(parent) == InvestorsDoubtNode:
            self._value *= (1 - self.shares)
            if parent._value < 0.5:
                self.shares += parent.invest(self.shares)
            else:
                self.shares -= abs(random.gauss(1, 0.5) * parent._value)
            self.shares = clamp(self.shares, 0, 1)
            self._value *= (1 + self.shares)            


class ApparentCapitalNode(BaseNode):
    def __init__(self, bubble):
        super().__init__(bubble)
        self.persuade = 0.1

    def update(self):
        super().update()
        
        self.bubble.set_text(string_shown_capital(self._value))
        self.persuade = clamp(self.persuade, 0, 1)
        self._value = clamp(self._value, 0, 10_000)
        
        self.value_history.append(self._value)
        

    def influencedBy(self, parent):
        if (type(parent) == TrueCapitalNode):
            self._value = self.persuade * self._value + (1 - self.persuade) * parent._value

        if (type(parent) == MarketingNode):
            self.persuade = getNewValue(self._value, parent._value/10, 100)
            self._value = getNewValue(self._value, parent._value, 100)

        if (type(parent) == PublicDoubtNode):
            self.persuade = getNewValue(self.persuade, parent._value/100, 0.5)

class MarketNode(BaseNode):
    def __init__(self, bubble):
        super().__init__(bubble)
        self.tendance = 1
        self.mult = 1
        # self.graph = graph

    def update(self):
        super().update()

        if self.bubble.clicked():
            self.mult += 0.1
            self.mult = clamp(self.mult, 0, 5)

        self._value += random.gauss(self.tendance, self._stability)
        self.tendance /= 2
    
    def influencedBy(self, parent):
        if type(parent) == PublicDoubtNode:
            self.tendance = getNewValue(self.tendance, parent._value, 25)
        
        if type(parent) == EspionageNode:
            self._value = getNewValue(self._value, parent._value, 25)

class PublicDoubtNode(BaseNode):
    def __init__(self, bubble):
        super().__init__(bubble)
        self.max_value = 100
    
    def update(self):
        super().update()

        self._value += random.gauss(0, 1) * self._stability

        self._value = clamp(self._value, 0, 10_000)
        
    def influencedBy(self, parent):
        if type(parent) == MarketingNode:
            self._value = getNewValue(self._value, parent._value, 100)
        
        elif type(parent) == EventNode:
            pass
        
class InvestorsDoubtNode(BaseNode):
    def __init__(self, bubble):
        super().__init__(bubble)
        self.max_value = 100
        # the investors observe for some time, which helps
        # then calculate how much they doubt you
        self.observing_for = 7
        self.records = []

    def all_eyes_on(self):
        self.observing_for = 2
        self.records = []

    def influencedBy(self, parent):
        if type(parent) == ApparentCapitalNode:
            newavg = self.records[-1] * len(self.records)
            newavg = (newavg + parent._value) / (len(self.records) + 1)
            self.records.append(newavg)
            if len(self.records) > self.observing_for:
                res = self.records[-1] - self.records[0]
                if res / self.records[0] < 0.2:
                    self.observing_for += 1
                elif res < 0:
                    self._value *= (2 + 1 / res)
                    if res / self.records[0] > 0.4:
                        selfall_eyes_on()
                else:
                    self._value *= 1 / (res + 1)
                    
            return 0

        if type(parent) == EventNode:
            # self._value = getNewValue()
            pass

    def update(self):
        super().update()

        self._value += random.gauss(0, 1) * self._stability
        self._value = clamp(self._value, 0, 10_000)

    def invest(self, shares):
        if random.random() > self._value:
            return random.random() * (1 - shares) * (1 - self._value)

class MarketingNode(BaseNode):
    def __init__(self, bubble):
        super().__init__(bubble)

    def update(self):
        if self.bubble.clicked():
            self._value += getNewValue(self._value, 10, 100)
            self._value = clamp(self._value, 0, 10_000)

class SecurityNode(BaseNode):
    def __init__(self, bubble):
        super().__init__(bubble)

    def update(self):
        if self.bubble.clicked():
            self._value += getNewValue(self._value, 10, 100)
            self._value = clamp(self._value, 0, 10_000)
            super().update()


class EspionageNode(BaseNode):
    def __init__(self, bubble):
        super().__init__(bubble)

    def update(self):
        if self.bubble.clicked():
            self._value += getNewValue(self._value, 10, 100)
            self._value = clamp(self._value, 0, 10_000)

class EventNode(BaseNode):
    def __init__(self, bubble):
        super().__init__(bubble)
        self.events = []

class Event():
    def __init__(self, TTL, stb, dbt, risk):
        self.time_to_live = TTL
        self.stability = stb
        self.doubt = dbt
        
        # the probability of the event to burst
        self.risk = risk
        # determines if the event is live or not
        self.alive = True
    
    def burst(self):
        self.alive = False
        # then do something else...

    def update(self):
        self.time_to_live -= 1
        if self.time_to_live == 0:
            self.alive = False
        elif random.random() < self.risk:
            self.burst()