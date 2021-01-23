from manim import *

# M Objects (math object) are the basic building blocks to manim
# More Complicated objects build off M Objects (ex. Axes, FunctionGraph, or BarChart)


class createCircle(Scene):
    """
    Creating and displaying mobjects¶
    """

    def construct(self):
        circle = Circle()                   # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency

        self.add(circle)
        self.wait(1)
        self.remove(circle)
        self.wait(1)


class manyObjects(Scene):
    """
    Simple orientation
    """

    def construct(self):
        triangle = Triangle()
        square = Square()
        circle = Circle()

        circle.shift(LEFT)
        triangle.shift(UP)
        square.shift(RIGHT)

        self.play(ShowCreation(circle))
        self.play(ShowCreation(square))
        self.play(ShowCreation(triangle))   # show the circle on screen


class MobjectPlacement(Scene):
    """
    Relative placement to other objects
    """

    def construct(self):
        circle = Circle()
        square = Square()
        triangle = Triangle()

        # place the circle two units left from the origin
        circle.move_to(LEFT * 2)
        # place the square to the left of the circle
        square.next_to(circle, LEFT)
        # align the left border of the triangle to the left border of the circle
        triangle.align_to(circle, LEFT)

        self.add(circle, square, triangle)
        self.wait(1)


class MobjectStyling(Scene):
    """
    Styling: Interior and Exterior 
    """

    def construct(self):
        circle = Circle().shift(LEFT)               # Suggested: Chain Methods
        square = Square().shift(UP)
        triangle = Triangle().shift(RIGHT)

        circle.set_stroke(color=GREEN, width=20)    # stroke: Styles Exterior (ex. circle to ring)
        square.set_fill(YELLOW, opacity=1.0)        # fill: Styles Interior
        triangle.set_fill(PINK, opacity=0.5)

        self.add(circle, square, triangle)
        # self.add(triangle, circle, square)          # Overlay Ordering of objects
        self.wait(1)


class SomeAnimations(Scene):
    """
    In general, Animation Methods: interpolate (transition) between 2 mobjects
    (ex. FadeIn: Starts with fully transparent square -> gradually increases opacity -> Ends with fully opaque)
    """

    def construct(self):
        square = Square()
        self.add(square)

        # some animations display mobjects, ...
        self.play(FadeIn(square))

        # ... some move or rotate mobjects around...
        self.play(Rotate(square, PI/4))

        # some animations remove mobjects from the screen
        self.play(FadeOut(square))

        self.wait(1)


class RunTime(Scene):
    """
    Manually setting duration of animation scene
    """

    def construct(self):
        square = Square()
        self.add(square)
        self.play(ApplyMethod(square.shift, UP), run_time=3)
        self.wait(1)
