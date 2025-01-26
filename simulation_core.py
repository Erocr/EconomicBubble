import random
import numpy as np
from misc import *
from observer import *
from math import exp
from vec import *
from actions import Actions

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

    def mulValue(self, val):
        self._value *= val

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

    def incrementCapital(self, increment):
        self._value += increment

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
        self.persuade /= 1.01
        self._value = max(self._value, self.true_capital + random.randint(12, 102))
        
    def influencedBy(self, parent):
        if (type(parent) == TrueCapitalNode):
            if (parent._value - self.true_capital > 0):
                self._value += 10 * self.persuade * (parent._value - self.true_capital)
            else:
                self._value = (5*self.persuade * self._value + parent._value)/(1 + 5*self.persuade)

            self.true_capital = parent._value

        if (type(parent) == MarketingNode):
            self.persuade = getNewValue(self.persuade, parent._value/500, 1)
            self._value = getNewValue(self._value, parent._value/200 * self.true_capital, 10*(self.true_capital**2))

        if (type(parent) == PublicDoubtNode):
            self.persuade = getNewValue(self.persuade, parent._value/500, 1)
    
    def incrementCapital(self, increment):
        self._value += increment
    
    def incrementPersuasion(self, increment): # must be positive, between 0 and 1
        self.persuade = getNewValue(self.persuade, increment, 1)
        self.persuade = max(self.persuade, 0)

class MarketNode(BaseNode):
    doc = """Choose wisely where you invest. If the bubble is filled, you can buy.\nLook at the graph.\nExplanations? Become a trader."""
    def __init__(self, bubble, observer):
        super().__init__(bubble, observer)
        self._value = 1
        self.max_value = 194
        self.min_value = 3
        self.tendance = 1
        self.worker = 2
        self.is_click = False
        self.nb_clicks = 1

    def quick_update(self):
        self._value += random.random()/4_000
        self._value += random.gauss(self.tendance, self.volatility*10)/2_000
        self.tendance /= 1.1
        if self.bubble.clicked():
            self.is_click = True

    def update(self):
        self._value = clamp(self._value, random.randint(self.min_value, self.min_value)/100, random.randint(self.max_value - 10, self.max_value)/100)

    def mulValue(self, val):
        self._value *= val
    
    def increment_max_price(self, increment):
        self.max_value += increment
    
    def increment_min_price(self, increment):
        self.min_value += increment
    
    def incrementTendance(self, increment):
        self.tendance += increment

    
class SoapNode(MarketNode):
    def __init__(self, bubble, observer):
        super().__init__(bubble, observer)
    def update(self):
        super().update()
        self.bubble.set_text(
            f"Soap: {to_readable_int(marketPriceIncrement(self.nb_clicks))}$ {to_readable_int(self._value)}$ {self.worker:.1f} tendance {round(self.tendance, 2)}"
        )
class BeerNode(MarketNode):
    def __init__(self, bubble, observer):
        super().__init__(bubble, observer)
    def update(self):
        super().update()
        self.bubble.set_text(
            f"Beer: {to_readable_int(marketPriceIncrement(self.nb_clicks))}$ {to_readable_int(self._value)}$ {self.worker:.1f} tendance {round(self.tendance, 2)}"
        )
