import random
import numpy as np
from misc import *
from observer import *
from math import exp
from vec import *

def getNewValue(value, bonus, max_value):
    clamped_bonus = clamp(bonus, -max_value, max_value)
    return value + clamped_bonus - value * abs(clamped_bonus) / max_value

def priceIncrement(n: int):
    return n**3

def marketPriceIncrement(n: int):
    return 10*n*np.log(n) + 15

class BaseNode:
    doc = "It's something clickable, maybe"
    def __init__(self, bubble, observer):
        self._value = 0
        self.volatility = 5
        self.max_value = 10_000
        self.bubble = bubble
        self.parents = []
        self.debt = 0
        self.observer = observer
        self.hover = False
    
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
    
    def draw(self, view, inputs, paused):
        if not paused:
            self.bubble.update(inputs)
        self.bubble.draw(view)
        self.hover = self.test_hover(inputs)

    def draw_docs(self, view):
        if self.hover:
            size_x = 200
            images = view.renders(self.doc, size_x, (255, 255, 255))
            y = 0
            for im in images:
                y += im.get_height()
            view.rect(self.bubble.center + DOWN*self.bubble.radius + LEFT*size_x/2, Vec(size_x, y), (0, 0, 0))
            pos = self.bubble.center + DOWN*self.bubble.radius
            for im in images:
                view.screen.blit(im, (pos - Vec(im.get_width() / 2, 0)).get)
                pos += Vec(0, im.get_height())

    def test_hover(self, inputs):
        return dist(inputs.mouse_pos, self.bubble.center) < self.bubble.radius


    def notify(self, event, notifications):
        """ notifications doit etre de la forme (type_du_noeud, valeur_a_ajouter) """
        pass
        # if event == EVENT_ADD_VALUE_NODE and type(self).__name__ == notifications[0]:
        #     self._value += notifications[1]

class TrueCapitalNode(BaseNode):
    doc = """Your True Capital, what you truly have, the money you can actually spend.\nNobody knows it. It's your darkest secret."""
    def __init__(self, bubble, observer):
        super().__init__(bubble, observer)
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
            self._value += parent._value * parent.worker

        elif type(parent) == InvestorsDoubtNode:
            self._value *= (1 - self.shares)
            if parent._value < 0.5 * parent.max_value:
                if self.shares < 0.8:
                    self.shares += parent.invest(self.shares)
            else:
                self.shares -= parent.pullout()
            self.shares = clamp(self.shares, 0, 0.8)
            self._value /= (1 - self.shares)
    
    def tutorial(self):
        return f"test"

class ApparentCapitalNode(BaseNode):
    doc = """Shown Capital : the capital you show to other people, you better lie very well if you want to make them invest"""
    def __init__(self, bubble, observer):
        super().__init__(bubble, observer)
        self._value = 10
        self.persuade = 0.5
        self.true_capital = 10

    def update(self):
        super().update() 
        self.bubble.set_text(
            f"Shown capital {to_readable_int(self._value)}$"
        )
        self.bubble.set_fill_level(1 - exp(-1 / 1000 * self._value))

        self.persuade = clamp(self.persuade, 0, 1)
        self.persuade /= 1.1
        # print(f"{self.persuade = }")
        
    def influencedBy(self, parent):
        if (type(parent) == TrueCapitalNode):
            self.true_capital = parent._value
            self._value = self.persuade * self._value + (1 - self.persuade) * self.true_capital

        if (type(parent) == MarketingNode):
            self.persuade = getNewValue(self.persuade, parent._value/500, 1)
            if self.true_capital == 0:
                print("aaaaaaaaaaaa")
            else:
                self._value = getNewValue(self._value, parent._value/200 * self.true_capital, 10*(self.true_capital**2))

        if (type(parent) == PublicDoubtNode):
            self.persuade = getNewValue(self.persuade, parent._value/500, 1)

