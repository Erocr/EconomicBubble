import simulation_core as core
from bubble import Bubble
from PopUps import PopupsContainer
import random
import curve
from observer import *
from actions import Actions

class EconomyGraph:
    def __init__(self, visual_data, observer):
        vd = visual_data
        
        self.observer = observer

        self.TC = core.TrueCapitalNode(
            Bubble(vd.bubble_size_capital, vd.pos_true_capital, vd.default_fill,
                   "", (7, 37, 6), (133, 187, 101)), observer
        )  # True capital

        self.AC = core.ApparentCapitalNode(
            Bubble(vd.bubble_size_capital, vd.pos_shown_capital, vd.default_fill,
                   "", (7, 37, 6), (133, 187, 101)), observer
        )  # Apparent capital

        self.ID = core.InvestorsDoubtNode(
            Bubble(vd.bubble_size_doubt, vd.pos_investor_doubt, vd.default_fill,
                   "Investor Doubt", (33, 171, 205), (239, 204, 0)), observer
        )  # Investors Doubt

        self.PD = core.PublicDoubtNode(
            Bubble(vd.bubble_size_doubt, vd.pos_public_doubt, vd.default_fill,
                   "Public Doubt", (33, 171, 205), (239, 204, 0)), observer
        )  # Public Doubt

        self.Events = core.EventNode(
            Bubble(vd.bubble_size_investing, vd.sc * 2, vd.default_fill,
                   "Wrap", (246, 108, 164), (245, 197, 217)), observer
        )  # Events

        self.M1 = core.MarketingNode(
            Bubble(vd.bubble_size_big, vd.pos_marketing, vd.default_fill,
                   "Marketing", (45, 81, 242), (22, 164, 202)), observer
        )  # Marketing 1 : press message

        self.S1 = core.SecurityNode(
            Bubble(vd.bubble_size_big, vd.pos_security, vd.default_fill,
                   "Security", (1, 1, 1), (128, 128, 128)), observer
        )  # Security 1 : media control

        self.Spy = core.EspionageNode(
            Bubble(vd.bubble_size_big, vd.pos_espionnage, vd.default_fill,
                   "Espionnage", (128, 0, 0), (184, 20, 20)), observer
        )  # Espionage

        self.soap_color = (95, 167, 120)
        self.beer_color = (185, 113, 31)
        self.wrap_color = (246, 108, 164)

        self.SoapM = core.SoapNode(
            Bubble(vd.bubble_size_investing, vd.pos_invest_left, vd.default_fill,
                   "", (206, 200, 239),self.soap_color), observer
        )  # Soap Market

        self.BeerM = core.BeerNode(
            Bubble(vd.bubble_size_investing, vd.pos_invest_center, vd.default_fill,
                   "", self.beer_color, (242, 142, 28)), observer
        )  # Beer Market

        self.WrapM = core.WrapNode(
            Bubble(vd.bubble_size_investing, vd.pos_invest_right, vd.default_fill,
                   "", self.wrap_color, (245, 197, 217)), observer
        )  # Wrap Market

        self.savedValues = []
        self.multi_curve = curve.MultiCurve(vd.multicurve_pos, vd.multicurve_size, 3,
                                            [self.soap_color, self.beer_color, self.wrap_color])

        self.market_nodes = [self.SoapM, self.BeerM, self.WrapM]

        self.market = core.MarketGroup(self.market_nodes)

        self.influenced_nodes = [
            self.TC, self.AC, self.PD, self.ID, self.Events, self.market
        ]

        self.clickable_nodes = [
            self.M1, self.S1, self.Spy
        ]

        self.nodes = self.influenced_nodes + self.clickable_nodes

        self.all_nodes = [
            self.TC, self.AC, self.PD, self.ID, self.Events, self.M1, self.S1, self.Spy,
        ] + self.market_nodes

        self.observer.add_observables(self.all_nodes)

        # Edges
        self.TC.addParents([*self.market_nodes, self.ID])
        self.AC.addParents([self.TC, self.M1, self.PD])

        self.market.addParents([self.PD, self.Spy, self.TC])

        self.PD.addParents([self.Events, self.ID])
        self.ID.addParents([self.S1, self.Events, self.AC, self.ID])
        self.M1.addParents([self.S1, self.TC])
        self.Events.addParents([self.Spy])
        self.S1.addParents([self.Events, self.TC])
        self.Spy.addParents([self.Events, self.TC])

        self.type_to_node = {type(node): node for node in self.all_nodes}
        
        self.actions = Actions(core.TrueCapitalNode, core.WrapNode, core.SoapNode, core.WrapNode, core.PublicDoubtNode, core.InvestorsDoubtNode, core.SecurityNode)

    def quick_simulation_update(self):
        for node in self.nodes:
            node.quick_update()

    def save_values(self):
        self.savedValues.append([node._value for node in self.market_nodes])

    def update_multigraph(self):
        for e in self.savedValues:
            self.multi_curve.add_values(e)
        self.savedValues = []

    def notify(self, event, notifications):
        if event == EVENT_EVENT_BURST:
            security = self.S1
            public = self.PD
            investors = self.ID.investors
            volatility = 1.1

            if security.defense_team > 0:
                security.add_defense_team(-1)
                self.observer.notify(EVENT_NEW_POPUP,
                (["A crime was discovered!", "You used a legal defense!"],
                (0, 0, 0)))
            else:
                public._value = min(100, public._value + notifications)
                for investor in investors:
                    investor._value += abs(random.gauss(0, public.volatility)) * notifications
                    investor._value = core.clamp(public._value, 1, 100)
                self.observer.notify(EVENT_NEW_POPUP,
                (["A crime was discovered!", "You've lost trust of public!"],
                (0, 0, 0)))
                volatility = 1.5
            # no matter what, people become very unstable
            public.volatility *= volatility
            public.volatility = core.clamp(public.volatility, 1, 10)
            for investor in investors:
                investor._value += abs(random.gauss(0, public.volatility)) * notifications
                investor._value = core.clamp(investor._value, 1, 100)
                investor.volatility *= volatility
                investor.volatility = core.clamp(investor.volatility, 1, 10)

        elif event == EVENT_INVESTED:
            investor, invested = notifications
            capital = self.TC._value
            invest_str = str(int(invested * capital)) + "$"
            self.observer.notify(EVENT_NEW_POPUP,
                (["An investor has just spent ", invest_str + " into your company!"],
                (0, 0, 0))
            )
            investor.invested_money += invested * capital
        elif event == EVENT_PULLED_OUT:
            investor, pulled_out = notifications
            capital = self.TC._value
            pullout_str = str(int(pulled_out * capital)) + "$"
            self.observer.notify(EVENT_NEW_POPUP,
                (["An investor has withdrawn", pullout_str + " from your company!"],
                (255, 0, 0))
            )
            investor.invested_money -= pulled_out * capital
            if investor.owned_shares == 0:
                self.observer.notify(EVENT_NEW_POPUP,
                (["An investor has left your company!"], (255, 0, 0)))

        elif event == EVENT_REQUEST_QUESTION:
            if self.S1.check_answer <= 0:
                self.observer.notify(EVENT_NEW_POPUP,
                (["There was nothing interesting."], (0, 0, 0)))
                return
            string1 = notifications[0] + str(int(notifications[1] * 100)) + "%"
            string2 = notifications[0] + str(int(notifications[2] * 100)) + "%"
            self.actions.questions[string1] = {self.S1: [(self.S1.right_answer, 1)]}
            self.actions.questions[string2] = {self.S1: [(self.S1.wrong_answer, 1)]}
            self.observer.notify(EVENT_TRIGGER_CHOICES, [string1, string2])

        elif event == EVENT_RIGHT_ANSWER:
            public.volatility *= 0.8
            public.volatility = core.clamp(public.volatility, 1, 10)
            for investor in investors:
                investor.volatility *= 0.8
                investor.volatility = core.clamp(investor.volatility, 1, 10)
            self.observer.notify(EVENT_NEW_POPUP,
                (["Right Answer! You are now more stable!"], (0, 0, 0)))

        elif event == EVENT_WRONG_ANSWER:
            public.volatility *= 1.2
            public.volatility = core.clamp(public.volatility, 1, 10)
            for investor in investors:
                investor.volatility *= 1.2
                investor.volatility = core.clamp(investor.volatility, 1, 10)
            self.observer.notify(EVENT_NEW_POPUP,
                (["Wrong Answer! Better luck next time!"], (0, 0, 0)))

    def update_simulation(self):
        random.shuffle(self.nodes)
        for node in self.nodes:
            node.update()

        max_invest = 0
        for investor in self.ID.investors:
            investor.true_capital = self.TC._value
            if investor.owned_shares > max_invest:
                max_invest = investor.owned_shares
        self.S1.check_answer = max_invest

    def update_visuals(self, view, inputs, observer, paused):
        for node in self.nodes:
            node.draw(view, inputs, paused)
        self.multi_curve.draw(view)

    def draw_docs(self, view):
        for node in self.nodes:
            node.draw_docs(view)

    def apply_action(self, action):
        # print(self.type_to_node)
        for node_type, actions in action.items():
            for function, arg in actions:
                function(self.type_to_node[node_type], arg)

    def has_exploded(self):
        return (self.AC._value <= 0) or (self.PD._value >= 100)