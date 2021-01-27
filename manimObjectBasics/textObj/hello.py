from manim import *


class HelloWorld(Scene):
    def construct(self):
        text = Text('Hello world').scale(3)
        self.add(text)
        self.wait()


class TextAlignment(Scene):
    def construct(self):
        title = Text("K-means clustering and Logistic Regression", color=WHITE)
        title.scale_in_place(0.75)
        self.add(title.to_edge(UP))

        t1 = Text("1. Measuring").set_color(WHITE)
        t1.next_to(ORIGIN, direction=RIGHT, aligned_edge=UP)

        t2 = Text("2. Clustering").set_color(WHITE)
        t2.next_to(t1, direction=DOWN, aligned_edge=LEFT)

        t3 = Text("3. Regression").set_color(WHITE)
        t3.next_to(t2, direction=DOWN, aligned_edge=LEFT)

        t4 = Text("4. Prediction").set_color(WHITE)
        t4.next_to(t3, direction=DOWN, aligned_edge=LEFT)

        x = VGroup(t1, t2, t3, t4).scale_in_place(0.7)
        x.set_opacity(0.5)
        x.submobjects[1].set_opacity(1)
        self.add(x)
        self.wait()
