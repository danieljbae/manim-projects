from manim import *


class TransformationText2(Scene):
    def construct(self):
        text1 = TextMobject("Function")
        text2 = TextMobject("Derivative")
        text3 = TextMobject("Integral")
        text4 = TextMobject("Transformation")
        self.play(Write(text1))
        self.wait()
        # Trans text1 -> text2
        self.play(ReplacementTransform(text1, text2))
        self.wait()
        # Trans text2 -> text3
        self.play(ReplacementTransform(text2, text3))
        self.wait()
        # Trans text3 -> text4
        self.play(ReplacementTransform(text3, text4))
        self.wait()


class CopyTextV1(Scene):
    """
    Reveal Hidden part of Array:

    Copy Transform when you want Reveal "Hidden" part of array
    By Mapping or Transforming values to it 
    """

    def construct(self):
        formula = TexMobject(
            "\\frac{d}{dx}",  # 0
            "(",  # 1
            "u",  # 2
            "+",  # 3
            "v",  # 4
            ")",  # 5
            "=",  # 6

            # Hidden part of formula array
            "\\frac{d}{dx}",  # 7
            "xxx",  # 8
            "+",  # 9
            "\\frac{d}{dx}",  # 10
            "v"  # 11
        )
        formula.scale(2)

        # Write LHS [0:7]
        self.play(Write(formula[0:7]))
        self.wait()

        # Copy Tranform: Reveal RHS [8:11]
        self.play(
            ReplacementTransform(formula[2].copy(), formula[8]),
            ReplacementTransform(formula[4].copy(), formula[11]),
            ReplacementTransform(formula[3].copy(), formula[9])
        )
        self.wait()
        self.play(
            ReplacementTransform(formula[0].copy(), formula[7]),
            ReplacementTransform(formula[0].copy(), formula[10])
        )
        self.wait()


class CopyTextV4(Scene):
    """
    Reveal Hidden part of Array associated by Color
    """

    def construct(self):
        formula = TexMobject("\\frac{d}{dx}",
                             "(", "u", "+", "v", ")", "=",
                             "\\frac{d}{dx}", "u", "+", "\\frac{d}{dx}", "v"
                             )
        formula.scale(2)
        for letter, color in [("u", RED), ("v", BLUE)]:
            formula.set_color_by_tex(letter, color)
        self.play(Write(formula[0:7]))
        self.wait()
        self.play(
            ReplacementTransform(formula[2].copy(), formula[8]),
            ReplacementTransform(formula[4].copy(), formula[11]),
            ReplacementTransform(formula[3].copy(), formula[9]),
            run_time=3
        )
        self.wait()
        self.play(
            ReplacementTransform(formula[0].copy(), formula[7]),
            ReplacementTransform(formula[0].copy(), formula[10]),
            run_time=3
        )
        self.wait()


class CopyTwoFormulas2(Scene):
    def construct(self):
        formula1 = TexMobject(
            "\\neg", "\\forall", "x", ":", "P(x)"
        )
        formula2 = TexMobject(
            "\\exists", "x", ":", "\\neg", "P(x)"
        )
        for tam, pos, formula in [(2, 2*UP, formula1), (2, 2*DOWN, formula2)]:
            formula.scale(tam)
            formula.move_to(pos)
        self.play(Write(formula1))
        self.wait()
        changes = [
            # First time
            [(2, 3, 4),
             # | | |
             # v v v
             (1, 2, 4)],
            # Second time
            [(0,),
             # |
             # v
             (3,)],
            # Third time
            [(1,),
             # |
             # v
             (0,)]
        ]
        for pre_ind, post_ind in changes:
            self.play(*[
                ReplacementTransform(
                    formula1[i].copy(), formula2[j]
                )
                for i, j in zip(pre_ind, post_ind)
            ],
                run_time=2
            )
            self.wait()


class ChangeTextColorAnimation(Scene):
    def construct(self):
        text = TextMobject("Text")
        text.scale(3)
        self.play(Write(text))
        self.wait()
        self.play(
            text.set_color, YELLOW,
            run_time=2
        )
        self.wait()


class ChangeSizeAnimation(Scene):
    def construct(self):
        text = TextMobject("Text")
        text.scale(2)
        self.play(Write(text))
        self.wait()
        self.play(
            text.scale, 3,
            run_time=2
        )
        self.wait()


class MoveText(Scene):
    def construct(self):
        text = TextMobject("Text")
        text.scale(2)
        text.shift(LEFT*2)
        self.play(Write(text))
        self.wait()
        self.play(
            text.shift, RIGHT*2,
            run_time=2,
            path_arc=0  # Change 0 by -np.pi
        )
        self.wait()


class ChangeColorAndSizeAnimation(Scene):
    def construct(self):
        text = TextMobject("Text")
        text.scale(2)
        text.shift(LEFT*2)
        self.play(Write(text))
        self.wait()
        self.play(
            text.shift, RIGHT*2,
            text.scale, 2,
            text.set_color, RED,
            run_time=2,
        )
        self.wait()
