from bubble import Bubble
from vec import Vec


class Game:
    def __init__(self, view):
        self.view = view
        default_fill = 0.25
        sc = view.screenSize
        string_shown_capital = f"Shown capital: {0}$"
        string_true_capital = f"True capital: {0}$"

        ratio = sc.size / (1100**2 + 700**2)**(1/2)
        # Triangle of marketing, espionnage and security
        bubble_size_big = 90 * ratio
        mid_triangle_pos = view.screenSize / Vec(4.5, 2.6)
        pos_marketing = mid_triangle_pos - Vec(0, sc.get[1] / 11)
        pos_espionnage = mid_triangle_pos + \
            sc / Vec(sc.get[0], 7) - Vec(sc.get[0] / 9, 0)
        pos_security = mid_triangle_pos + \
            sc / Vec(sc.get[0], 7) + Vec(sc.get[0] / 9, 0)

        # Investing possibilities
        bubble_size_investing = 50 * ratio
        pos_invest_center = sc / Vec(1.4, 1.7)
        pos_invest_left = pos_invest_center - Vec(sc.get[0] / 9, 0)
        pos_invest_right = pos_invest_center + Vec(sc.get[0] / 9, 0)

        # Capital
        bubble_size_capital = 70 * ratio
        mid_capital_pos = sc / \
            Vec(2, 2) - Vec(0, sc.get[1] / 2) + Vec(0,
                                                    bubble_size_capital) + Vec(0, sc.get[1]/100)
        pos_shown_capital = mid_capital_pos - Vec(sc.get[0]/10, 0)
        pos_true_capital = mid_capital_pos + Vec(sc.get[0]/10, 0)

        self.bubbles = [
            Bubble(bubble_size_big, pos_marketing, default_fill,
                   "Marketing", (0, 0, 255), (0, 255, 255)),
            Bubble(bubble_size_big, pos_espionnage, default_fill,
                   "Espionnage", (50, 0, 0), (100, 0, 0)),
            Bubble(bubble_size_big, pos_security, default_fill, "Security",
                   (255, 0, 0), (255, 100, 100)),

            Bubble(bubble_size_investing, pos_invest_left, default_fill, "Soap",
                   (95, 167, 120), (206, 200, 239)),

            Bubble(bubble_size_investing, pos_invest_center, default_fill, "Beer",
                   (185, 113, 31), (242, 142, 28)),

            Bubble(bubble_size_investing, pos_invest_right, default_fill, "Soap Opera",
                   (246, 108, 164), (245, 197, 217)),

            Bubble(bubble_size_capital, pos_shown_capital, default_fill,
                   string_shown_capital,  (7, 37, 6), (133, 187, 101)),

            Bubble(bubble_size_capital, pos_true_capital, default_fill,
                   string_true_capital,  (7, 37, 6), (133, 187, 101)),
        ]

    def update(self, inputs):
        for bubble in self.bubbles:
            bubble.update(inputs)

    def draw(self, view):
        for bubble in self.bubbles:
            bubble.draw(view)
