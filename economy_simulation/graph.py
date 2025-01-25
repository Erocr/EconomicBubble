import simulation_core as core
import matplotlib.pyplot as plt
import numpy as np
import random

class EconomyGraph:
    def __init__(self):
        # Nodes
        TC = core.TrueCapitalNode()     # True capital
        AC = core.ApparentCapitalNode() # Apparent capital
        SoapM = core.MarketNode()       # Soap Market
        BeerM = core.MarketNode()       # Beer Market
        OperaM = core.MarketNode()      # Soap-Opera Market
        PD = core.PublicDoubtNode()     # Public Doubt
        ID = core.InvestorsDoubtNode() # Investors Doubt
        Events = core.EventNode()       # Events

        M1 = core.MarketingNode()       # Marketing 1 : press message
        M2 = core.MarketingNode()       # Marketing 2 : ads
        S1 = core.SecurityNode()        # Security 2 : media control
        S2 = core.SecurityNode()        # Security 2 : surveillance
        Spy = core.EspionageNode()       # Espionage

        self.nodes = [
            TC, AC, SoapM, BeerM, OperaM, PD, ID, Events
        ]
        
        # Edges
        TC.addParents([SoapM, BeerM, OperaM, ID])
        AC.addParents([TC, M1, PD])
        SoapM.addParents([PD])
        BeerM.addParents([PD])
        OperaM.addParents([PD])
        PD.addParents([M2, Events])
        ID.addParents([S1, Events, AC, ID])
        M1.addParents([S1])
        M2.addParents([S2])
        Events.addParents([S2, Spy])
        
        # self.market_nodes = (core.MarketNode(),)*3
        # self.nodes = [*self.market_nodes]

        # self.influence_table = {
            # 0: (2, 3, 4)
        # }

    def update(self):
        random.shuffle(self.nodes)
        for e in self.nodes:
            e.update()
    
    def dbg_print(self):
        for node in self.nodes:
            print(node.__name__)
            print(node._value)

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