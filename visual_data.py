from vec import Vec


class VisualData:
    def __init__(self, view):
        self.view = view
        self.default_fill = 0.25
        self.sc = view.screenSize

        self.ratio = self.sc.size / (1100**2 + 700**2)**(1/2)
        # Triangle of marketing, espionnage and security
        self.bubble_size_big = 90 * self.ratio
        self.mid_triangle_pos = self.view.screenSize / Vec(4.5, 2.6)
        self.pos_marketing = self.mid_triangle_pos - \
            Vec(0, self.sc.get[1] / 11)
        self.pos_espionnage = self.mid_triangle_pos + \
            self.sc / Vec(self.sc.get[0], 7) - Vec(self.sc.get[0] / 9, 0)
        self.pos_security = self.mid_triangle_pos + \
            self.sc / Vec(self.sc.get[0], 7) + Vec(self.sc.get[0] / 9, 0)

        # Investing possibilities
        self.bubble_size_investing = 50 * self.ratio
        self.pos_invest_center = self.sc / Vec(1.4, 1.7)
        self.pos_invest_left = self.pos_invest_center - \
            Vec(self.sc.get[0] / 9, 0)
        self.pos_invest_right = self.pos_invest_center + \
            Vec(self.sc.get[0] / 9, 0)

        # Capital
        self.bubble_size_capital = 70 * self.ratio
        self.mid_capital_pos = self.sc / \
            Vec(2, 2) - Vec(0, self.sc.get[1] / 2) + Vec(0,
                                                         self.bubble_size_capital) + Vec(0, self.sc.get[1]/100)
        self.pos_shown_capital = self.mid_capital_pos - \
            Vec(self.sc.get[0]/10, 0)
        self.pos_true_capital = self.mid_capital_pos + \
            Vec(self.sc.get[0]/10, 0)

        # Doubt
        self.bubble_size_doubt = 50 * self.ratio
        self.pos_investor_doubt = Vec(
            self.sc.get[0], 0) + Vec(- self.sc.get[0], self.sc.get[1]) / Vec(12, 12)
        self.pos_public_doubt = self.pos_investor_doubt + \
            Vec(0, self.bubble_size_doubt*2) + Vec(0, self.sc.get[1]/30)
