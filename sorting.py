from manim import *
from helper import MyVector


class InsertionSort(Scene):
    def construct(self):
        data = [10, 7, 11, 13, 9, 4]

        vec = MyVector(data)
        self.play(Write(vec))
        self.wait(1)

        key_bg = vec.focus(1,2,buff=0)
        cmp_bg = vec.focus(0,1,color=RED,buff=0)

        self.play(Write(key_bg), Write(cmp_bg))
        vec.swap_and_shift(self, 1,0)
        
        self.play(FadeOut(cmp_bg), key_bg.animate.shift(RIGHT*vec.cell_width))
        self.play(key_bg.animate.shift(RIGHT*vec.cell_width))
        self.play(key_bg.animate.shift(RIGHT*vec.cell_width))

        cmp_bg.shift(RIGHT*vec.cell_width*3)
        self.play(FadeIn(cmp_bg))
        self.play(cmp_bg.animate.shift(LEFT*vec.cell_width))
        self.play(cmp_bg.animate.shift(LEFT*vec.cell_width))
        vec.swap_and_shift(self, 4,1)

        self.play(FadeOut(cmp_bg), key_bg.animate.shift(RIGHT*vec.cell_width))
        cmp_bg.shift(RIGHT*vec.cell_width*3)
        self.play(FadeIn(cmp_bg))
        for i in range(4):
            self.play(cmp_bg.animate.shift(LEFT*vec.cell_width))
        vec.swap_and_shift(self, 5, 0)
        
        self.play(FadeOut(cmp_bg), FadeOut(key_bg))
        
        self.wait(2)
