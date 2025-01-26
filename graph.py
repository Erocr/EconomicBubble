import simulation_core as core
from bubble import Bubble
from PopUps import PopupsContainer
# import matplotlib.pyplot as plt
# import numpy as np
import random
import curve
import vec
from observer import *


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

        self.SoapM = core.MarketNode(
            Bubble(vd.bubble_size_investing, vd.pos_invest_left, vd.default_fill,
                   "", self.soap_color, (206, 200, 239)), "Soap", observer
        )  # Soap Market

        self.BeerM = core.MarketNode(
            Bubble(vd.bubble_size_investing, vd.pos_invest_center, vd.default_fill,
                   "", self.beer_color, (242, 142, 28)), "Beer", observer
        )  # Beer Market

        self.WrapM = core.MarketNode(
            Bubble(vd.bubble_size_investing, vd.pos_invest_right, vd.default_fill,
                   "", self.wrap_color, (245, 197, 217)), "Wrap", observer
        )  # Wrap Market

        self.multi_curve = curve.MultiCurve(vd.multicurve_pos, vd.multicurve_size, 3,
                                            [self.soap_color, self.beer_color, self.wrap_color])

        self.market_nodes = [self.SoapM, self.BeerM, self.WrapM]

        self.influenced_nodes = [
                                    self.TC, self.AC, self.PD, self.ID, self.Events
                                ] + self.market_nodes

        self.clickable_nodes = [
            self.M1, self.S1, self.Spy
        ]

        self.nodes = self.influenced_nodes + self.clickable_nodes
        
        self.observer.add_observables(self.nodes)

        # Edges
        self.TC.addParents([*self.market_nodes, self.ID])
        self.AC.addParents([self.TC, self.M1, self.PD])

        for node in self.market_nodes:
            node.addParents([self.PD, self.Spy, self.TC])

        self.PD.addParents([self.Events, self.ID])
        self.ID.addParents([self.S1, self.Events, self.AC, self.ID])
        self.M1.addParents([self.S1, self.TC])
        self.Events.addParents([self.Spy])
        self.S1.addParents([self.Events, self.TC])
        self.Spy.addParents([self.TC])

    def quick_simulation_update(self):
        for node in self.nodes:
            node.quick_update()

    def update_multigraph(self):
        self.multi_curve.add_values([node._value for node in self.market_nodes])

    def check_invest(self, node, observer):
        node = self.ID
        if node.invested > 0:
            invest_str = str(int(node.invested * 100)) + "%"
            observer.notify(EVENT_NEW_POPUP,
                            (["An investor has just bought", invest_str + " of your company!"],
                             (0, 0, 0))
                            )
            node.invested = 0

    def check_pullout(self, node, observer):
        node = self.ID
        if node.pulled_out > 0:
            pullout_str = str(int(node.pulled_out * 100)) + "%"
            observer.notify(EVENT_NEW_POPUP,
                            (["An investor has withdrawn", pullout_str + " of your company!"],
                             (255, 0, 0))
                            )
            node.pulled_out = 0

    def update_simulation(self):
        random.shuffle(self.nodes)
        full_debt = 0
        for node in self.nodes:
            full_debt += node.debt
            node.debt = 0
            node.true_capital = self.TC._value
            node.update()
        self.TC._value -= full_debt
        if self.TC._value < 0: self.TC._value = 0

    def update_visuals(self, view, inputs, observer, paused):
        for node in self.nodes:
            node.draw(view, inputs, paused)
            if not paused:
                self.check_invest(node, observer)
                self.check_pullout(node, observer)
        self.multi_curve.draw(view)

    def draw_docs(self, view):
        for node in self.nodes:
            node.draw_docs(view)

    def has_exploded(self):
        return (self.AC._value == 0) or (self.ID._value >= 100) or (self.PD._value >= 100)

# def main2():
#     economy = EconomyGraph()
#     time = np.arange(100)
#     for i in time:
#         economy.update()

#     i, l = 0, len(economy.nodes)
#     fig = plt.figure(figsize = [l // 5, 5])
#     for node in economy.nodes:
#         ax = plt.subplot(i // 5 + 1, i + 1, i + 1)
#         ax.plot(time, node.value_history, label = str(node))

#         ax.legend()
#         i += 1
#     plt.show()


# def main():
#     economy = EconomyGraph()
#     time = np.arange(100)
#     for i in time:
#         economy.update()

#     for node in economy.nodes:
#         plt.plot(time, node.value_history, label = str(node))

#     plt.legend()
#     plt.show()

# main()
