from graph import *
from observer import *
from simulation_core import *

'''List of breaking news
    Each element is a list with :
     - a string to be shown on screen
     - a dictionnary with
        - keys = id of the variable to change (0 for soap, 1 for )
        TODO'''
    
    # string, (ressource type, factor)
news = {
    "Enjoy a hot air balloon trip for two people at a low price !": {},
    "A strange phenomenon: giant soap bubbles invade a beach": {},
    "A toxic bubble discovered in barley fields. Repercussions on the beer industry are to be expected.": {BeerNode: [(BeerNode.mulValue, 0.3)]},
    "Soap isn't strong enough anymore, try bleach instead.": {SoapNode : [(SoapNode.mulValue, 0.6), (SoapNode.increment_min_price, -0.15)]},
    "Alcoholism is climbing, investors love you, people blame you.": {},
    "blup, Blup, BLUP ...                          POP !": {},
    "O     °     O     o     0     °     o     O     0     °     o     0     O": {},
    "Video game industry experts are predicting that bubble-themed games are going to be the next big thing.": {},
    "Maps are becoming collectibles; with some paying hundreds of dollars for them for them.": {},
    "Price of bubble wrap explodes after surge in demand for e-commerce" : {WrapNode : [(WrapNode.mulValue, 1.8)]},
    "Health insitutions have descovered asbestos in bubble-rap (TM) soap! Avoid using it at all costs" : {SoapNode : [(SoapNode.mulValue, 0.8)]},
    "Scandal breaks out: disposable bubble wrap singled out for its plastic pollution": {WrapNode : [(WrapNode.mulValue, 0.5)]},
    "A world record: an author creates a comic strip with 10,000 speech bubbles on a single page !" : {}, 
    "Champagne !" : {},
    "Following the TriPod challenge, swallowing bubble soap becomes the new trend for Gen Zers" : {SoapNode : [(SoapNode.mulValue, 1.2)]},
    "A beer enriched with vitamins promises to combine pleasure and well-being" : {BeerNode: [(BeerNode.mulValue, 1.3)]},
    "Five reasons you should start using Bubble Sort in your code (and five why it sucks)" : {},
    
}