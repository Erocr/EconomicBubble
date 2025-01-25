import simulation_core as core
from ... import bubble, visual_data
import matplotlib.pyplot as plt
import numpy as np
import random


class EconomyGraph:
    def __init__(self, visualData):
        self.vd = visualData
        
        self.TC = core.TrueCapitalNode(
            bubble.Bubble(self.vd.bubble_size_capital, self.vd.pos_true_capital, self.vd.default_fill,
                self.vd.string_true_capital,  (7, 37, 6), (133, 187, 101))
        ) # True capital

        self.AC = core.ApparentCapitalNode(
            bubble.Bubble(self.vd.bubble_size_capital, self.vd.pos_shown_capital, self.vd.default_fill,
                self.vd.string_shown_capital,  (7, 37, 6), (133, 187, 101)),
        ) # Apparent capital

        self.SoapM = core.MarketNode(
            bubble.Bubble(self.vd.bubble_size_investing, self.vd.pos_invest_left, self.vd.default_fill, "Soap",
                (95, 167, 120), (206, 200, 239)),
        ) # Soap Market

        self.BeerM = core.MarketNode(
            bubble.Bubble(self.vd.bubble_size_investing, self.vd.pos_invest_center, self.vd.default_fill, "Beer",
                (185, 113, 31), (242, 142, 28)),
        ) # Beer Market

        self.OperaM = core.MarketNode(
            bubble.Bubble(self.vd.bubble_size_investing, self.vd.pos_invest_right, self.vd.default_fill, "Soap Opera",
                (246, 108, 164), (245, 197, 217)),
        ) # Bubblewrap Market

        self.PD = core.PublicDoubtNode(
            
        ) # Public Doubt

        self.ID = core.InvestorsDoubtNode(

        ) # Investors Doubt

        self.Events = core.EventNode(

        ) # Events
    
        self.M1 = core.MarketingNode(
            bubble.Bubble(self.vd.bubble_size_big, self.vd.pos_marketing, self.vd.default_fill,
                   "Marketing", (0, 0, 255), (0, 255, 255)),
        )       # Marketing 1 : press message

        self.M2 = core.MarketingNode(

        )       # Marketing 2 : ads

        self.S1 = core.SecurityNode(
            bubble.Bubble(self.vd.bubble_size_big, self.vd.pos_security, self.vd.default_fill, "Security",
                    (255, 0, 0), (255, 100, 100)),
        )        # Security 2 : media control

        self.S2 = core.SecurityNode(

        )        # Security 2 : surveillance

        self.Spy = core.EspionageNode(
            bubble.Bubble(self.vd.bubble_size_big, self.vd.pos_espionnage, self.vd.default_fill,
                    "Espionnage", (50, 0, 0), (100, 0, 0))
        )      # Espionage


        self.influenced_nodes = [
            self.TC, self.AC, self.SoapM, self.BeerM, self.OperaM, self.PD, self.ID, self.Events
        ]

        self.clickable_nodes = [
            self.M1, self.M2, self.S1, self.S2, self.Spy
        ]

        self.nodes = self.influenced_nodes + self.clickable_nodes

        # Edges
        self.TC.addParents([self.SoapM, self.BeerM, self.OperaM, self.ID])
        self.AC.addParents([self.TC, self.M1, self.PD])
        self.SoapM.addParents([self.PD])
        self.BeerM.addParents([self.PD])
        self.OperaM.addParents([self.PD])
        self.PD.addParents([self.M2, self.Events])
        self.ID.addParents([self.S1, self.Events, self.AC, self.ID])
        self.M1.addParents([self.S1])
        self.M2.addParents([self.S2])
        self.Events.addParents([self.S2, self.Spy])

    def update_simulation(self):
        random.shuffle(self.nodes)
        for e in self.nodes:
            e.update()
    
    def update_visuals(self, inputs):
        for bubble in self.bubbles:
            bubble.update(inputs)

    def draw(self, view):
        for bubble in self.bubbles:
            bubble.draw(view)

    def dbg_print(self):
        for node in self.nodes:
            print(node.__name__)
            print(node._value)

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


def main():
    economy = EconomyGraph()
    time = np.arange(100)
    for i in time:
        economy.update()

    for node in economy.nodes:
        plt.plot(time, node.value_history, label = str(node))

    plt.legend()
    plt.show()

main()