class MarketNode(BaseNode):
    doc = """Choose wisely where you invest. If the bubble is filled, you can buy.\nLook at the graph.\nExplanations? Become a trader."""
    def __init__(self, bubble, name, observer):
        super().__init__(bubble, observer)
        self._value = 1
        self.max_value = 194
        self.tendance = 1
        self.worker = 2
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
        self._value = clamp(self._value, random.randint(3, 12)/100, random.randint(163, 194)/100)

        self.bubble.set_text(
            f"{self.name} {to_readable_int(marketPriceIncrement(self.nb_clicks))}$ {to_readable_int(self._value)}$ {self.worker:.1f} tendance {round(self.tendance, 2)}"
        )
    
class MarketGroup():
    def __init__(self, markets_nodes):
        self.market_nodes = markets_nodes
        self.parents = []
    
    def addParent(self, node):
        self.parents.append(node)

    def addParents(self, nodes_list):
        for e in nodes_list:
            self.addParent(e)

    def quick_update(self):
        for market_node in self.market_nodes:
            market_node.quick_update()

    def update(self):
        for node in self.parents:
            self.influencedBy(node)

        for market_node in self.market_nodes:
            market_node.update()

    def draw(self, view, inputs, paused):
        for market_node in self.market_nodes:
            if not paused:
                market_node.bubble.update(inputs)
            market_node.bubble.draw(view)

    def draw_docs(self, view):
        pass
    
    def influencedBy(self, parent):
        if type(parent) == PublicDoubtNode:
            for market_node in self.market_nodes:
                market_node.tendance = market_node.tendance*2 - 4*(parent._value - parent.max_value / 2) / parent.max_value

        if type(parent) == EspionageNode:
            if parent.is_click:
                for market_node in self.market_nodes:
                    market_node.worker += 0.5

        if type(parent) == TrueCapitalNode:
            for market_node in self.market_nodes:
                price = marketPriceIncrement(market_node.nb_clicks)
                market_node.bubble.set_fill_level(parent._value / price)
                if market_node.is_click:
                    if price <= parent._value:
                        other_market_nodes = [m for m in self.market_nodes if m.name != market_node.name]
                        market_node.worker += sum([o.worker / 2 for o in other_market_nodes])
                        for o in other_market_nodes:
                            o.worker /= 2


                        market_node.nb_clicks += 1
                        parent._value -= price
                    market_node.is_click = False

    def notify(self, event, notifications):
        pass

class PublicDoubtNode(BaseNode):
    doc = """Public Doubt : if the public loves you, we love you.\nIf Public doubt is a 100%, you're over."""
    def __init__(self, bubble, observer):
        super().__init__(bubble, observer)
        self.max_value = 100
    
    def update(self):
        super().update()
        self._value -= 0.1
        self._value += random.gauss(0, self.volatility/500)
        self._value = clamp(self._value, 0, self.max_value)

        self.bubble.set_text(
            f"Public Doubt {to_readable_int(self._value)}%"
        )
        self.bubble.set_fill_level(self._value / self.max_value)

    def influencedBy(self, parent):
        if type(parent) == MarketingNode:
            self._value = getNewValue(self._value, -parent._value/2, self.max_value)
        
        if type(parent) == InvestorsDoubtNode:
            self._value = getNewValue(self._value, parent._value/25, self.max_value)

        # if type(parent) == EventNode:
        #     for ev in parent.events:
        #         if not ev.alive:
    
    def notify(self, event, notifications):
        if event == EVENT_EVENT_BURST:
            self._value = min(100, self._value + notifications)

