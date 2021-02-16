from manim import *
# from src.arrayObj import


class showArray(Scene):
    def construct(self):
        #######################################
        # export to arrayObj.py
        self.pointer_color = YELLOW
        self.box_color = BLUE_C
        self.nums = [5, 2, 6, 4, 1, 3]  # simpleConfig
        #######################################
        self.showTitle("Bubble Sort")
        self.showArray(self.nums)

    def showTitle(self, titleText):
        title = TextMobject(titleText).to_edge(UP).scale(1.5)
        self.play(
            Write(title)
        )
        self.wait()

    def buildArray(self, nums):
        '''
        Builds array mobjects (boxes and text values)
        Packs array mobjects into VGroups
        '''

        # Build array box mobjects
        boxes = []
        for i in range(len(nums)):
            boxes.append(
                Square(side_length=1, color=self.box_color).move_to(2 * LEFT + i * RIGHT)
            )
        self.boxes = boxes

        # Build array value mobjects
        values = []
        for i in range(len(nums)):
            numText = str(nums[i])
            values.append(TextMobject(numText).move_to(2 * LEFT + i * RIGHT))

        # Aggregate mobjects
        boxes_mobj = VGroup(*boxes)
        values_mobj = VGroup(*values)
        self.array_mobj = VGroup(boxes_mobj, values_mobj)
        return boxes_mobj, values_mobj

    def showArray(self, nums):
        '''
        Display creation of array
        '''
        boxes_mobj, values_mobj = self.buildArray(nums)
        self.play(
            AnimationGroup(
                *[ShowCreation(mob) for mob in boxes_mobj],
                *[ShowCreation(mob) for mob in values_mobj],
                run_time=5,
                lag_ratio=0.2
            )
        )

        brace = Brace(self.array_mobj, DOWN)
        braceText = brace.get_text(f"n = {len(self.nums)}")

        self.play(
            GrowFromCenter(brace),
            Write(braceText),
        )

        self.wait()

        self.play(
            FadeOut(brace),
            FadeOut(braceText),
        )

    def doSort(self):
        array = self.array
        array.generate_target()
        array.target.shift(UP)

        self.play(MoveToTarget(array))

        self.pointer = RegularPolygon(3, start_angle=-PI/2, color=self.pointer_color,
                                      fill_opacity=1).scale(0.2).next_to(self.boxes[0], UP)

        self.play(ShowCreation(self.pointer))

        self._comparison_1()
        self._comparison_2()
        self._comparison_3()
        self._comparison_4()
        self._comparison_5()
        self._comparison_6()
        self._comparison_7()
        self._comparison_8()
        self._comparison_9()
        self._comparison_10()

        self.play(FadeOut(self.pointer))

        self._activateArray()

        array.generate_target()
        array.target.shift(DOWN)

        self.play(MoveToTarget(array))

        ordered = TextMobject("Sorted").move_to(UP)

        self.play(Write(ordered))

        self.wait(3)

        self.play(
            FadeOut(array),
            FadeOut(ordered),
        )

        self.wait(10)
