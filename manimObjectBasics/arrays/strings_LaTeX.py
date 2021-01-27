from manim import *

# Based off manim-ce Tutorial series, code found below
# Source: https://github.com/Elteoremadebeethoven/AnimationsWithManim/blob/master/English/3_text_like_arrays/3_text_like_arrays.py


class FormulaColor(Scene):
    """
    LaTeX use: MathTex or TexMobject (See @CrossText1)
    """

    def construct(self):
        formula = MathTex("\\sqrt{", "{\\left(", "{x", "\\over", "y}", "\\right)}", "d", "x", ".}")
        formula[0].set_color(YELLOW)
        formula[1].set_color(YELLOW)
        formula[2].set_color(WHITE)
        formula[3].set_color(BLUE)
        formula[4].set_color(WHITE)
        formula[5].set_color(RED)
        formula[6].set_color(WHITE)
        formula[7].set_color(WHITE)
        formula[8].set_color(BLUE)

        self.play(Write(formula))
        self.wait(2)


class ForRange(Scene):
    """
    Putting it all together
    """

    def construct(self):
        vals = TextMobject("3", "8", "12", "15", "16", "19").scale(2)
        idx = TextMobject("[0] ", "[1] ", "[2] ", "[3] ", "[4] ", "[5]").scale(1.5)

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


class ZipRange(Scene):
    def construct(self):
        vals = TextMobject("3", "8", "12", "15", "16", "19").scale(2)
        idx = TextMobject("[0] ", "[1] ", "[2] ", "[3] ", "[4] ", "[5]").scale(1.5)

        for i, color in zip([2, 3, 4], [GREEN, YELLOW, BLUE]):
            vals[i].set_color(color)
            idx[i].set_color(color)

        idx.next_to(vals.get_center(), direction=DOWN, buff=.70)
        self.add(vals, idx)
        self.wait(3)


class CrossText1(Scene):
    def construct(self):
        """
        Write text first, wait then cross off
        """
        text = TexMobject("\\sum_{i=1}^{n}i", "=", "-\\frac{1}{2}")

        cross = Cross(text[2])
        cross.set_stroke(RED, 7)
        self.play(Write(text))
        self.wait(2)
        self.play(ShowCreation(cross))
        self.wait(2)


class FrameBox2(Scene):
    """
    Emphasize subarray via  FrameBox
    """

    def construct(self):
        text = TexMobject(
            "\\hat g(", "f", ")", "=", "\\int", "_{t_1}", "^{t_{2}}",
            "g(", "t", ")", "e", "^{-2\\pi i", "f", "t}", "dt"
        )
        seleccion = VGroup(text[4], text[5], text[6])
        frameBox = SurroundingRectangle(seleccion, buff=0.5*SMALL_BUFF)
        frameBox.set_stroke(GREEN, 9)
        self.play(Write(text))
        self.wait(.5)
        self.play(ShowCreation(frameBox))
        self.wait(2)


class BraceText(Scene):
    """
    Emphasize subarray via brackets
    """

    def construct(self):
        text = TexMobject(
            "\\frac{d}{dx}f(x)g(x)=", "f(x)\\frac{d}{dx}g(x)", "+",
            "g(x)\\frac{d}{dx}f(x)"
        )
        self.play(Write(text))
        brace_top = Brace(text[1], UP, buff=SMALL_BUFF)
        brace_bottom = Brace(text[3], DOWN, buff=SMALL_BUFF)
        text_top = brace_top.get_text("$g'f$")
        text_bottom = brace_bottom.get_text("$f'g$")
        self.play(
            GrowFromCenter(brace_top),
            GrowFromCenter(brace_bottom),
            FadeIn(text_top),
            FadeIn(text_bottom)
        )
        self.wait()
