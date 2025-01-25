import simulation_core as core
import matplotlib.pyplot as plt
import numpy as np
import random

class EconomyGraph:
    def __init__(self):
        # Nodes
        self.TC = core.TrueCapitalNode()     # True capital
        self.AC = core.ApparentCapitalNode() # Apparent capital
        self.SoapM = core.MarketNode()       # Soap Market
        self.BeerM = core.MarketNode()       # Beer Market
        self.OperaM = core.MarketNode()      # Soap-Opera Market
        self.PD = core.PublicDoubtNode()     # Public Doubt
        self.ID = core.InvestorsDoubtNode() # Investors Doubt
        self.Events = core.EventNode()       # Events

        self.M1 = core.MarketingNode()       # Marketing 1 : press message
        self.M2 = core.MarketingNode()       # Marketing 2 : ads
        self.S1 = core.SecurityNode()        # Security 2 : media control
        self.S2 = core.SecurityNode()        # Security 2 : surveillance
        self.Spy = core.EspionageNode()       # Espionage

        self.nodes = [
            self.TC, self.AC, self.SoapM, self.BeerM, self.OperaM, self.PD, self.ID, self.Events
        ]
        
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

    def update(self):
        random.shuffle(self.nodes)
        for e in self.nodes:
            e.update()
    
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