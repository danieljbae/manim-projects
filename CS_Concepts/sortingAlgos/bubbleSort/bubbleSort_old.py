from manim import *


class psuedoCode(Scene):
    def construct(self):
        code0 = Code(
            file_name=".\\1.CS_Concepts\\bubbleSortAlgo.py",
            background="window",  # rectangle
            tab_width=4,
            background_stroke_color=WHITE,
            insert_line_no=False,
            # style=Code.styles_list[15],
            language="py",
        )

        # code0[1]
        # snippet = code0.line_numbers()
        self.play(Write(code0))
        self.wait()


class pairsBox(Scene):
    def construct(self):
        pass


class arrayContainer(Scene):
    def construct(self):
        sq1 = Square(side_length=1)
        sq2 = Square(side_length=1)
        sq3 = Square(side_length=1)
        sq4 = Square(side_length=1)
        sq5 = Square(side_length=1)
        self.add(sq1, sq2, sq3, sq4, sq5)

        # for i, mobj in enumerate(self.mobjects):
        #     mobj.shift(i * RIGHT)
        #     self.play(Write(SurroundingRectangle(mobj)))

        arrayObj = Group(sq1, sq2, sq3, sq4, sq5)
        self.play((Write(arrayObj)))

        self.wait()


class AddtoVGroup(Scene):
    def construct(self):
        circle_red = Circle(color=RED)
        circle_green = Circle(color=GREEN)
        circle_blue = Circle(color=BLUE)
        circle_red.shift(LEFT)
        circle_blue.shift(RIGHT)
        gr = VGroup(circle_red, circle_green)
        gr2 = VGroup(circle_blue)  # Constructor uses add directly
        self.add(gr, gr2)
        self.wait()
        gr += gr2  # Add group to another
        self.play(
            gr.animate.shift(DOWN),
        )
        gr -= gr2  # Remove group
        self.play(  # Animate groups separately
            gr.animate.shift(LEFT),
            gr2.animate.shift(UP),
        )
        self.play(  # Animate groups without modification
            (gr+gr2).animate.shift(RIGHT)
        )
        self.play(  # Animate group without component
            (gr-circle_red).animate.shift(RIGHT)
        )


class VariablesWithValueTracker(Scene):
    def construct(self):
        var = 0.5
        on_screen_var = Variable(var, Text("var"), num_decimal_places=3)

        # You can also change the colours for the label and value
        on_screen_var.label.set_color(RED)
        on_screen_var.value.set_color(GREEN)

        self.play(Write(on_screen_var))
        # The above line will just display the variable with
        # its initial value on the screen. If you also wish to
        # update it, you can do so by accessing the `tracker` attribute
        self.wait()
        var_tracker = on_screen_var.tracker
        var = 10.5
        self.play(var_tracker.animate.set_value(var))
        self.wait()

        int_var = 0
        on_screen_int_var = Variable(
            int_var, Text("int_var"), var_type=Integer
        ).next_to(on_screen_var, DOWN)
        on_screen_int_var.label.set_color(RED)
        on_screen_int_var.value.set_color(GREEN)

        self.play(Write(on_screen_int_var))
        self.wait()
        var_tracker = on_screen_int_var.tracker
        var = 10.5
        self.play(var_tracker.animate.set_value(var))
        self.wait()

        # If you wish to have a somewhat more complicated label for your
        # variable with subscripts, superscripts, etc. the default class
        # for the label is MathTex
        subscript_label_var = 10
        on_screen_subscript_var = Variable(subscript_label_var, "{a}_{i}").next_to(
            on_screen_int_var, DOWN
        )
        self.play(Write(on_screen_subscript_var))
        self.wait()
