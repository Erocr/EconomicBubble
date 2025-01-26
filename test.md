# list of functions to modify the economy:

Node.mulValue est defini dans baseNode!!!!! il fait tjr la meme chose

TrueCapitalNode.incrementCapital(increment) # increment can be negative

ApparentCapitalNode.incrementCapital(increment) # increment can be negative

ApparentCapitalNode.incrementPersuasion(increment) # must be positive, between 0 and 1

# MarketNode means one of (soap, beer, wrap)
MarketNode.incrementMaxPrice(increment) # increment can be negative, advised to be between roughly -2 and 2 ( can be more, no problem)

MarketNode.incrementMinPrice(increment) # increment can be positive, advised to be between roughly -2 and 2 ( can be more, no problem)

# will be brutal: good to simulate an economic crash or a very sudden increase
MarketNode.mulValue(mul) # multiply market price by value (does nothing if value is being capped), (be careful, if market price is negative it makes them go even lower)

MarketNode.incrementTendance(increment) #between -... and ...

PublicDoubtNode.incrementDoubt(increment) # between -100 and 100

PublicDoubtNode.incrementVolatility(increment) # between -15 and 15

