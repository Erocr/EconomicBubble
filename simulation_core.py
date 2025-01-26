import random
import numpy as np
from misc import *
from observer import *
from math import exp

def getNewValue(value, bonus, max_value):
    clamped_bonus = clamp(bonus, -max_value, max_value)
    return value + clamped_bonus - value * abs(clamped_bonus) / max_value

def priceIncrement(n: int):
    return n**1.65

class BaseNode:
    def __init__(self, bubble):
        self._value = 0
        self.volatility = 5
        self.max_value = 10_000
        self.bubble = bubble
        self.parents = []
        self.true_capital = 1_000
        self.debt = 0
    
    def addParent(self, node):
        self.parents.append(node)
        
    def addParents(self, nodes_list):
        for e in nodes_list:
            self.addParent(e)

    def quick_update(self):
        pass

    def update(self):
        for node in self.parents:
            self.influencedBy(node)
    
    def draw(self, view, inputs):
        self.bubble.update(inputs)
        self.bubble.draw(view)

    def notify(self, event, notifications):
        """ notifications doit etre de la forme (type_du_noeud, valeur_a_ajouter) """
        if event == EVENT_ADD_VALUE_NODE and type(self).__name__ == notifications[0]:
            self._value += notifications[1]

class TrueCapitalNode(BaseNode):
    def __init__(self, bubble):
        super().__init__(bubble)
        self._value = 10
        self.shares = 0 # Ratio of investment, between 0 and 1
    
    def update(self):
        super().update()
        self.bubble.set_text(
            f"True capital {to_readable_int(self._value)}$"
        )
        value = self._value
        if value < 100:
            self.bubble.color_border = (255, 0, 0)

        else:
            self.bubble.color_border = (108, 104, 101)
        self.bubble.set_fill_level(1-exp(-1/1000*self._value))

    def influencedBy(self, parent):
        if type(parent) == MarketNode:
            self._value += parent._value * parent.mult

        elif type(parent) == InvestorsDoubtNode:
            self._value *= (1 - self.shares)
            if parent._value < 0.5 * parent.max_value:
                if self.shares < 0.8 and parent.interest > 1.1:
                    self.shares += parent.invest(self.shares)
            else:
                self.shares -= parent.pullout(self.shares)
            self.shares = clamp(self.shares, 0, 0.8)
            self._value /= (1 - self.shares)
    
    def tutorial(self):
        return f"test"

class ApparentCapitalNode(BaseNode):
    def __init__(self, bubble):
        super().__init__(bubble)
        self._value = 1000
        self.persuade = 0.1
        self.true_capital = 0

    def update(self):
        self.true_capital = self.parents[0]._value # hacky fix, change later
        self._value = max(self._value, self.true_capital)
        super().update() 
        self.bubble.set_text(
            f"Shown capital {to_readable_int(self._value)}$"
        )

        self.persuade = clamp(self.persuade, 0, 1)
        self.persuade /= 1.1
        # print(f"{self.persuade = }")
        
    def influencedBy(self, parent):
        if (type(parent) == TrueCapitalNode):
            self._value = self.persuade * self._value + (1 - self.persuade) * parent._value

        if (type(parent) == MarketingNode):
            self.persuade = getNewValue(self.persuade, parent._value/500, 1)
            if self.true_capital == 0:
                print("aaaaaaaaaaaa")
            else:
                self._value = getNewValue(self._value, parent._value/200 * self.true_capital, self.true_capital*10)

        if (type(parent) == PublicDoubtNode):
            self.persuade = getNewValue(self.persuade, parent._value/500, 1)

