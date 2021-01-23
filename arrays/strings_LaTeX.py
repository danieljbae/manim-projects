from manim import *


class TextColor(Scene):
    def construct(self):
        text = TextMobject("A", "B", "C", "D")

        text[0].set_color(RED)
        text[1].set_color(BLUE)
        text[2].set_color(GREEN)
        text[3].set_color(ORANGE)

        self.play(Write(text))
        self.wait(2)


class FormulaColor(Scene):
    def construct(self):
        formula = MathTex("x", "=", "{a", "\\over", "b}")

        formula[0].set_color(GREEN)
        formula[1].set_color(WHITE)
        formula[2].set_color(RED)
        formula[3].set_color(GRAY)
        formula[4].set_color(BLUE)

        self.play(Write(formula))
        self.wait(2)


class ForRange(Scene):
    """
    Values and Indices 
    """

    def construct(self):
        vals = TextMobject("3, ", "8, ", "12, ", "15, ", "16, ", "19")
        idx = TextMobject("[0] ", "[1] ", "[2] ", "[3] ", "[4] ", "[5]")

        for i in range(6):
            if i % 2:
                vals[i].set_color(YELLOW)
                idx[i].set_color(YELLOW)
            else:
                vals[i].set_color(GREEN)
                idx[i].set_color(GREEN)

        idx.next_to(vals.get_center(), direction=DOWN, buff=.70)
        self.add(vals, idx)
        self.wait(3)
