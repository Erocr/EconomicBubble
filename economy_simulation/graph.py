import simulation_core as core

class EconomyGraph:
    def __init__(self):
        self.market_nodes = (core.MarketNode(),)*3
        self.nodes = [*self.market_nodes]

        self.influence_table = {
            
        }

