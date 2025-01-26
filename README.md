# Economic Bubble

Want to experience what it is like to lead a company that scams people? Economic Bubble is the game for you! This is the game where you can trick your investors, spread fake rumors and create a mega monopoly by disrespecting all morals.

This is a game we made for APOIL's Global Game Jam 2025.

## Features

The features of the game include:
- Advanced economic modeling
- Full control over how you manage your business
- High performance on all systems
- Cross-platform compatibility 

## How to install

### Uncompiled version (Windows, Linux/Unix, MacOS)

**1. Install dependencies**

If you don't have Python installed, go to https://www.python.org/about/gettingstarted/ to install it.

If you do, open a terminal window and run the following commands:

```
pip install matplotlib
```

```
pip install pygame
```

```
pip install numpy
```

```
pip install curve
```


**2. Clone this repo into a folder of your choosing**

Open a terminal window and paste one of the commands below.

If you are not in your desired folder:

```
git clone https://github.com/Erocr/EconomicBubble REPLACE_THIS_WITH_YOUR_DESTINATION
```

if you are in your desired folder:

```
git clone https://github.com/Erocr/EconomicBubble
```

**3. Execute the program**

If you are in the folder where you cloned the repo, execute the following command in your terminal:

```
python3 main.py
```

If not, you can either go to the folder or use the following command:

```
python3 REPLACE_WITH_FULL_PATH/main.py
```

PRO TIP: If you want to make opening the game easier and you're on MacOS or Linux, make an alias by using ```alias EconomicBubble="python3 REPLACE_WITH_FULL_PATH/main.py".``` Once done, you can simply type ```EconomicBubble``` to run the game. Remember to actually replace "REPLACE_WITH_FULL_PATH" with the full path

If you get a "ModuleNotFound" error when you try to run the game, try to install the missing module(s) by using 

```
pip install REPLACE_WITH_MODULE_NAME
```


## How to play

Your company sells soap, beer and wraps. The goal of the game is to make as much money as possible without people knowing that you're scamming them. The economic model is designed to make it impossible to succeed without scamming people, so you're forced to put aside your morals.

There are three activities you can invest in:
- Marketing: Makes the public like you and less likely to doubt your company
- Security: Lowers the chance of your crimes getting discovered
- Espionnage: Allows your company to get ahead of competitors by stealing their discoveries, but if discovered it can make the public doubt you

There are a couple of important metrics:
- Actual capital: The amount of money your company actually has.
- Shown capital: The amount of money your investors and the general public think your company has
- Public doubt: Represents the amount of skepticism surrounding your company amongst the public
- Investor doubt: Represents the amount of skepticism surrounding your company amongst the investors
- The prices of the products you're selling

You lose the game if:
- Public doubt reaches 100%
- Investor doubt reaches 100%
- Your true capital reaches zero