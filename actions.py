from graph import *

'''List of actions
    Each element is a list with :
     - a string to be shown on screen
     - a dictionnary with
        - keys = id of the variable to change (0 for soap, 1 for beer, 2 for wrap)
        - float influences
        TODO'''

    # string, (ressource type, factor)
actions = {
    "You create a viral social media campaign featuring your soap products being used as impromptu bubble wrap replacements in a humorous DIY video":
    {TrueCapitalNode : [(TrueCapitalNode.mulValue, 1.05)], 
     WrapNode : [(WrapNode.mulValue, 1.03)], 
     SoapNode : [(SoapNode.mulValue, 1.02)],
     PublicDoubtNode : [(PublicDoubtNode.mulValue, 0.9)]
     },
    #(Effect: TrueCapitalNode + 5%, WrapNode + 3%, SoapNode + 2%, PublicDoubtNode - 10%)
    "You host an 'open house' where you let customers play with bubble wrap for hours on end, causing a massive delay in production and sales":
    {WrapNode : [(WrapNode.mulValue, 1.05)],
     PublicDoubtNode : [(PublicDoubtNode.mulValue, 1.10)],
     SoapNode : [(PublicDoubtNode.mulValue, 1.10)],
     },
    #(Effect: WrapNode + 5%, PublicDoubtNode - 10%, SoapNode - 1%, BeerNode - 3%, InvestorsDoubtNode + 3%)"
    "You decide to rebrand your soap company as 'Bubble Wrap Soaps' just to see how many investors take it seriously":
    {InvestorsDoubtNode : [(InvestorsDoubtNode.mulValue, 1.08)],
     TrueCapitalNode : [(TrueCapitalNode.mulValue, 0.96)],
     WrapNode : [(WrapNode.mulValue, 1.06)],
     SoapNode : [(SoapNode.mulValue, 0.97)]
     },
    # (Effect: InvestorsDoubtNode + 8%, TrueCapitalNode - 4%, WrapNode + 6%, SoapNode - 3%)
    "You buy an entire warehouse full of bubble wrap to use as office decor and end up bankrupting the company":
    {WrapNode : [(WrapNode.mulValue, 1.08)],
     InvestorsDoubtNode : [(InvestorsDoubtNode.mulValue, 1.1)],
     TrueCapitalNode : [TrueCapitalNode.mulValue, 0.88]
     },
    #(Effect: WrapNode + 8%, InvestorsDoubtNode + 10%, TrueCapitalNode - 12%)"
    "You accidentally order 1000 cases of beer for a party that only 10 people will attend, resulting in a massive inventory glut":
    {BeerNode : [(BeerNode.mulValue, 0.95)],
     TrueCapitalNode : [(TrueCapitalNode.mulValue, 0.9)],
     PublicDoubtNode : [(PublicDoubtNode.mulValue, 1.05)],
     },
    #(Effect: BeerNode - 5%, TrueCapitalNode - 2%, PublicDoubtNode + 5%)",
    "You start selling soap-shaped whoopee cushions as a 'novelty item' to make some extra cash, but they're actually a major distraction from your main products":
    {SoapNode : [(SoapNode.mulValue, 1.1)],
     WrapNode : [(WrapNode.mulValue, 0.96)],
     BeerNode : [(BeerNode.mulValue, 0.96)],
     TrueCapitalNode : [(TrueCapitalNode.mulValue, 1.04)],
     PublicDoubtNode : [(PublicDoubtNode.mulValue, 0.98)]
    },
    #(Effect: SoapNode + 10%, WrapNode - 4%, BeerNode - 4%, TrueCapitalNode + 4%, PublicDoubtNode - 2%)",
    "You try to create a viral challenge by making people attempt to wrap themselves in bubble wrap, but it ends up being a mess":
    {WrapNode : [(WrapNode.mulValue, 1.4)],
     InvestorsDoubtNode : [(InvestorsDoubtNode.mulValue, 0.98)],
     TrueCapitalNode : [(TrueCapitalNode.mulValue, 0.9)],
     SoapNode : [(SoapNode.mulValue, 0.97)],
    },
    #(Effect: WrapNode + 4%, InvestorsDoubtNode - 2%, TrueCapitalNode - 1%, SoapNode - 3%)
    "You partner with a rival company to co-create a beer-infused soap that's supposed to be the 'next big thing', but it's actually just gross":
    {BeerNode : [(BeerNode.mulValue, 0.94)],
     SoapNode : [(SoapNode.mulValue, 0.95)],
     WrapNode : [(WrapNode.mulValue, 0.98)],
     TrueCapitalNode : [(TrueCapitalNode.mulValue, 0.96)]
    },
    #(Effect: BeerNode - 6%, SoapNode - 5%, WrapNode - 2%, TrueCapitalNode - 4%)
    "You decide to replace all your employees with automated bubble wrap dispensers, but they keep getting jammed and causing chaos":
    {InvestorsDoubtNode : [(InvestorsDoubtNode.mulValue, 1.08)],
     PublicDoubtNode : [(PublicDoubtNode.mulValue, 1.03)],
     TrueCapitalNode : [(TrueCapitalNode.mulValue, 0.94)],
     WrapNode : [(WrapNode.mulValue, 0.95)]
    },
    
    "You host a 'soap-making' workshop for kids where they get to create their own bubble wrap soap, but it's actually just a bunch of sticky messes":
    {SoapNode: [(SoapNode.mulValue, 1.02)],
     WrapNode: [(WrapNode.mulValue, 1.01)],
     InvestorsDoubtNode: [(InvestorsDoubtNode.mulValue, 0.99)],
     TrueCapitalNode: [(TrueCapitalNode.mulValue, 0.99)]},
    # (Effect: SoapNode + 2%, WrapNode + 1%, InvestorsDoubtNode - 1%, TrueCapitalNode - 1%)
    
    "You invest in a beer brewery that specializes in creating beers with extremely unusual ingredients, like seaweed and garlic":
    {BeerNode: [(BeerNode.mulValue, 1.04)],
     PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.98)],
     TrueCapitalNode: [(TrueCapitalNode.mulValue, 0.97)],
     InvestorsDoubtNode: [(InvestorsDoubtNode.mulValue, 0.99)]},
    # (Effect: BeerNode + 4%, PublicDoubtNode - 2%, TrueCapitalNode - 3%, InvestorsDoubtNode - 1%)

    "You create an 'anti-bubble wrap' movement where people try to avoid bubble wrap at all costs, but it's actually just a bunch of hipsters being hipsters":
    {WrapNode: [(WrapNode.mulValue, 0.94)],
     SoapNode: [(SoapNode.mulValue, 0.96)],
     TrueCapitalNode: [(TrueCapitalNode.mulValue, 0.98)],
     PublicDoubtNode: [(PublicDoubtNode.mulValue, 1.03)]},
    # (Effect: WrapNode - 6%, SoapNode - 4%, TrueCapitalNode - 2%, PublicDoubtNode + 3%)

    "You start selling 'soap-scented' beer that's supposed to be the perfect pairing for your soap products, but it's actually just a cheap gimmick":
    {BeerNode: [(BeerNode.mulValue, 1.03)],
     SoapNode: [(SoapNode.mulValue, 0.99)],
     WrapNode: [(WrapNode.mulValue, 0.98)],
     TrueCapitalNode: [(TrueCapitalNode.mulValue, 0.98)]},
    # (Effect: BeerNode + 3%, SoapNode - 1%, WrapNode - 2%, TrueCapitalNode - 2%)

    "You try to create a new market trend by selling bubble wrap as a luxury item, but people are like 'meh, I can just buy regular bubble wrap for cheaper'":
    {WrapNode: [(WrapNode.mulValue, 1.02)],
     SoapNode: [(SoapNode.mulValue, 0.97)],
     TrueCapitalNode: [(TrueCapitalNode.mulValue, 0.99)],
     PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.99)]},
    # (Effect: WrapNode + 2%, SoapNode - 3%, TrueCapitalNode - 1%, PublicDoubtNode - 1%)

    "You partner with a social media influencer to promote your soap products, but they're actually just posting pictures of themselves wrapped in bubble wrap":
    {SoapNode: [(SoapNode.mulValue, 1.04)],
     WrapNode: [(WrapNode.mulValue, 1.03)],
     InvestorsDoubtNode: [(InvestorsDoubtNode.mulValue, 0.98)],
     TrueCapitalNode: [(TrueCapitalNode.mulValue, 0.98)]},
    # (Effect: SoapNode + 4%, WrapNode + 3%, InvestorsDoubtNode - 2%, TrueCapitalNode - 2%)

    "You invest in a new manufacturing process that replaces human labor with automated machines, but it's causing all the employees to get laid off and start a union":
    {InvestorsDoubtNode: [(InvestorsDoubtNode.mulValue, 1.08)],
     PublicDoubtNode: [(PublicDoubtNode.mulValue, 1.05)],
     TrueCapitalNode: [(TrueCapitalNode.mulValue, 0.90)],
     WrapNode: [(WrapNode.mulValue, 0.95)]},
    # (Effect: InvestorsDoubtNode + 8%, PublicDoubtNode + 5%, TrueCapitalNode - 10%, WrapNode - 5%)

    "You create a new line of 'craft' soaps that use only rare and expensive ingredients, but they're actually just regular soap with some fancy labels":
    {SoapNode: [(SoapNode.mulValue, 1.03)],
     WrapNode: [(WrapNode.mulValue, 0.99)],
     TrueCapitalNode: [(TrueCapitalNode.mulValue, 0.98)],
     PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.99)]},
    # (Effect: SoapNode + 3%, WrapNode - 1%, TrueCapitalNode - 2%, PublicDoubtNode - 1%)

    "You try to create a viral challenge by making people compete in bubble wrap unwrapping contests, but it's actually just a bunch of old people complaining about the state of society":
    {WrapNode: [(WrapNode.mulValue, 1.04)],
     InvestorsDoubtNode: [(InvestorsDoubtNode.mulValue, 0.97)],
     TrueCapitalNode: [(TrueCapitalNode.mulValue, 0.98)],
     PublicDoubtNode: [(PublicDoubtNode.mulValue, 1.05)]},
    # (Effect: WrapNode + 4%, InvestorsDoubtNode - 3%, TrueCapitalNode - 2%, PublicDoubtNode + 5%)

    "You start selling 'anti-bubble wrap' merchandise that's supposed to be ironic, but it's actually just regular clothes with a weird slogan on them":
    {SoapNode: [(SoapNode.mulValue, 0.99)],
     WrapNode: [(WrapNode.mulValue, 0.98)],
     TrueCapitalNode: [(TrueCapitalNode.mulValue, 0.99)],
     PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.98)]},
    # (Effect: SoapNode - 1%, WrapNode - 2%, TrueCapitalNode - 1%, PublicDoubtNode - 2%)

    
    ## Illegal
    
    "You partner with a notorious drug lord to produce and distribute a new designer soap that contains marijuana, creating a new business, but maybe not a good one.": {
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.1)],
        SoapNode: [(SoapNode.mulValue, 0.7)],
        WrapNode: [(WrapNode.mulValue, 1.05)],
        BeerNode: [(BeerNode.mulValue, 1.03)],
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.8)],
    },
    "You team up with a ruthless gun runner to smuggle soap into the country by hiding it in beer barrels, causing a surge in soap sales and confusion in the beer market.": {
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.15)],
        SoapNode: [(SoapNode.mulValue, 1.25)],
        WrapNode: [(WrapNode.mulValue, 1.05)],
        BeerNode: [(BeerNode.mulValue, 0.8)],
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.9)],
    },
    "You align with a powerful mafia boss to corner the bubble wrap market by threatening rival companies, forcing them out of business and leaving you in control of the entire industry.": {
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.2)],
        WrapNode: [(WrapNode.mulValue, 1.5)],
        SoapNode: [(SoapNode.mulValue, 1.05)],
        BeerNode: [(BeerNode.mulValue, 1.05)],
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.75)],
    },
    "You hire a mercenary squad to raid rival soap companies, stealing their secret formulas and using them to dominate the market while causing chaos in the beer industry.": {
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.3)],
        SoapNode: [(SoapNode.mulValue, 1.5)],
        WrapNode: [(WrapNode.mulValue, 1.05)],
        BeerNode: [(BeerNode.mulValue, 0.75)],
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.85)],
    },
    "You collude with corrupt officials to rig soap market prices, artificially inflating your profits while hurting small businesses and causing investor doubt.": {
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.1)],
        SoapNode: [(SoapNode.mulValue, 1.2)],
        WrapNode: [(WrapNode.mulValue, 1.03)],
        BeerNode: [(BeerNode.mulValue, 1.05)],
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.9)],
    },
    "You leverage connections with organized crime to monopolize the beer market by bribing officials, extorting competitors, and infiltrating distribution networks.": {
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.25)],
        SoapNode: [(SoapNode.mulValue, 1.05)],
        WrapNode: [(WrapNode.mulValue, 1.03)],
        BeerNode: [(BeerNode.mulValue, 0.7)],
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.8)],
    },
    "You partner with a dangerous cartel to produce a new designer soap that's highly addictive and illegal, flooding the market and causing chaos in law enforcement agencies.": {
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.15)],
        SoapNode: [(SoapNode.mulValue, 0.75)],
        WrapNode: [(WrapNode.mulValue, 1.05)],
        BeerNode: [(BeerNode.mulValue, 1.07)],
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.9)],
    },
    "You hire a team of cybercriminals to hack into rival soap companies' systems, stealing intellectual property and using it to dominate the market while causing chaos in the tech industry.": {
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.2)],
        SoapNode: [(SoapNode.mulValue, 1.3)],
        WrapNode: [(WrapNode.mulValue, 1.05)],
        BeerNode: [(BeerNode.mulValue, 1.1)],
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.85)],
    },
    "You start what you thought was a great campaign, artificially inflating your profits but causing public doubt about the integrity of the industry.": {
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.1)],
        SoapNode: [(SoapNode.mulValue, 1.2)],
        WrapNode: [(WrapNode.mulValue, 1.03)],
        BeerNode: [(BeerNode.mulValue, 1.05)],
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.85)],
    },
    "You pay off rival soap companies to sabotage their production facilities, allowing you to monopolize the market while causing chaos in the beer industry.": {
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.3)],
        SoapNode: [(SoapNode.mulValue, 1.5)],
        WrapNode: [(WrapNode.mulValue, 1.05)],
        BeerNode: [(BeerNode.mulValue, 0.75)],
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.85)],
    },
    "You work with a dangerous smuggling ring to import massive amounts of illegal soap into the country, flooding the market and causing chaos in law enforcement agencies.": {
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.2)],
        SoapNode: [(SoapNode.mulValue, 0.8)],
        WrapNode: [(WrapNode.mulValue, 1.3)],
        BeerNode: [(BeerNode.mulValue, 1.05)],
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.85)],
    },
    "You bribe government officials to approve a new type of transparent soap that is insanely dangerous, causing thousands to die before it's removed.": {
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.2)],
        SoapNode: [(SoapNode.mulValue, 1.2)],
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.75)],
    },
    "You form an alliance with a ruthless gang to monopolize the bubble wrap market by raiding competitors and spreading misinformation about product safety, causing investor doubt.": {
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.2)],
        SoapNode: [(SoapNode.mulValue, 1.05)],
        WrapNode: [(WrapNode.mulValue, 0.6)],
        BeerNode: [(BeerNode.mulValue, 1.07)],
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.8)],
    },
    "You forge alliances with international crime syndicates to monopolize the soap market by sabotaging competitors and spreading misinformation about product safety, causing investor doubt.": {
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.25)],
        SoapNode: [(SoapNode.mulValue, 0.6)],
        WrapNode: [(WrapNode.mulValue, 1.05)],
        BeerNode: [(BeerNode.mulValue, 1.1)],
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.7)],
    },
    "You become the head of an underground gun-running organization that also controls the distribution of a highly potent and addictive strain of craft beer, causing chaos and rising demand.": {
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.25)],
        BeerNode: [(BeerNode.mulValue, 1.3)],
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.8)],
    },
    "You form an alliance with international espionage agencies to monopolize the illicit arms trade while secretly producing a top-quality microbrew, creating a profitable black market.": {
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.3)],
        BeerNode: [(BeerNode.mulValue, 1.4)],
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.75)],
    },
    "You infiltrate rival gangs and governments by using your impressive beer-making skills as leverage, ultimately controlling both the illicit arms trade and the craft beer market.": {
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.35)],
        BeerNode: [(BeerNode.mulValue, 1.5)],
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.7)],
    },
    "You create a powerful spy organization that specializes in using high-quality beer as a means of communication and control, simultaneously monopolizing both the espionage industry and the beer market.": {
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.4)],
        BeerNode: [(BeerNode.mulValue, 1.5)],
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.65)],
    },
    "You leverage your expertise in crafting exotic beers to gain influence within organized crime syndicates, using their resources to establish a vast network of arms dealers and spies.": {
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.45)],
        BeerNode: [(BeerNode.mulValue, 1.4)],
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.6)],
    },
    "You infiltrate the highest levels of government by producing an addictive strain of beer that only top officials have access to, using their addiction as leverage over both the arms trade and espionage markets.": {
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.5)],
        BeerNode: [(BeerNode.mulValue, 1.3)],
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.55)],
    },
    "You form a secret society of elite spies and brewers who control both the international arms market and the lucrative craft beer industry, spreading misinformation and chaos to maintain their power.": {
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.55)],
        BeerNode: [(BeerNode.mulValue, 1.5)],
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.5)],
    },
    "You use your skill in brewing to forge alliances with rival gun runners and intelligence agencies, using the allure of your beer to gain control over both the illegal arms trade and espionage markets.": {
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.6)],
        BeerNode: [(BeerNode.mulValue, 1.6)],
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.45)],
    },
}