class InvestorNode(BaseNode):
    def __init__(self, bubble, observer):
        super().__init__(bubble, observer)
        self.max_value = 100
        # the investors observe for some time, which helps
        # then calculate how much they doubt you, as well as
        # how interested they are
        self.invested = 0
        self.pulled_out = 0
        self.interest = 1
        self.new_join = True
        self.owned_shares = 0

        self.observing_for = random.randint(6, 8)
        self.records = []

    def setObsPeriod(self, val1, val2, keepHistory=0):
        new_obs_period = random.randint(val1, val2) * self.interest
        new_obs_period /= (self.volatility / 5)
        self.observing_for = int(new_obs_period)
        if keepHistory > len(self.records): return
        if keepHistory == 0: self.records = []
        else: self.records = self.records[-keepHistory : -1]

    def record(self, value):
        if len(self.records) > 0:
            newavg = self.records[-1] * len(self.records)
            newavg = (newavg + value) / (len(self.records) + 1)
        else: newavg = value
        self.records.append(newavg)
        # print(str(self._value) + ", " + str(newavg))

    def determine(self):
        # once enough info is given:
        if len(self.records) > self.observing_for:
            res = self.records[-1] - self.records[0] 
            res /= self.records[0]
            # print(str(res) + " & ")
            if abs(res) < 1 / self.volatility:
                self._value *= 1.01; return
            if res < 0:
                self._value *= (1 + abs(res))
                self.interest = max(1, self.interest - 0.05)
                if self._value > 75: self.setObsPeriod(3, 5)
            else:
                if self.observing_for < 7:
                    self.setObsPeriod(6, 8)
                else:
                    last_point = random.randint(0, self.observing_for)
                    self.setObsPeriod(6, 8, keepHistory=last_point)
                self.interest = min(1.5, self.interest + 0.05)
                self._value /= (1 + res)

    def update(self):
        self._value += random.gauss(0, 1) * self.volatility
        self._value -= 0.05
        self._value = clamp(self._value, 1, 100)

    def draw(self): return

    def invest(self, shares): 
        # invest only after observing
        if len(self.records) < self.observing_for or self.invested > 0 \
                                                  or self.interest < 1.1: 
            return 0
        if random.random() * 100 > self._value:
            self.invested = random.random() * (0.8 - shares) / 2.5
            self.invested *= self.interest
            self.invested *= (1 - self._value / 100)
            if self.invested * 100 < 1: self.invested = 0
            self.owned_shares += self.invested
            return self.invested
        return 0

    def pullout(self):
        # pullout if doubt starts to grow
        if len(self.records) < self.observing_for or self.pulled_out > 0 \
                            or (self.interest > 1.4 and self._value < 70):
            return 0
        if random.random() * 100 < self._value:
            self.pulled_out = random.random() * self.owned_shares / 2
            self.pulled_out /= self.interest
            self.pulled_out *= self._value / 100
            if self.pulled_out * 100 < 1: self.pulled_out = 0
            self.owned_shares -= self.pulled_out
            return self.pulled_out
        return 0

class InvestorsDoubtNode(BaseNode):
    doc = """Investor Doubt : investors will fund you. Don't make them leave.\nIf you show consitent growth, they will take interest in you.\nIf Investor doubt is a 100%, you're over."""
    def __init__(self, bubble, observer):
        super().__init__(bubble, observer)
        self.max_value = 100
        # our group of investors
        self.investors = []

    def influencedBy(self, parent):
        if type(parent) == ApparentCapitalNode:
            for investor in self.investors:
                investor.record(parent._value)
                investor.determine()

        if type(parent) == EventNode:
            # self._value = getNewValue()
            pass

    def update(self):
        super().update()

        if len(self.investors) > 0:
            investor_doubt = []
            for investor in self.investors:
                investor.update()
                investor_doubt.append(investor._value)
            self._value = np.mean(investor_doubt)
            self._value = clamp(self._value, 1, 100)

        if len(self.investors) < 10:
            if random.random() * 100 > self._value:
                new_investor = InvestorNode(self.bubble, self.observer)
                self.investors.append(new_investor)

        self.bubble.set_text(
            f"Investors Doubt {to_readable_int(self._value)}%"
        )
        self.bubble.set_fill_level(self._value / self.max_value)

    def invest(self, shares):
        if len(self.investors) <= 0: return 0
        random.shuffle(self.investors)
        return self.investors[0].invest(shares)

    def pullout(self):
        if len(self.investors) <= 0: return 0
        random.shuffle(self.investors)
        return self.investors[0].pullout()

