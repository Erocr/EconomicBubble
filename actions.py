class Actions :
    def __init__(self, TC, W, S, B, PD, ID, SN):
        TrueCapitalNode = TC
        WrapNode = W
        SoapNode = S
        BeerNode = B
        PublicDoubtNode = PD
        InvestorsDoubtNode = ID
        SecurityNode = SN

        self.actions = {
        "You create a viral social media campaign featuring your soap products being used creatively, resulting in increased sales and public engagement":
        {TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.10)],
        WrapNode: [(WrapNode.increment_max_price, 106)],
        SoapNode: [(SoapNode.mulValue, 1.08)],
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.90)]
        },
        # (Effect: TrueCapitalNode + 10%, WrapNode + 6%, SoapNode + 8%, PublicDoubtNode - 10%)

        "You host an 'open house' event showcasing your bubble wrap-themed office decor, drawing in new clients and boosting morale":  
        {WrapNode: [(WrapNode.mulValue, 1.08)],  
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.90)],  
        SoapNode: [(SoapNode.mulValue, 1.02)]  
        },
        # (Effect: WrapNode + 8%, PublicDoubtNode - 10%, SoapNode + 2%)

        "You decide to rebrand your soap company as 'Bubble Wrap Soaps,' attracting investor excitement with the creative twist":
        {InvestorsDoubtNode: [(InvestorsDoubtNode.mulValue, 0.90)],
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.06)],
        WrapNode: [(WrapNode.mulValue, 1.10)],
        SoapNode: [(SoapNode.increment_min_price, 107)]
        },
        # (Effect: InvestorsDoubtNode - 10%, TrueCapitalNode + 6%, WrapNode + 10%, SoapNode + 7%)

        "You buy an entire warehouse full of bubble wrap and convert it into a pop-up museum, becoming a cultural sensation":  
        {WrapNode: [(WrapNode.mulValue, 1.12)],  
        InvestorsDoubtNode: [(InvestorsDoubtNode.mulValue, 0.92)],  
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.10)]  
        },
        # (Effect: WrapNode + 12%, InvestorsDoubtNode - 8%, TrueCapitalNode + 10%)

        "You accidentally order 1000 cases of beer for a party, and it becomes a viral event that boosts your brand's image":  
        {BeerNode: [(BeerNode.mulValue, 1.10)],  
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.08)],  
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.90)]  
        },
        # (Effect: BeerNode + 10%, TrueCapitalNode + 8%, PublicDoubtNode - 10%)

        "You start selling soap-shaped whoopee cushions as a novelty item, and they become a huge success at trade shows":  
        {SoapNode: [(SoapNode.mulValue, 3.15)],  
        WrapNode: [(WrapNode.increment_min_price, -100)],
        BeerNode: [(BeerNode.increment_min_price, -300)],
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.10)],  
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.95)]  
        },
        # (Effect: SoapNode + 15%, WrapNode + 2%, BeerNode + 3%, TrueCapitalNode + 10%, PublicDoubtNode - 5%)

        "You create a viral challenge where people wrap themselves in bubble wrap creatively, bringing positive attention to your brand":
        {WrapNode: [(WrapNode.mulValue, 1.15)],  
        InvestorsDoubtNode: [(InvestorsDoubtNode.mulValue, 0.90)],  
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.08)],  
        SoapNode: [(SoapNode.mulValue, 1.05)]  
        },
        # (Effect: WrapNode + 15%, InvestorsDoubtNode - 10%, TrueCapitalNode + 8%, SoapNode + 5%)

        "You partner with a rival company to co-create a beer-infused soap, which becomes a popular novelty item in stores":
        {BeerNode: [(BeerNode.increment_max_price, 110)],
        SoapNode: [(SoapNode.mulValue, 1.10)],
        WrapNode: [(WrapNode.mulValue, 1.05)],
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.08)]
        },
        # (Effect: BeerNode + 10%, SoapNode + 10%, WrapNode + 5%, TrueCapitalNode + 8%)

        "You decide to replace manual labor with automated bubble wrap dispensers, which speeds up production and cuts costs":
        {InvestorsDoubtNode: [(InvestorsDoubtNode.mulValue, 0.90)],  
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.95)],  
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.12)],  
        WrapNode: [(WrapNode.mulValue, 1.10)]  
        },
        # (Effect: InvestorsDoubtNode - 10%, PublicDoubtNode - 5%, TrueCapitalNode + 12%, WrapNode + 10%)

        "You host a 'soap-making' workshop for kids, sparking creativity and bringing new customers to your brand":  
        {SoapNode: [(SoapNode.mulValue, 1.10)],  
        WrapNode: [(WrapNode.increment_min_price, -106)],
        InvestorsDoubtNode: [(InvestorsDoubtNode.mulValue, 0.92)],  
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.08)]},  
        # (Effect: SoapNode + 10%, WrapNode + 6%, InvestorsDoubtNode - 8%, TrueCapitalNode + 8%)

        "You invest in a beer brewery specializing in beers with unique ingredients, gaining a loyal following for creativity":  
        {BeerNode: [(BeerNode.mulValue, 1.15)],  
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.90)],  
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.08)],  
        InvestorsDoubtNode: [(InvestorsDoubtNode.mulValue, 0.95)]},  
        # (Effect: BeerNode + 15%, PublicDoubtNode - 10%, TrueCapitalNode + 8%, InvestorsDoubtNode - 5%)

        "You create an 'eco-friendly bubble wrap' movement, reducing plastic use and earning praise for sustainability":  
        {WrapNode: [(WrapNode.increment_max_price, 115)],
        SoapNode: [(SoapNode.increment_max_price, 208)],
        TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.12)],  
        PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.85)]},  
        # (Effect: WrapNode + 15%, SoapNode + 8%, TrueCapitalNode + 12%, PublicDoubtNode - 15%)
        }


        
        
        self.illegal = {
            "You partner with a notorious drug lord to produce and distribute a new designer soap that contains marijuana, creating a new business, but maybe not a good one.": {
                    TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.1)],
                    SoapNode: [(SoapNode.increment_min_price, -300)],
                    WrapNode: [(WrapNode.mulValue, 1.05)],
                    BeerNode: [(BeerNode.mulValue, 1.03)],
                    PublicDoubtNode: [(PublicDoubtNode.mulValue, 1.8), (PublicDoubtNode.incrementDoubt, 9)],
                },
                "You team up with a ruthless gun runner to smuggle soap into the country by hiding it in beer barrels, causing a surge in soap sales and confusion in the beer market.": {
                    TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.15)],
                    SoapNode: [(SoapNode.increment_max_price, 80)],
                    WrapNode: [(WrapNode.increment_max_price, 70)],
                    BeerNode: [(SoapNode.increment_min_price, -100)],
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
                    SoapNode: [(SoapNode.increment_max_price, 1500)],
                    WrapNode: [(WrapNode.mulValue, 1.05)],
                    BeerNode: [(BeerNode.increment_min_price, -750)],
                    PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.85)],
                },
                "You collude with corrupt officials to rig soap market prices, artificially inflating your profits while hurting small businesses and causing investor doubt.": {
                    TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.1)],
                    SoapNode: [(SoapNode.increment_max_price, 1200)],
                    WrapNode: [(WrapNode.increment_min_price, -503)],
                    BeerNode: [(BeerNode.mulValue, 1.05)],
                    PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.9)],
                },
                "You leverage connections with organized crime to monopolize the beer market by bribing officials, extorting competitors, and infiltrating distribution networks.": {
                    TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.25)],
                    SoapNode: [(SoapNode.increment_max_price, 110.5)],
                    WrapNode: [(WrapNode.mulValue, 1.03)],
                    BeerNode: [(BeerNode.increment_min_price, -1700)],
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
                    SoapNode: [(SoapNode.increment_max_price, 15)],
                    WrapNode: [(WrapNode.mulValue, 1.05)],
                    BeerNode: [(BeerNode.mulValue, 0.75)],
                    PublicDoubtNode: [(PublicDoubtNode.mulValue, 0.85)],
                },
                "You work with a dangerous smuggling ring to import massive amounts of illegal soap into the country, flooding the market and causing chaos in law enforcement agencies.": {
                    TrueCapitalNode: [(TrueCapitalNode.mulValue, 1.2)],
                    SoapNode: [(SoapNode.increment_min_price, -18)],
                    WrapNode: [(WrapNode.increment_max_price, 13)],
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
                }
        }

        self.surveillance =  {
            "Surveillance": {
                SecurityNode: [(SecurityNode.monitor, 0)]
            },
            "Legal Defense": {
                SecurityNode: [(SecurityNode.add_defense_team, 1)]
            }
        }

        self.questions = {}

        self.all_actions = self.actions | self.illegal | self.surveillance | self.questions

