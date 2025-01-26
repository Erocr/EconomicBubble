import random
from misc import *
from observer import *
from math import exp, log
from vec import *
from actions import Actions

def getNewValue(value, bonus, max_value):
    clamped_bonus = clamp(bonus, -max_value, max_value)
    return value + clamped_bonus - value * abs(clamped_bonus) / max_value

def priceIncrement(n: int):
    return n**3

def marketPriceIncrement(n: int):
    return 50*n*log(n) + 15

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
        if event == EVENT_APPLY_FUNC_NODE:
            if type(self) in notifications:
                for l in notifications[type(self)]:
                    l[0](self, *l[1:])


class TrueCapitalNode(BaseNode):
    doc = """Your True Capital, what you truly have, the money you can actually spend.\nNobody knows it. It's your darkest secret."""
    def __init__(self, bubble, observer):
        super().__init__(bubble, observer)
        self._value = 5000
        self.shares = 0 # Ratio of investment, between 0 and 1
        self.bills = 0
        self.percentage_bills = 0
    
    def update(self):
        super().update()
        self.bubble.set_text(
            f"True capital {to_readable_int(self._value)}$"
        )

        if self._value < 100:
            self.bubble.color_border = (255, 0, 0)
            self.observer.notify(EVENT_PLAY_CRITICAL, None)
        else:
            self.bubble.color_border = (108, 104, 101)
            if self._value > 130:
                self.observer.notify(EVENT_PLAY_NORMAL, None)
        self.bubble.set_fill_level(1-exp(-1/100000*self._value))
        self.bills += 0.5
        self.percentage_bills = getNewValue(self.percentage_bills, 0.01, 2)
        self._value -= self.bills


    def influencedBy(self, parent):
        if type(parent) in [SoapNode, BeerNode, WrapNode]:
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
        self._value = 5000
        self.persuade = 0.5
        self.true_capital = 10

    def update(self):
        super().update() 
        self.bubble.set_text(
            f"Shown capital {to_readable_int(self._value)}$"
        )
        self.bubble.set_fill_level(1 - exp(-1 / 100000 * self._value))

        self.persuade = clamp(self.persuade, 0, 1)
        self.persuade /= 1.01
        self._value = max(self._value, self.true_capital + random.randint(12, 102))
        
    def influencedBy(self, parent):
        if (type(parent) == TrueCapitalNode):
            if (parent._value - self.true_capital > 0):
                self._value += 4 * self.persuade * (parent._value - self.true_capital)
            else:
                self._value = (5*self.persuade * self._value + parent._value)/(1 + 5*self.persuade)
            
            self._value = self.persuade * self._value + (1-self.persuade) * parent._value

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
        self.min_value = -3
        self.tendance = 1
        self.worker = 2
        self.is_click = False
        self.nb_clicks = 1

    def quick_update(self):
        self._value += random.random()/3_300
        self._value += random.gauss(self.tendance, self.volatility*10)/2_000
        if self.tendance < 0:
            self.tendance /= 1.08
        else:
            self.tendance /= 1.1

        if self.bubble.clicked():
            self.is_click = True

    def update(self):
        if random.random() < 0.2:
            self.max_value += 100
            self.min_value -= 100
        if random.random() < 0.1:
            self.max_value *= 1.03
            self.max_value = round(self.max_value)
            self.min_value *= 1.03
            self.min_value = round(self.min_value)

        self._value = clamp(self._value, random.randint(self.min_value, self.min_value + 10)/100, random.randint(self.max_value-10, self.max_value)/100)

    def mulValue(self, val):
        self._value *= val
    
    def increment_max_price(self, increment):
        self.max_value += increment
        self.max_value = round(self.max_value)
    
    def increment_min_price(self, increment):
        self.min_value += increment
        self.min_value = round(self.min_value)
    
    def incrementTendance(self, increment):
        self.tendance += increment

    
class SoapNode(MarketNode):
    def __init__(self, bubble, observer):
        super().__init__(bubble, observer)
    def update(self):
        super().update()
        self.bubble.set_text(
            f"Soap: {to_readable_int(marketPriceIncrement(self.nb_clicks))}$ {self.worker:.1f}"
        )
class BeerNode(MarketNode):
    def __init__(self, bubble, observer):
        super().__init__(bubble, observer)
    def update(self):
        super().update()
        self.bubble.set_text(
            f"Beer: {to_readable_int(marketPriceIncrement(self.nb_clicks))}$ {self.worker:.1f}"
        )
