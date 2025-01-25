import random

def clamp(val, min_, max_):
    return min(max(val, min_), max_)

def getNewValue(value, bonus, max_bonus):
    clamped_bonus = clamp(bonus, -max_bonus, max_bonus)
    return value + clamped_bonus - value * abs(clamped_bonus) / max_bonus


class BaseNode:
    def __init__(self):
        self.value_history = []
        self._value = 0
        self._stability = 0
        self.max_value = 10_000
        self.parents = []
    
    def addParent(self, node):
        self.parents.append(node)
        
    def addParents(self, nodes_list):
        for e in nodes_list:
            self.addParent(e)

    def clamp(self):
        self._value = clamp(self._value, 0, self.max_value)
        self._stability = clamp(self._stability, 0, self.max_value)
    
    def update(self):
        self.value_history.append(self._value)


class TrueCapitalNode(BaseNode):
    def __init__(self):
        super().__init__()
        self.shares = 0 # Ratio of investment, between 0 and 1
    
    def update(self):
        for node in self.parents:
            self.influencedBy(node)
        super().update()
    
    def influencedBy(self, parent):
        if type(parent) == MarketNode:
            self._value += parent._value * parent.mult
        elif type(parent) == InvestorsDoubtNode:
            self._value *= (1 - self.shares)
            if parent._value < 0.5:
                self.shares += parent.invest(self.shares)
            else:
                self.shares -= random.gauss(parent._value, 0.5)
            clamp(self.shares, 0, 1)
            self._value *= (1 + self.shares)            

class ApparentCapitalNode(BaseNode):
    def __init__(self):
        super().__init__()
        self.persuade = 0.1

    def update(self):
        for node in self.parents:
            self.influencedBy(node)
        super().update()

    def influencedBy(self, parent):
        if (type(parent) == TrueCapitalNode):
            self._value = self.persuade * self._value + (1 - self.persuade) * parent._value

        if (type(parent) == MarketingNode):
            self.persuade = getNewValue(self._value, parent._value/10, 100)
            self._value = getNewValue(self._value, parent._value, 100)

class MarketNode(BaseNode):
    def __init__(self):
        super().__init__()
        self.tendance = 1
        self.mult = 1

    def update(self):
        for node in self.parents:
            self.influencedBy(node)

        self._value += random.gauss(self.tendance, self._stability)
        self.tendance /= 2
        super().update()
    
    def influencedBy(self, parent):
        if type(parent) == PublicDoubtNode:
            self.tendance = getNewValue(self.tendance, parent._value, 25)
        
        if type(parent) == EspionageNode:
            self._value = getNewValue(self._value, parent._value, 25)

class PublicDoubtNode(BaseNode):
    def __init__(self):
        super().__init__()
        self.max_value = 100
    
    def update(self):
        for node in self.parents:
            self.influencedBy(node)

        self._value += random.gauss(0, 1) * self._stability

        self.clamp()
        super().update()
        
    def influencedBy(self, parent):
        if type(parent) == MarketingNode:
            self._value = getNewValue(self._value, parent._value, 100)
        
        elif type(parent) == EventNode:
            pass
        
    
class InvestorsDoubtNode(BaseNode):
    def __init__(self):
        super().__init__()
        self.max_value = 100

    def influencedBy(self, parent):
        if type(parent) == MarketNode:
            self._value = getNewValue(2*(parent.max_value/2 - parent._value) / parent.max_value)        
        if type(parent) == EventNode:
            # self._value = getNewValue()
            pass

    def update(self):
        for node in self.parents:
            self.influencedBy(node)
        self._value += random.gauss(0, 1) * self._stability
        self.clamp()
        super().update()

    def invest(self, shares):
        if random.random() > self._value:
            return random.random() * (1 - shares)

class MarketingNode(BaseNode):
    def __init__(self):
        super().__init__()

    def update(self, bonus):
        self._value += getNewValue(self._value, bonus, 100)
        self.clamp()

class SecurityNode(BaseNode):
    def __init__(self):
        super().__init__()

    def update(self, bonus):
        self._value += getNewValue(self._value, bonus, 100)
        self.clamp()
        super().update()


class EspionageNode(BaseNode):
    def __init__(self):
        super().__init__()

    def update(self, bonus):
        self._value += getNewValue(self._value, bonus, 100)
        self.clamp()
        super().update()

class EventNode(BaseNode):
    def __init__(self):
        super().__init__()
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