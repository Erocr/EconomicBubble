import random


def clamp(val, min_, max_):
    return min(max(val, min_), max_)

def getNewValue(value, bonus, max_bonus):
    clamped_bonus = clamp(bonus, -max_bonus, max_bonus)
    return value + clamped_bonus - value * abs(clamped_bonus) / max_bonus


class BaseNode:
    def __init__(self):
        self._value = 0
        self._stability = 0
        self.max_value = 10_000

    def clamp(self):
        self._value = clamp(self._value, 0, self.max_value)
        self._stability = clamp(self._stability, 0, self.max_value)


class MarketNode(BaseNode):
    def __init__(self):
        super().__init__()
        self.tendance = 1

    def update(self, bonus):
        self.tendance += getNewValue(self.tendance, bonus, 25)
        self._value += random.gauss(self.tendance, self._stability)
        


class DoubtNode(BaseNode):
    def __init__(self):
        super().__init__()
    
    
    def update(self, bonus):
        self._value = getNewValue(self._value, bonus, self.max_value)
        self._value += random.gauss(0, 1) * self._stability

        self.clamp()
    
    def computeMarketBonus(self):
        pass
    
    def computeApparentCapitalBonus(self):
        pass

class TrueCapitalNode(BaseNode):
    
    def update(self, bonus):
        self._value += bonus
    
class ApparentCapitalNode(BaseNode):
    def __init__(self):
        super().__init__()
        self.persuade = 0.1

    def update(self, true_capital, bonus):
        self._value = self._value * self.persuade + true_capital * (1 - self.persuade)

        self._value += bonus



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
        

    

