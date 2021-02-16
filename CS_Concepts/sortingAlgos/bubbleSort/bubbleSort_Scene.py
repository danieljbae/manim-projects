from manim import *


class showArray(Scene):
    def construct(self):
        self.pointer_color = YELLOW_A
        self.box_color = BLUE
        self.nums = [5, 2, 6, 4, 1, 3]  # simpleConfig

        #######################################
        # Scene Driver
        #######################################
        self.showTitle("Bubble Sort")
        self.showArray(self.nums)
        self.bubbleSort(self.nums, self.values_mobj, self.boxes_mobj)

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
        self.boxes_mobj = boxes_mobj = VGroup(*boxes)
        self.values_mobj = values_mobj = VGroup(*values)
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

    def bubbleSort(self, nums, values_mobj, boxes_mobj):
        '''
        Bubble Sort Animations
        '''
        array = self.array_mobj

        # Move array upwards
        array.generate_target()
        array.target.shift(UP)
        self.play(
            MoveToTarget(array)
        )

        # Pointer to indicate current value
        self.pointer = RegularPolygon(3, start_angle=-PI/2, color=self.pointer_color,
                                      fill_opacity=1).scale(0.2).next_to(self.boxes[0], UP)
        self.play(
            ShowCreation(self.pointer)
        )

        # Bubble Sort Algorithm
        arrayObjs = list(zip(nums, values_mobj, boxes_mobj))
        # arrayObjs = list(zip(nums, values, boxes))
        for i in range(len(arrayObjs)):
            for j in range(len(arrayObjs)-i-1):
                currNum, nextNum = arrayObjs[j][0], arrayObjs[j+1][0]
                currNum, currText, currBox = arrayObjs[j][0], arrayObjs[j][1], arrayObjs[j][2]
                nextNum, nextText, nextBox = arrayObjs[j+1][0], arrayObjs[j+1][1], arrayObjs[j+1][2]

                # Swap values
                if currNum > nextNum:
                    arrayObjs[j], arrayObjs[j+1] = arrayObjs[j+1], arrayObjs[j]
                    result = TextMobject("Swap").move_to(2 * DOWN)
                    self.displayComparison(currNum, nextNum, currBox, nextBox)
                    self.play(
                        AnimationGroup(
                            FadeIn(result),
                            Swap(currText, nextText),
                        )
                    )
                else:
                    self.displayComparison(currNum, nextNum, currBox, nextBox)
                    result = TextMobject("Do not Swap").move_to(2 * DOWN)
                    self.play(
                        FadeIn(result)
                    )
                self.play(
                    FadeOut(result)
                )
                if j == len(arrayObjs)-i:
                    continue
                self.shiftPointer()

            # Todo: play with add_updater to update/maintain color of sorted region
            # self.boxes_mobj[j+1:].set_color(GREY)
            self.resetPointer()

    def displayComparison(self, currNum, nextNum, currBox, nextBox):
        highlight = VGroup(currBox, nextBox)
        brace = Brace(highlight, DOWN)
        brace_text = TexMobject(str(currNum) + "\\text{ }\\textgreater\\text{ }" + str(nextNum)).next_to(brace, DOWN)
        self.play(
            AnimationGroup(
                # GrowFromCenter(brace),
                Write(brace_text)
            )
        )
        self.play(
            # FadeOut(brace),
            FadeOut(brace_text),
        )
        currBox.set_color(self.box_color)
        nextBox.set_color(self.box_color)

    def shiftPointer(self):
        self.pointer.generate_target()
        self.pointer.target.shift(RIGHT)
        self.play(
            MoveToTarget(self.pointer)
        )

    def resetPointer(self):
        self.pointer.generate_target()
        self.pointer.target.next_to(self.boxes[0], UP)
        self.play(
            MoveToTarget(self.pointer)
        )
