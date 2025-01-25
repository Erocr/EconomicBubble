import simulation_core as core
from bubble import Bubble
from PopUps import PopupsContainer
import matplotlib.pyplot as plt
import numpy as np
import random
import curve
import vec

class EconomyGraph:
    def __init__(self, visual_data):
        self.vd = visual_data
        self.popups = PopupsContainer()

        self.TC = core.TrueCapitalNode(
            Bubble(self.vd.bubble_size_capital, self.vd.pos_true_capital, self.vd.default_fill,
                    "",  (7, 37, 6), (133, 187, 101))
        ) # True capital

        self.AC = core.ApparentCapitalNode(
            Bubble(self.vd.bubble_size_capital, self.vd.pos_shown_capital, self.vd.default_fill,
                    "",  (7, 37, 6), (133, 187, 101))
        ) # Apparent capital

        self.ID = core.InvestorsDoubtNode(
            Bubble(self.vd.bubble_size_doubt, self.vd.pos_investor_doubt, self.vd.default_fill,
                   "Investor Doubt", (33,171,205),(239,204,0))
        ) # Investors Doubt

        self.PD = core.PublicDoubtNode(
            Bubble(self.vd.bubble_size_doubt, self.vd.pos_public_doubt, self.vd.default_fill,
                   "Public Doubt", (33,171,205),(239,204,0))
        ) # Public Doubt

        self.Events = core.EventNode(
            Bubble(self.vd.bubble_size_investing, self.vd.sc * 2, self.vd.default_fill,
                   "Wrap", (246, 108, 164), (245, 197, 217))
        ) # Events
    
        self.M1 = core.MarketingNode(
            Bubble(self.vd.bubble_size_big, self.vd.pos_marketing, self.vd.default_fill,
                   "Marketing", (45,81, 242), (22,164,202)) 
        )       # Marketing 1 : press message

        self.S1 = core.SecurityNode(
            Bubble(self.vd.bubble_size_big, self.vd.pos_security, self.vd.default_fill,
                   "Security",(1, 1, 1), (128, 128, 128))
        )       # Security 1 : media control

        self.Spy = core.EspionageNode(
            Bubble(self.vd.bubble_size_big, self.vd.pos_espionnage, self.vd.default_fill,
                    "Espionnage", (128, 0, 0), (184, 20, 20))
        )      # Espionage

        self.soap_color = (95, 167, 120)
        self.beer_color = (185, 113, 31)
        self.wrap_color = (246, 108, 164)

        self.SoapM = core.MarketNode(
            Bubble(self.vd.bubble_size_investing, self.vd.pos_invest_left, self.vd.default_fill,
                    "", self.soap_color, (206, 200, 239)), "Soap"
        ) # Soap Market

        self.BeerM = core.MarketNode(
            Bubble(self.vd.bubble_size_investing, self.vd.pos_invest_center, self.vd.default_fill,
                    "", self.beer_color, (242, 142, 28)), "Beer"
        ) # Beer Market

        self.WrapM = core.MarketNode(
            Bubble(self.vd.bubble_size_investing, self.vd.pos_invest_right, self.vd.default_fill,
                    "", self.wrap_color, (245, 197, 217)), "Wrap"
        ) # Wrap Market

        self.multi_curve = curve.MultiCurve(self.vd.multicurve_pos, self.vd.multicurve_size, 3,
                                            [self.soap_color, self.beer_color, self.wrap_color])

        self.market_nodes = [self.SoapM, self.BeerM, self.WrapM]

        self.influenced_nodes = [
            self.TC, self.AC, self.PD, self.ID, self.Events
        ] + self.market_nodes

        self.clickable_nodes = [
            self.M1, self.S1, self.Spy
        ]

        self.nodes = self.influenced_nodes + self.clickable_nodes

        # Edges
        self.TC.addParents([*self.market_nodes, self.ID])
        self.AC.addParents([self.TC, self.M1, self.PD])

        for node in self.market_nodes:
            node.addParents([self.PD])

        self.PD.addParents([self.Events, self.Spy])
        self.ID.addParents([self.S1, self.Events, self.AC, self.ID])
        self.M1.addParents([self.S1])
        self.Events.addParents([self.Spy])

    def quick_simulation_update(self):
        for node in self.nodes:
            node.quick_update()
    
    def check_invest(self, node):
        if type(node) == core.InvestorsDoubtNode:
            if node.invested > 0:
                self.popups.add_popup(
                    f"An investor has just bought {node.invested * 100}% of your company!"
                )
                node.invested = 0
                

    def update_simulation(self):
        random.shuffle(self.nodes)
        for node in self.nodes:
            node.update()
    
    def draw_market_multicurve(self, view):
        # draw the multi curve
        self.multi_curve.add_values([node._value for node in self.market_nodes])
        self.multi_curve.draw(view)

    def update_visuals(self, view, inputs):
        for node in self.nodes:
            node.draw(view, inputs)
            self.check_invest(node)
            self.popups.update(inputs)
        self.draw_market_multicurve(view)

    def has_exploded(self):
        return (self.AC._value == 0) or (self.ID._value > 100) or (self.PD._value > 100)

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