class WrapNode(MarketNode):
    def __init__(self, bubble, observer):
        super().__init__(bubble, observer)
    def update(self):
        super().update()
        self.bubble.set_text(
            f"Wrap: {to_readable_int(marketPriceIncrement(self.nb_clicks))}$ {self.worker:.1f}"
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
                    market_node.worker += 1

        if type(parent) == TrueCapitalNode:
            for market_node in self.market_nodes:
                price = marketPriceIncrement(market_node.nb_clicks)
                market_node.bubble.set_fill_level(parent._value / price)
                if market_node.is_click:
                    if price <= parent._value:
                        other_market_nodes = [m for m in self.market_nodes if type(m) != type(market_node)]
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
        self._value /= 1.01
        self._value -= 0.05
        self._value += random.gauss(0, self.volatility/5)
        self._value = clamp(self._value, 0, self.max_value)
        self.bubble.set_text(
            f"Public Doubt {to_readable_int(self._value)}%"
        )
        self.bubble.set_fill_level(self._value / self.max_value)

        if self._value > 90:
            self.observer.notify(EVENT_PLAY_CRITICAL, None)
        elif self._value < 80:
            self.observer.notify(EVENT_PLAY_NORMAL, None)

    def influencedBy(self, parent):
        if type(parent) == MarketingNode:
            self._value = getNewValue(self._value, -parent._value/2, self.max_value)
        
        if type(parent) == InvestorsDoubtNode:
            self._value = getNewValue(self._value, parent._value/25, self.max_value)


        if type(parent) == EspionageNode:
            self._value = getNewValue(self._value, parent._value/75, self.max_value)

        # if type(parent) == EventNode:
        #     for ev in parent.events:
        #         if not ev.alive:
    
    # def notify(self, event, notifications):
    #     if event == EVENT_EVENT_BURST:
    #         self._value = min(100, self._value + notifications)
    
    def incrementDoubt(self, increment):
        self._value = getNewValue(self._value, increment, 100)
        self._value = max(self._value, 1)
    
    def incrementVolatility(self, increment):
        self.volatility = getNewValue(self.volatility, increment, 15)

class InvestorNode(BaseNode):
    def __init__(self, bubble, observer):
        super().__init__(bubble, observer)
        self.max_value = 100
        # the investors observe for some time, which helps
        # then calculate how much they doubt you, as well as
        # how interested they are
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
                self._value *= 1.1; return
            if res < 0:
                self._value *= (1 + abs(res)) * self.volatility / 5
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
            self._value *= self.volatility

    def draw(self): return

    def invest(self, shares): 
        # invest only after observing
        if len(self.records) < self.observing_for or self.interest < 1.1: 
            return 0
        if random.random() * 100 > self._value:
            invested = random.random() * (0.8 - shares) / 2.5
            invested *= self.interest
            invested *= (1 - self._value / 100)
            if invested * 100 < 2: invested = 0
            self.owned_shares += invested
            if invested > 0:
                self.observer.notify(EVENT_INVESTED, [self, invested])
            return invested
        return 0

    def pullout(self):
        # pullout if doubt starts to grow
        if len(self.records) < self.observing_for or \
                            (self.interest > 1.4 and self._value < 70):
            return 0
        if self.disturbed:
            pulled_out = self.invested_money / self.true_capital
            pulled_out = clamp(pulled_out, 0, 1)
            self.observer.notify(EVENT_PULLED_OUT, [self, pulled_out])
            self.owned_shares = 0
            return pulled_out
            
        if random.random() * 100 < self._value:
            if self.owned_shares * 100 < 5:
                pulled_out = self.owned_shares
                self.owned_shares = 0
            else:
                pulled_out = random.random() * self.shares / 2
                pulled_out /= self.interest
                pulled_out *= self._value / 100
                if pulled_out * 100 < 2: pulled_out = 0
                self.owned_shares -= pulled_out
            if pulled_out > 0:
                self.observer.notify(EVENT_PULLED_OUT, [self, pulled_out])
            return pulled_out
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
            self._value = sum(investor_doubt) / len(investor_doubt)
            # self._value = np.mean(investor_doubt)
            self._value = clamp(self._value, 1, 100)
        if self._value > 90:
            self.observer.notify(EVENT_PLAY_CRITICAL, None)
        elif self._value < 80:
            self.observer.notify(EVENT_PLAY_NORMAL, None)

        if len(self.investors) < 10:
            #print(str(len(self.investors)) + "@")
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
        pullout = self.investors[0].pullout()
        if self.investors[0].owned_shares == 0:
            self.investors.pop()
        return pullout

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
        actions = Actions(TrueCapitalNode, WrapNode, SoapNode, BeerNode, PublicDoubtNode, InvestorsDoubtNode, SecurityNode)
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
        self.defense_team = 0
        self.check_answer = 0

    def quick_update(self):
        if self.bubble.clicked():
            self.is_click = True
    
    def add_defense_team(self, val):
        self.defense_team += 1

    def right_answer(self, val):
        self.observer.notify(EVENT_WRONG_ANSWER, 0)

    def wrong_answer(self, val):
        self.observer.notify(EVENT_RIGHT_ANSWER, 0)

    def monitor(self, val):
        #print("Not Yet Implemented")
        string = "Let's see how successful the surveillance was! What share do you think your biggest investor holds? \n"
        right_answer = self.check_answer
        wrong_answer = random.random() * 0.8
        self.observer.notify(EVENT_REQUEST_QUESTION, [string, right_answer, wrong_answer])

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
                self.observer.notify(EVENT_TRIGGER_CHOICES, ["Surveillance", "Legal Defense"])
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

    def present_choices(self):
        actions = Actions(TrueCapitalNode, WrapNode, SoapNode, BeerNode, PublicDoubtNode, InvestorsDoubtNode, SecurityNode)
        first_choice, second_choice = random.sample(list(actions.illegal.keys()), 2)

        self.observer.notify(EVENT_TRIGGER_CHOICES, [first_choice, second_choice])

    def influencedBy(self, parent):
        if type(parent) == EventNode: # = Crime
            if self.is_click:
                parent.createEvent()
        
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
        self.events.append(Event(5, 10, 0.6, self.observer))

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
            self.risk = max(self.risk - 0.1, 0)

# class Crime(Event):
#     def burst(self):
#         super().burst(self)
#         self.observer.notify(EVENT_CRIME_FOUND, self.risk)