class MarketNode(BaseNode):
    def __init__(self, bubble, name):
        super().__init__(bubble)
        self._value = 1
        self.max_value = 194
        self.tendance = 1
        self.mult = 1
        self.maxmult = 5
        self.name = name
        self.is_click = False
        self.nb_clicks = 1

    def quick_update(self):
        self._value += random.random()/4_000
        self._value += random.gauss(self.tendance, self.volatility*10)/2_000
        self.tendance /= 1.1
        if self.bubble.clicked():
            self.is_click = True

    def update(self):
        super().update()

        self._value = clamp(self._value, random.randint(3, 12)/100, random.randint(163, 194)/100)

        self.bubble.set_text(
            f"{self.name} {to_readable_int(priceIncrement(self.nb_clicks))}$ {to_readable_int(self._value)}$ {self.mult:.1f} tendance {round(self.tendance, 2)}"
        )
    
    def influencedBy(self, parent):
        if type(parent) == PublicDoubtNode:
            self.tendance += -10 * 2*(parent._value - parent.max_value / 2) / parent.max_value
        
        if type(parent) == EspionageNode:
            if parent.is_click:
                self.maxmult += 0.5
                self.mult += 0.5
                # parent.is_click = False
        
        if type(parent) == TrueCapitalNode:
            if self.is_click:
                price = priceIncrement(self.nb_clicks)
                if price <= parent._value:
                    self.mult += 0.1
                    self.mult = clamp(self.mult, 0, self.maxmult)
                    self.nb_clicks += 1
                    parent._value -= price
                self.is_click = False

class PublicDoubtNode(BaseNode):
    def __init__(self, bubble):
        super().__init__(bubble)
        self.max_value = 100
    
    def update(self):
        super().update()
        self._value -= 0.05
        self._value += random.gauss(0, self.volatility/500)
        self._value = clamp(self._value, 0, self.max_value)

        self.bubble.set_text(
            f"Public Doubt {to_readable_int(self._value)}%"
        )

    def influencedBy(self, parent):
        if type(parent) == MarketingNode:
            self._value = getNewValue(self._value, -parent._value/2, self.max_value)
        
        if type(parent) == InvestorsDoubtNode:
            self._value = getNewValue(self._value, parent._value/25, self.max_value)

        if type(parent) == EventNode:
            pass
        
class InvestorsDoubtNode(BaseNode):
    def __init__(self, bubble):
        super().__init__(bubble)
        self.max_value = 100
        # the investors observe for some time, which helps
        # then calculate how much they doubt you, as well as
        # how interested they are
        self.invested = 0
        self.pulled_out = 0
        self.interest = 1

        self.observing_for = 7
        self.records = []

    def all_eyes_on(self):
        self.observing_for = 3
        self.records = []
    
    def stop_watching(self):
        self.observing_for = 7
        self.records = []

    def record(self, value):
        if len(self.records) > 0:
            newavg = self.records[-1] * len(self.records)
            newavg = (newavg + value) / (len(self.records) + 1)
        else: newavg = value
        self.records.append(newavg)
        # print(str(self._value) + ", " + str(newavg))


    def influencedBy(self, parent):
        if type(parent) == ApparentCapitalNode:
            self.record(parent._value)
            # once enough info is given:
            if len(self.records) > self.observing_for:
                res = self.records[-1] - self.records[0] 
                res /= self.records[0]
                # print(str(res) + " & ")
                if abs(res) < 0.2 / self.volatility:
                    self._value *= 1.01; return
                if res < 0:
                    self._value *= (1 + abs(res))
                    self.interest = max(1, self.interest - 0.05)
                    if self._value > 75: self.all_eyes_on()
                else:
                    self.stop_watching()
                    self.interest = min(1.5, self.interest + 0.05)
                    self._value /= (1 + res)

        if type(parent) == EventNode:
            # self._value = getNewValue()
            pass

    def update(self):
        super().update()

        self._value += random.gauss(0, 1) * self.volatility
        self._value -= 0.05
        self._value = clamp(self._value, 1, 100)

        self.bubble.set_text(
            f"Investors Doubt {to_readable_int(self._value)}%"
        )

    def invest(self, shares): 
        # invest only after observing
        if len(self.records) < self.observing_for or self.invested > 0: 
            return 0
        if random.random() * 100 > self._value:
            self.invested = random.random() * (0.8 - shares) / 2.5
            self.invested *= self.interest
            self.invested *= (1 - self._value / 100)
            if self.invested * 100 < 1: self.invested = 0
            return self.invested
        return 0

    def pullout(self, shares):
        # pullout if doubt starts to grow
        if len(self.records) < self.observing_for or self.pulled_out > 0:
            return 0
        if random.random() * 100 < self._value:
            self.pulled_out = random.random() * shares / 2
            self.pulled_out /= self.interest
            self.pulled_out *= self._value / 100
            if self.pulled_out * 100 < 1: self.pulled_out = 0
            return self.pulled_out
        return 0

