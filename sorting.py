from manim import *
from helper import MyVector


class Merge(Scene):
    def construct(self):
        data = [7,10,13,16,8,9,15]
        sdata = sorted(data)

        width=0.6
        vec1 = MyVector(data,width=width)
        vec2 = MyVector(data=[" "]*len(data),width=width, index=False).next_to(vec1, DOWN*1.5)
        larr = vec1.focus(0,4)
        rarr = vec1.focus(4,color=RED)
        
        hl = vec1.focus(0,1,buff=0,color=YELLOW)
        hr = vec1.focus(4,5,buff=0,color=YELLOW)
        hk = vec2.focus(0,1,buff=0,color=YELLOW)

        self.play(Write(vec1))
        self.wait(1)
        self.play(Write(larr), Write(rarr))
        self.wait(1)

        self.play(Write(vec2), Write(hl), Write(hr), Write(hk))
        self.wait(1)

        vec2.set_text(0,1,[sdata[0]])
        self.play(hl.animate.shift(RIGHT*width),hk.animate.shift(RIGHT*width))
        self.wait(0.5)
        
        vec2.set_text(1,2,[sdata[1]])
        self.play(hr.animate.shift(RIGHT*width),hk.animate.shift(RIGHT*width))
        self.wait(0.5)

        vec2.set_text(2,3,[sdata[2]])
        self.play(hr.animate.shift(RIGHT*width),hk.animate.shift(RIGHT*width))
        self.wait(0.5)

        vec2.set_text(3,4,[sdata[3]])
        self.play(hl.animate.shift(RIGHT*width),hk.animate.shift(RIGHT*width))
        self.wait(0.5)

        vec2.set_text(4,5,[sdata[4]])
        self.play(hl.animate.shift(RIGHT*width),hk.animate.shift(RIGHT*width))
        self.wait(0.5)

        vec2.set_text(5,6,[sdata[5]])
        self.play(FadeOut(hr),hk.animate.shift(RIGHT*width))
        self.wait(0.5)

        vec2.set_text(6,7,[sdata[6]])
        self.play(FadeOut(hl), FadeOut(hk))
        self.wait(2)


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