class WrapNode(MarketNode):
    def __init__(self, bubble, observer):
        super().__init__(bubble, observer)
    def update(self):
        super().update()
        self.bubble.set_text(
            f"Wrap: {to_readable_int(marketPriceIncrement(self.nb_clicks))}$ {to_readable_int(self._value)}$ {self.worker:.1f} tendance {round(self.tendance, 2)}"
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
            market_node.draw(view, inputs, paused)

    def draw_docs(self, view):
        for node in self.market_nodes:
            node.draw_docs(view)
    
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
        self._value /= 1.05
        self._value -= 0.08
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
    
    def incrementDoubt(self, increment):
        self._value = getNewValue(self._value, increment, 100)
        self._value = max(self._value, 0)
    
    def incrementVolatility(self, increment):
        self.volatility = getNewValue(self.volatility, increment, 15)

class InvestorNode(BaseNode):
    def __init__(self, bubble, observer):
        super().__init__(bubble, observer)
        self.max_value = 100
        # the investors observe for some time, which helps
        # then calculate how much they doubt you, as well as
        # how interested they are
        self.pulled_out = 0
        self.interest = 1
        self.true_capital = 10
        
        self.owned_shares = 0
        self.invested_money = 0
        self.bottom_line = 0   # an investor becomes disturbed if your
                               # shown capital passes the bottom line
        self.disturbed = False # a disturbed investor will immediately
                               # pull everything away.

        self.observing_for = random.randint(6, 8)
        self.records = []
        self.newest_record = 0

    def setObsPeriod(self, val1, val2, keepHistory=False):
        new_obs_period = random.randint(val1, val2) * self.interest
        new_obs_period /= (self.volatility / 5)
        self.observing_for = int(new_obs_period)
        if not keepHistory: self.records = []
        else: self.observing_for += len(self.records)

    def record(self, value):
        if len(self.records) > 0:
            newavg = self.records[-1] * len(self.records)
            newavg = (newavg  + value) / (len(self.records) + 1)
        else: newavg = value
        self.records.append(newavg)
        self.newest_record = value
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
                    self.setObsPeriod(6, 8, keepHistory=True)
                self.interest = min(1.5, self.interest + 0.05)
                self._value /= (1 + res)

    def update(self):
        self._value += random.gauss(0, 1) * self.volatility
        self._value -= 0.05
        self._value = clamp(self._value, 1, 100)
        self.bottom_line = self.invested_money * self.volatility
        if self.newest_record * self.interest < self.bottom_line:
            self.disturbed = True

    def draw(self): return

    def invest(self, shares): 
        # invest only after observing
        if len(self.records) < self.observing_for or self.invested > 0 \
                                                  or self.interest < 1.1: 
            return 0
        if random.random() * 100 > self._value:
            invested = random.random() * (0.8 - shares) / 2.5
            invested *= self.interest
            invested *= (1 - self._value / 100)
            if invested * 100 < 1: invested = 0
            self.owned_shares += invested
            self.observer.notify(EVENT_INVESTED, [self, invested])
            return invested
        return 0

    def pullout(self):
        # pullout if doubt starts to grow
        if len(self.records) < self.observing_for or self.pulled_out > 0 \
                            or (self.interest > 1.4 and self._value < 70):
            return 0
        if self.disturbed:
            self.pulled_out = self.invested_money / self.true_capital
            self.pulled_out = clamp(self.pulled_out, 0, 1)
            self.owned_shares = 0
            return self.pulled_out
            
        if random.random() * 100 < self._value:
            if self.owned_shares * 100 < 5:
                self.pulled_out = self.owned_shares
                self.owned_shares = 0
            else:
                self.pulled_out = random.random() * self.shares / 2
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
                if investor.owned_shares == 0:
                    self.investors.remove(investor)
                    continue
                investor.record(parent._value)
                investor.determine()

        if type(parent) == EventNode:
            # self._value = getNewValue()
            pass

    def mulValue(self, val):
        for investor in self.investors:
            investor._value *= val

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
    doc = """Marketing : invest a ton into marketing and your public will love you. And investors will think your rich.\nYour shown capital will go up."""
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
    
    def present_choices(self):
        actions = Actions(TrueCapitalNode, WrapNode, SoapNode, BeerNode, PublicDoubtNode, InvestorsDoubtNode)
        first_choice, second_choice = random.sample(list(actions.actions.keys()), 2)

        self.observer.notify(EVENT_TRIGGER_CHOICES, [first_choice, second_choice])

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
                self.present_choices()
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
            f"Event: Risk to burst {to_readable_int(self._risk)}%"
        )

class Crime(Event):
    def burst(self):
        super().burst(self)
        self.observer.notify(EVENT_CRIME_FOUND, self.risk)


# '''List of actions
#     Each element is a list with :
#      - a string to be shown on screen
#      - a dictionnary with
#         - keys = id of the variable to change (0 for soap, 1 for beer, 2 for wrap)
#         - float influences
#         TODO'''