class MarketingNode(BaseNode):
    doc = """Marketing : invest a ton into marketing and your public will love you. And investors will think your very rich.\nYour apparent capital will go up."""
    def __init__(self, bubble, observer):
        super().__init__(bubble, observer)
        self.is_click = False
        self.nb_clicks = 1

    def quick_update(self):
        if self.bubble.clicked():
            self.is_click = True

    def update(self):
        super().update()
        self.bubble.set_text(
            f"Marketing {to_readable_int(priceIncrement(self.nb_clicks))}$ {to_readable_int(self._value)}%"
        )
    
    def influencedBy(self, parent):
        if type(parent) == TrueCapitalNode:
            price = priceIncrement(self.nb_clicks)
            self.bubble.set_fill_level(parent._value / price)
            if self.is_click:
                price = priceIncrement(self.nb_clicks)
                if price <= parent._value:
                    self._value = getNewValue(self._value, 10, 100)
                    self.nb_clicks += 1
                    parent._value -= price
                self.is_click = False

class SecurityNode(BaseNode):
    doc = """Security : diminishes the probability of getting caught doing criminal activities"""
    def __init__(self, bubble, observer):
        super().__init__(bubble, observer)
        self.is_click = False
        self.nb_clicks = 1


    def quick_update(self):
        if self.bubble.clicked():
            self.is_click = True

    def update(self):
        super().update()
        self.bubble.set_text(
            f"Security {to_readable_int(priceIncrement(self.nb_clicks))}$ {to_readable_int(self._value)}%"
        )
    
    def influencedBy(self, parent):
        if type(parent) == TrueCapitalNode:
            price = priceIncrement(self.nb_clicks)
            self.bubble.set_fill_level(parent._value / price)
            if self.is_click:
                price = priceIncrement(self.nb_clicks)
                if price <= parent._value:
                    self._value = getNewValue(self._value, 10, 100)
                    self.nb_clicks += 1
                    parent._value -= price
                self.is_click = False

class EspionageNode(BaseNode):
    doc = """Espionage : this is a criminal activity. Big risk, big reward. It's up to you.\nTry not to trail behind the competition."""
    def __init__(self, bubble, observer):
        super().__init__(bubble, observer)
        self.is_click = False
        self.nb_clicks = 1
        

    def quick_update(self):
        if self.bubble.clicked():
            self.is_click = True

    def update(self):
        super().update()
        self.bubble.set_text(
            f"Espionage {to_readable_int(priceIncrement(self.nb_clicks))}$ {to_readable_int(self._value)}%"
        )
    
    def influencedBy(self, parent):
        if self.is_click:
            if type(parent) == Event:
                parent.createEvent()
            
            if type(parent) == TrueCapitalNode:
                price = priceIncrement(self.nb_clicks)
                self.bubble.set_fill_level(parent._value / price)
                if price <= parent._value:
                    self._value = getNewValue(self._value, 10, 100)
                    self.nb_clicks += 1
                    parent._value -= price
            self.is_click = False

class EventNode(BaseNode):
    def __init__(self, bubble, observer):
        super().__init__(bubble, observer)
        self.events = []
        self.bubble.set_fill_level(0)
    
    def update(self):
        super().update()
        for e in self.events:
            e.update()
        self.events = [e for e in self.events if e.alive]

    def influencedBy(self, parent):
        # TODO
        # if type(parent) == EspionageNode:
            # createEvent
        pass

    def createEvent(self):
        self.events.append(Event(5, 0.4, 0.8, self.observer))

class Event():
    def __init__(self, TTL, dbt, risk, observer):
        self.time_to_live = TTL
        self.observer = observer
        
        # the doubt provided if the event is discovered
        self.doubt = dbt
        
        # the probability of the event to burst
        self.risk = risk
        # determines if the event is live or not
        self.alive = True
    
    def burst(self):
        self.alive = False
        self.observer.notify(EVENT_EVENT_BURST, self.doubt)
        

    def update(self):
        self.time_to_live -= 1
        if self.time_to_live == 0:
            self.alive = False
        elif random.random() < self.risk:
            self.burst()
        else:
            self.risk /= 2
                
        self.bubble.set_text(
            f"Event {to_readable_int(self._value)}$"
        )