class MarketingNode(BaseNode):
    def __init__(self, bubble):
        super().__init__(bubble)
        self.is_click = False
        self.nb_clicks = 1

    def quick_update(self):
        if self.bubble.clicked():
            self.is_click = True

    def update(self):
        super().update()
        self._value = max(0, self._value - 1)
        # if self.is_click:
        #     self._value = getNewValue(self._value, 10, 100)
        #     self.is_click = False
        #     self.debt += 50 + self.true_capital/80
            # self._value = clamp(self._value, 0, 10_000)

        self.bubble.set_text(
            f"Marketing {to_readable_int(self.nb_clicks ** 2)}$ {to_readable_int(self._value)}%"
        )
    
    def influencedBy(self, parent):
        if type(parent) == TrueCapitalNode:
            if self.is_click:
                price = self.nb_clicks ** 2
                if price <= parent._value:
                    self._value = getNewValue(self._value, 10, 100)
                    self.nb_clicks += 1
                    parent._value -= price
                self.is_click = False

class SecurityNode(BaseNode):
    def __init__(self, bubble):
        super().__init__(bubble)
        self.is_click = False
        self.nb_clicks = 1


    def quick_update(self):
        if self.bubble.clicked():
            self.is_click = True

    def update(self):
        super().update()
        # if self.is_click:
        #     self._value = getNewValue(self._value, 10, 100)
        #     self.debt += 50 + self.true_capital/80
        #     self.is_click = False
        
        self.bubble.set_text(
            f"Security {to_readable_int(self.nb_clicks ** 2)}$ {to_readable_int(self._value)}%"
        )
    
    def influencedBy(self, parent):
        if type(parent) == TrueCapitalNode:
            if self.is_click:
                price = self.nb_clicks ** 2
                if price <= parent._value:
                    self._value = getNewValue(self._value, 10, 100)
                    self.nb_clicks += 1
                    parent._value -= price
                self.is_click = False

class EspionageNode(BaseNode):
    def __init__(self, bubble):
        super().__init__(bubble)
        self.is_click = False
        self.nb_clicks = 1
        

    def quick_update(self):
        if self.bubble.clicked():
            self.is_click = True

    def update(self):
        self._value = max(0, self._value - 1)
        super().update()
        # if self.is_click:
        #     self._value = getNewValue(self._value, 10, 100)
        #     self.debt += 50 + self.true_capital/80
        #     self.is_click = False
            
        
        self.bubble.set_text(
            f"Espionage {to_readable_int(self.nb_clicks ** 2)}$ {to_readable_int(self._value)}%"
        )
    
    def influencedBy(self, parent):
        if type(parent) == TrueCapitalNode:
            if self.is_click:
                price = self.nb_clicks ** 2
                if price <= parent._value:
                    self._value = getNewValue(self._value, 10, 100)
                    self.nb_clicks += 1
                    parent._value -= price
                self.is_click = False

class EventNode(BaseNode):
    def __init__(self, bubble):
        super().__init__(bubble)
        self.events = []
    
    def update(self):
        super().update()

    def influencedBy(self, parent):
        # TODO
        # if type(parent) == EspionageNode:
            # createEvent
        pass

class Event():
    def __init__(self, TTL, vol, dbt, risk):
        self.time_to_live = TTL
        self.volatility = vol
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
                
        self.bubble.set_text(
            f"Event {to_readable_int(self._value)}$"
        )