#     # string, (ressource type, factor)
# actions = {
#     "You create a viral social media campaign featuring your soap products being used as impromptu bubble wrap replacements in a humorous DIY video":
#     {TrueCapitalNode : [(TrueCapitalNode.mulValue, 1.05)], 
#      WrapNode : [(WrapNode.mulValue, 1.03)], 
#      SoapNode : [(SoapNode.mulValue, 1.02)],
#      PublicDoubtNode : [(PublicDoubtNode.mulValue, 0.9)]
#      },
#     #(Effect: TrueCapitalNode + 5%, WrapNode + 3%, SoapNode + 2%, PublicDoubtNode - 10%)
#     "You host an 'open house' where you let customers play with bubble wrap for hours on end, causing a massive delay in production and sales":
#     {WrapNode : [(WrapNode.mulValue, 1.05)],
#      PublicDoubtNode : [(PublicDoubtNode.mulValue, 1.10)],
#      SoapNode : [(PublicDoubtNode.mulValue, 1.10)],
#      },
#     #(Effect: WrapNode + 5%, PublicDoubtNode - 10%, SoapNode - 1%, BeerNode - 3%, InvestorsDoubtNode + 3%)"
#     "You decide to rebrand your soap company as 'Bubble Wrap Soaps' just to see how many investors take it seriously":
#     {InvestorsDoubtNode : [(InvestorsDoubtNode.mulValue, 1.08)],
#      TrueCapitalNode : [(TrueCapitalNode.mulValue, 0.96)],
#      WrapNode : [(WrapNode.mulValue, 1.06)],
#      SoapNode : [(SoapNode.mulValue, 0.97)]
#      },
#     # (Effect: InvestorsDoubtNode + 8%, TrueCapitalNode - 4%, WrapNode + 6%, SoapNode - 3%)
#     "You buy an entire warehouse full of bubble wrap to use as office decor and end up bankrupting the company":
#     {WrapNode : [(WrapNode.mulValue, 1.08)],
#      InvestorsDoubtNode : [(InvestorsDoubtNode.mulValue, 1.1)],
#      TrueCapitalNode : [TrueCapitalNode.mulValue, 0.88]
#      },
#     #(Effect: WrapNode + 8%, InvestorsDoubtNode + 10%, TrueCapitalNode - 12%)"
#     "You accidentally order 1000 cases of beer for a party that only 10 people will attend, resulting in a massive inventory glut":
#     {BeerNode : [(BeerNode.mulValue, 0.95)],
#      TrueCapitalNode : [(TrueCapitalNode.mulValue, 0.9)],
#      PublicDoubtNode : [(PublicDoubtNode.mulValue, 1.05)],
#      },
#     #(Effect: BeerNode - 5%, TrueCapitalNode - 2%, PublicDoubtNode + 5%)",
#     "You start selling soap-shaped whoopee cushions as a 'novelty item' to make some extra cash, but they're actually a major distraction from your main products":
#     {SoapNode : [(SoapNode.mulValue, 1.1)],
#      WrapNode : [(WrapNode.mulValue, 0.96)],
#      BeerNode : [(BeerNode.mulValue, 0.96)],
#      TrueCapitalNode : [(TrueCapitalNode.mulValue, 1.04)],
#      PublicDoubtNode : [(PublicDoubtNode.mulValue, 0.98)]
#     },
#     #(Effect: SoapNode + 10%, WrapNode - 4%, BeerNode - 4%, TrueCapitalNode + 4%, PublicDoubtNode - 2%)",
#     "You try to create a viral challenge by making people attempt to wrap themselves in bubble wrap, but it ends up being a mess":
#     {WrapNode : [(WrapNode.mulValue, 1.4)],
#      InvestorsDoubtNode : [(InvestorsDoubtNode.mulValue, 0.98)],
#      TrueCapitalNode : [(TrueCapitalNode.mulValue, 0.9)],
#      SoapNode : [(SoapNode.mulValue, 0.97)],
#     },
#     #(Effect: WrapNode + 4%, InvestorsDoubtNode - 2%, TrueCapitalNode - 1%, SoapNode - 3%)
#     "You partner with a rival company to co-create a beer-infused soap that's supposed to be the 'next big thing', but it's actually just gross":
#     {BeerNode : [(BeerNode.mulValue, 0.94)],
#      SoapNode : [(SoapNode.mulValue, 0.95)],
#      WrapNode : [(WrapNode.mulValue, 0.98)],
#      TrueCapitalNode : [(TrueCapitalNode.mulValue, 0.96)]
#     },
#     #(Effect: BeerNode - 6%, SoapNode - 5%, WrapNode - 2%, TrueCapitalNode - 4%)
#     "You decide to replace all your employees with automated bubble wrap dispensers, but they keep getting jammed and causing chaos":
#     {InvestorsDoubtNode : [(InvestorsDoubtNode.mulValue, 1.08)],
#      PublicDoubtNode : [(PublicDoubtNode.mulValue, 1.03)],
#      TrueCapitalNode : [(TrueCapitalNode.mulValue, 0.94)],
#      WrapNode : [(WrapNode.mulValue, 0.95)]
#     },
    
