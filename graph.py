import simulation_core as core
from bubble import Bubble
import matplotlib.pyplot as plt
import numpy as np
import random
import curve
import vec


class MarketGroup:
    def __init__(self):
        self.SoapM = core.MarketNode(
            Bubble(self.vd.bubble_size_investing, self.vd.pos_invest_left, self.vd.default_fill, "Soap",
                (95, 167, 120), (206, 200, 239))
        ) # Soap Market

        self.BeerM = core.MarketNode(
            Bubble(self.vd.bubble_size_investing, self.vd.pos_invest_center, self.vd.default_fill, "Beer",
                (185, 113, 31), (242, 142, 28))
        ) # Beer Market

        self.WrapM = core.MarketNode(
            Bubble(self.vd.bubble_size_investing, self.vd.pos_invest_right, self.vd.default_fill, "Wrap",
                (246, 108, 164), (245, 197, 217))
        ) # Wrap Market

        self.nodes = [self.BeerM, self.SoapM, self.WrapM]

        self.multi_curve = curve.MultiCurve(vec.Vec(0, 0), vec.Vec(100, 100), 3, [(255, 0, 0), (0, 255, 0), (0, 0, 255)])

    def update(self):
        for node in self.nodes:
            node.update()
    
    def draw(self, view, inputs):
        # draw the bubbles
        for node in self.nodes:
            node.draw(view, inputs)
        
        # draw the multi curve
        self.multi_curve.add_values([node._value for node in self.nodes])
        self.multi_curve.draw(view)
    

class EconomyGraph:
    def __init__(self, visualData):
        self.vd = visualData
        
        self.TC = core.TrueCapitalNode(
            Bubble(self.vd.bubble_size_capital, self.vd.pos_true_capital, self.vd.default_fill,
                core.string_true_capital(0),  (7, 37, 6), (133, 187, 101))
        ) # True capital

        self.AC = core.ApparentCapitalNode(
            Bubble(self.vd.bubble_size_capital, self.vd.pos_shown_capital, self.vd.default_fill,
                core.string_shown_capital(0),  (7, 37, 6), (133, 187, 101))
        ) # Apparent capital

        self.ID = core.InvestorsDoubtNode(
            Bubble(self.vd.bubble_size_doubt, self.vd.pos_investor_doubt, self.vd.default_fill, "Investor Doubt",
                (33,171,205),(239,204,0))
        ) # Investors Doubt

        self.PD = core.PublicDoubtNode(
            Bubble(self.vd.bubble_size_doubt, self.vd.pos_public_doubt, self.vd.default_fill, "Public Doubt",
                (33,171,205),(239,204,0))
        ) # Public Doubt

        self.Events = core.EventNode(
            Bubble(self.vd.bubble_size_investing, self.vd.pos_invest_right, self.vd.default_fill, "Wrap",
                (246, 108, 164), (245, 197, 217))
        ) # Events
    
        self.M1 = core.MarketingNode(
            Bubble(self.vd.bubble_size_big, self.vd.pos_marketing, self.vd.default_fill,
                   "Marketing", (0, 0, 255), (0, 255, 255))
        )       # Marketing 1 : press message

        self.S1 = core.SecurityNode(
            Bubble(self.vd.bubble_size_big, self.vd.pos_security, self.vd.default_fill, "Security",
                    (255, 0, 0), (255, 100, 100))
        )       # Security 1 : media control

        self.Spy = core.EspionageNode(
            Bubble(self.vd.bubble_size_big, self.vd.pos_espionnage, self.vd.default_fill,
                    "Espionnage", (50, 0, 0), (100, 0, 0))
        )      # Espionage

        self.influenced_nodes = [
            self.TC, self.AC, self.SoapM, self.BeerM, self.WrapM, self.PD, self.ID, self.Events
        ]

        self.clickable_nodes = [
            self.M1, self.S1, self.Spy
        ]

        self.nodes = self.influenced_nodes + self.clickable_nodes

        # Edges
        self.TC.addParents([self.SoapM, self.BeerM, self.WrapM, self.ID])
        self.AC.addParents([self.TC, self.M1, self.PD])
        self.SoapM.addParents([self.PD])
        self.BeerM.addParents([self.PD])
        self.WrapM.addParents([self.PD])
        self.PD.addParents([self.Events])
        self.ID.addParents([self.S1, self.Events, self.AC, self.ID])
        self.M1.addParents([self.S1])
        self.Events.addParents([self.Spy])

    def update_simulation(self):
        random.shuffle(self.nodes)
        for node in self.nodes:
            node.update()
            
    def update_visuals(self, view, inputs):
        for node in self.nodes:
            node.draw(view, inputs)
    
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