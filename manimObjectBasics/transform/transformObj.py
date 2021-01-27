from manim import *


class transformBasics(Scene):
    """
    Copy M2, and play M1
    """

    def construct(self):
        m1 = TexMobject("A")
        m2 = TexMobject("B")
        m3 = TexMobject("C")
        m4 = TexMobject("D")

        # Canvas: add m1
        self.add(m1)
        self.wait()

        # Copy M2's value into M1
        self.play(Transform(m1, m2))
        self.wait()

        self.play(Transform(m1, m3))
        self.wait()
        self.play(Transform(m1, m4))
        self.wait()

        self.play(FadeOut(m1))


class replacementTransform(Scene):
    """
    Copy M2, and play M2
    """

    def construct(self):
        m1 = TexMobject("A")
        m2 = TexMobject("B")
        m3 = TexMobject("C")
        m4 = TexMobject("D")

        # Canvas: add m1
        self.add(m1)
        self.wait()

        # Copy M2 and play M2
        self.play(ReplacementTransform(m1, m2))
        self.wait()

        self.play(ReplacementTransform(m1, m3))
        self.wait()
        self.play(ReplacementTransform(m1, m4))
        self.wait()

        self.play(FadeOut(m1))