#     "You host a 'soap-making' workshop for kids where they get to create their own bubble wrap soap, but it's actually just a bunch of sticky messes":
#     {SoapNode: [(SoapNode.mulValue, 1.02)],
#      WrapNode: [(WrapNode.mulValue, 1.01)],
#      InvestorsDoubtNode: [(InvestorsDoubtNode.mulValue, 0.99)],
#      TrueCapitalNode: [(TrueCapitalNode.mulValue, 0.99)]},
#     # (Effect: SoapNode + 2%, WrapNode + 1%, InvestorsDoubtNode - 1%, TrueCapitalNode - 1%)
    
#     "You invest in a beer brewery that specializes in creating beers with extremely unusual ingredients, like seaweed and garlic":
#     {BeerNode: [(BeerNode.mulValue, 1.04)],
#      PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.98)],
#      TrueCapitalNode: [(TrueCapitalNode.mulValue, 0.97)],
#      InvestorsDoubtNode: [(InvestorsDoubtNode.mulValue, 0.99)]},
#     # (Effect: BeerNode + 4%, PublicDoubtNode - 2%, TrueCapitalNode - 3%, InvestorsDoubtNode - 1%)

#     "You create an 'anti-bubble wrap' movement where people try to avoid bubble wrap at all costs, but it's actually just a bunch of hipsters being hipsters":
#     {WrapNode: [(WrapNode.mulValue, 0.94)],
#      SoapNode: [(SoapNode.mulValue, 0.96)],
#      TrueCapitalNode: [(TrueCapitalNode.mulValue, 0.98)],
#      PublicDoubtNode: [(PublicDoubtNode.mulValue, 1.03)]},
#     # (Effect: WrapNode - 6%, SoapNode - 4%, TrueCapitalNode - 2%, PublicDoubtNode + 3%)

#     "You start selling 'soap-scented' beer that's supposed to be the perfect pairing for your soap products, but it's actually just a cheap gimmick":
#     {BeerNode: [(BeerNode.mulValue, 1.10)],
#      SoapNode: [(SoapNode.mulValue, 1.10)],
#      WrapNode: [(WrapNode.mulValue, 0.98)],
#      TrueCapitalNode: [(TrueCapitalNode.mulValue, 0.98)]},
#     # (Effect: BeerNode + 3%, SoapNode - 1%, WrapNode - 2%, TrueCapitalNode - 2%)

#     "You try to create a new market trend by selling bubble wrap as a luxury item, but people are like 'meh, I can just buy regular bubble wrap for cheaper'":
#     {WrapNode: [(WrapNode.mulValue, 0.87)],
#      TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.03)],
#      PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.94)]},
#     # (Effect: WrapNode + 2%, SoapNode - 3%, TrueCapitalNode - 1%, PublicDoubtNode - 1%)

#     "You partner with a social media influencer to promote your soap products, but they're actually just posting pictures of themselves wrapped in bubble wrap":
#     {SoapNode: [(SoapNode.mulValue, 1.04)],
#      WrapNode: [(WrapNode.mulValue, 1.03)],
#      InvestorsDoubtNode: [(InvestorsDoubtNode.mulValue, 0.98)],
#      TrueCapitalNode: [(TrueCapitalNode.mulValue, 0.98)]},
#     # (Effect: SoapNode + 4%, WrapNode + 3%, InvestorsDoubtNode - 2%, TrueCapitalNode - 2%)

#     "You invest in a new manufacturing process that replaces human labor with automated machines, but it's causing all the employees to get laid off and start a union":
#     {InvestorsDoubtNode: [(InvestorsDoubtNode.mulValue, 1.08)],
#      PublicDoubtNode: [(PublicDoubtNode.mulValue, 1.05)],
#      TrueCapitalNode: [(TrueCapitalNode.mulValue, 0.90)],
#      WrapNode: [(WrapNode.mulValue, 0.95)]},
#     # (Effect: InvestorsDoubtNode + 8%, PublicDoubtNode + 5%, TrueCapitalNode - 10%, WrapNode - 5%)

#     "You create a new line of 'craft' soaps that use only rare and expensive ingredients, but they're actually just regular soap with some fancy labels":
#     {SoapNode: [(SoapNode.mulValue, 1.03)],
#      WrapNode: [(WrapNode.mulValue, 0.99)],
#      TrueCapitalNode: [(TrueCapitalNode.mulValue, 0.98)],
#      PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.99)]},
#     # (Effect: SoapNode + 3%, WrapNode - 1%, TrueCapitalNode - 2%, PublicDoubtNode - 1%)

#     "You try to create a viral challenge by making people compete in bubble wrap unwrapping contests, but it's actually just a bunch of old people complaining about the state of society":
#     {WrapNode: [(WrapNode.mulValue, 1.04)],
#      InvestorsDoubtNode: [(InvestorsDoubtNode.mulValue, 0.97)],
#      TrueCapitalNode: [(TrueCapitalNode.mulValue, 0.98)],
#      PublicDoubtNode: [(PublicDoubtNode.mulValue, 1.05)]},
#     # (Effect: WrapNode + 4%, InvestorsDoubtNode - 3%, TrueCapitalNode - 2%, PublicDoubtNode + 5%)

#     "You start selling 'anti-bubble wrap' merchandise that's supposed to be ironic, but it's actually just regular clothes with a weird slogan on them":
#     {SoapNode: [(SoapNode.mulValue, 0.99)],
#      WrapNode: [(WrapNode.mulValue, 0.98)],
#      TrueCapitalNode: [(TrueCapitalNode.mulValue, 0.99)],
#      PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.98)]},
#     # (Effect: SoapNode - 1%, WrapNode - 2%, TrueCapitalNode - 1%, PublicDoubtNode - 2%)

    
#     ## Illegal
    
#     "You partner with a notorious drug lord to produce and distribute a new designer soap that contains marijuana, creating a new business, but maybe not a good one.": {
#         TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.1)],
#         SoapNode: [(SoapNode.mulValue, 0.7)],
#         WrapNode: [(WrapNode.mulValue, 1.05)],
#         BeerNode: [(BeerNode.mulValue, 1.03)],
#         PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.8)],
#     },
#     "You team up with a ruthless gun runner to smuggle soap into the country by hiding it in beer barrels, causing a surge in soap sales and confusion in the beer market.": {
#         TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.15)],
#         SoapNode: [(SoapNode.mulValue, 1.25)],
#         WrapNode: [(WrapNode.mulValue, 1.05)],
#         BeerNode: [(BeerNode.mulValue, 0.8)],
#         PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.9)],
#     },
#     "You align with a powerful mafia boss to corner the bubble wrap market by threatening rival companies, forcing them out of business and leaving you in control of the entire industry.": {
#         TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.2)],
#         WrapNode: [(WrapNode.mulValue, 1.5)],
#         SoapNode: [(SoapNode.mulValue, 1.05)],
#         BeerNode: [(BeerNode.mulValue, 1.05)],
#         PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.75)],
#     },
#     "You hire a mercenary squad to raid rival soap companies, stealing their secret formulas and using them to dominate the market while causing chaos in the beer industry.": {
#         TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.3)],
#         SoapNode: [(SoapNode.mulValue, 1.5)],
#         WrapNode: [(WrapNode.mulValue, 1.05)],
#         BeerNode: [(BeerNode.mulValue, 0.75)],
#         PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.85)],
#     },
#     "You collude with corrupt officials to rig soap market prices, artificially inflating your profits while hurting small businesses and causing investor doubt.": {
#         TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.1)],
#         SoapNode: [(SoapNode.mulValue, 1.2)],
#         WrapNode: [(WrapNode.mulValue, 1.03)],
#         BeerNode: [(BeerNode.mulValue, 1.05)],
#         PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.9)],
#     },
#     "You leverage connections with organized crime to monopolize the beer market by bribing officials, extorting competitors, and infiltrating distribution networks.": {
#         TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.25)],
#         SoapNode: [(SoapNode.mulValue, 1.05)],
#         WrapNode: [(WrapNode.mulValue, 1.03)],
#         BeerNode: [(BeerNode.mulValue, 0.7)],
#         PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.8)],
#     },
#     "You partner with a dangerous cartel to produce a new designer soap that's highly addictive and illegal, flooding the market and causing chaos in law enforcement agencies.": {
#         TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.15)],
#         SoapNode: [(SoapNode.mulValue, 0.75)],
#         WrapNode: [(WrapNode.mulValue, 1.05)],
#         BeerNode: [(BeerNode.mulValue, 1.07)],
#         PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.9)],
#     },
#     "You hire a team of cybercriminals to hack into rival soap companies' systems, stealing intellectual property and using it to dominate the market while causing chaos in the tech industry.": {
#         TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.2)],
#         SoapNode: [(SoapNode.mulValue, 1.3)],
#         WrapNode: [(WrapNode.mulValue, 1.05)],
#         BeerNode: [(BeerNode.mulValue, 1.1)],
#         PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.85)],
#     },
#     "You start what you thought was a great campaign, artificially inflating your profits but causing public doubt about the integrity of the industry.": {
#         TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.1)],
#         SoapNode: [(SoapNode.mulValue, 1.2)],
#         WrapNode: [(WrapNode.mulValue, 1.03)],
#         BeerNode: [(BeerNode.mulValue, 1.05)],
#         PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.85)],
#     },
#     "You pay off rival soap companies to sabotage their production facilities, allowing you to monopolize the market while causing chaos in the beer industry.": {
#         TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.3)],
#         SoapNode: [(SoapNode.mulValue, 1.5)],
#         WrapNode: [(WrapNode.mulValue, 1.05)],
#         BeerNode: [(BeerNode.mulValue, 0.75)],
#         PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.85)],
#     },
#     "You work with a dangerous smuggling ring to import massive amounts of illegal soap into the country, flooding the market and causing chaos in law enforcement agencies.": {
#         TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.2)],
#         SoapNode: [(SoapNode.mulValue, 0.8)],
#         WrapNode: [(WrapNode.mulValue, 1.3)],
#         BeerNode: [(BeerNode.mulValue, 1.05)],
#         PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.85)],
#     },
#     "You bribe government officials to approve a new type of transparent soap that is insanely dangerous, causing thousands to die before it's removed.": {
#         TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.2)],
#         SoapNode: [(SoapNode.mulValue, 1.2)],
#         PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.75)],
#     },
#     "You form an alliance with a ruthless gang to monopolize the bubble wrap market by raiding competitors and spreading misinformation about product safety, causing investor doubt.": {
#         TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.2)],
#         SoapNode: [(SoapNode.mulValue, 1.05)],
#         WrapNode: [(WrapNode.mulValue, 0.6)],
#         BeerNode: [(BeerNode.mulValue, 1.07)],
#         PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.8)],
#     },
#     "You forge alliances with international crime syndicates to monopolize the soap market by sabotaging competitors and spreading misinformation about product safety, causing investor doubt.": {
#         TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.25)],
#         SoapNode: [(SoapNode.mulValue, 0.6)],
#         WrapNode: [(WrapNode.mulValue, 1.05)],
#         BeerNode: [(BeerNode.mulValue, 1.1)],
#         PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.7)],
#     },
#     "You become the head of an underground gun-running organization that also controls the distribution of a highly potent and addictive strain of craft beer, causing chaos and rising demand.": {
#         TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.25)],
#         BeerNode: [(BeerNode.mulValue, 1.3)],
#         PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.8)],
#     },
#     "You form an alliance with international espionage agencies to monopolize the illicit arms trade while secretly producing a top-quality microbrew, creating a profitable black market.": {
#         TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.3)],
#         BeerNode: [(BeerNode.mulValue, 1.4)],
#         PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.75)],
#     },
#     "You infiltrate rival gangs and governments by using your impressive beer-making skills as leverage, ultimately controlling both the illicit arms trade and the craft beer market.": {
#         TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.35)],
#         BeerNode: [(BeerNode.mulValue, 1.5)],
#         PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.7)],
#     },
#     "You create a powerful spy organization that specializes in using high-quality beer as a means of communication and control, simultaneously monopolizing both the espionage industry and the beer market.": {
#         TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.4)],
#         BeerNode: [(BeerNode.mulValue, 1.5)],
#         PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.65)],
#     },
#     "You leverage your expertise in crafting exotic beers to gain influence within organized crime syndicates, using their resources to establish a vast network of arms dealers and spies.": {
#         TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.45)],
#         BeerNode: [(BeerNode.mulValue, 1.4)],
#         PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.6)],
#     },
#     "You infiltrate the highest levels of government by producing an addictive strain of beer that only top officials have access to, using their addiction as leverage over both the arms trade and espionage markets.": {
#         TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.5)],
#         BeerNode: [(BeerNode.mulValue, 1.3)],
#         PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.55)],
#     },
#     "You form a secret society of elite spies and brewers who control both the international arms market and the lucrative craft beer industry, spreading misinformation and chaos to maintain their power.": {
#         TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.55)],
#         BeerNode: [(BeerNode.mulValue, 1.5)],
#         PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.5)],
#     },
#     "You use your skill in brewing to forge alliances with rival gun runners and intelligence agencies, using the allure of your beer to gain control over both the illegal arms trade and espionage markets.": {
#         TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.6)],
#         BeerNode: [(BeerNode.mulValue, 1.6)],
#         PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.45)],
#     },
# }
