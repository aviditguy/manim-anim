from manim import *


class MyNode(VGroup):
    def __init__(
        self,
        text=None,
        label=True,
        label_text=0,
        label_dir=UP,
        width=0.6,
        height=0.6,
        font_size=22,
        **kwargs,
    ):
        super().__init__(**kwargs)

        text = "" if None else text
        node_el = Rectangle(width=width, height=height)
        text_el = Text(str(text), font_size=font_size).move_to(node_el.get_center())

        if label:
            label_el = Text(str(label_text), font_size=font_size * 0.7).next_to(
                node_el, label_dir
            )
            self.add(node_el, text_el, label_el)
        else:
            self.add(node_el, text_el)

    def set_text(self, text=None):
        text = " " if None else text
        new_text = Text(str(text), font_size=self[1].font_size).move_to(
            self[0].get_center()
        )
        self[1].become(new_text)


class MyVector(VGroup):
    def __init__(
        self,
        data=None,
        width=0.6,
        height=0.6,
        index=True,
        index_from=0,
        index_step=1,
        index_dir=UP,
        dir_right=True,
        font_size=22,
        buff=0,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.data = [] if data is None else data
        self.len = len(self.data)

        self.cell_width = width
        self.cell_height = height

        self.index = index
        self.index_from = index_from
        self.index_step = index_step
        self.index_dir = index_dir

        self.dir_right = RIGHT if dir_right else UP
        self.font_size = font_size
        self.index_font_size = font_size * 0.7
        self.buff = buff

        indices = range(index_from, index_from + self.len * index_step, index_step)
        for text, idx in zip(self.data, indices):
            self.add(
                MyNode(
                    text,
                    width=width,
                    height=height,
                    label=index,
                    label_text=idx,
                    label_dir=index_dir,
                )
            )

        self.arrange(self.dir_right, buff=buff)

    def set_text(self, index=0, text=" "):
        self.data[index] = text
        self[index].set_text(text)

    def focus(self, start, end, color=GREEN, buff=0.1):
        group = VGroup(self[x][0] for x in range(start, end))
        rect = (
            SurroundingRectangle(group, buff=buff)
            .set_fill(color, opacity=0.3)
            .set_stroke(color, width=2)
        )
        return rect

    def swap(self, scene, swap_from, swap_to):
        if swap_from == swap_to:
            return

        start_pos = self[swap_from][0].get_center()
        end_pos = self[swap_to][0].get_center()

        arcup = ArcBetweenPoints(start_pos, end_pos, angle=-PI)
        arcdwn = ArcBetweenPoints(end_pos, start_pos, angle=-PI)

        scene.play(
            MoveAlongPath(self[swap_from][1], arcup),
            MoveAlongPath(self[swap_to][1], arcdwn),
        )

        self[swap_from].set_text(self.data[swap_to])
        self[swap_to].set_text(self.data[swap_from])
        self.data[swap_from], self.data[swap_to] = (
            self.data[swap_to],
            self.data[swap_from],
        )

    def shift_left(self, scene, shift_by=1, fill=" "):
        texts = VGroup(*[self[x][1] for x in range(self.len)])
        scene.play(
            FadeOut(texts[:shift_by]),
            texts[shift_by:].animate.shift(LEFT * self.cell_width * shift_by),
        )

        new_values = self.data[shift_by:] + ([fill] * shift_by)
        for i, x in enumerate(new_values):
            self.data[i] = x
            self[i].set_text(x)
            scene.play(FadeIn(self[i][1]), run_time=0.01)
        print(new_values)
        print(self.data)


class Test(Scene):
    def construct(self):
        data = [1, 2, 3, 4, 5]
        vec = MyVector(data=data)
        self.play(Write(vec))
        self.wait(1)

        # self.play(vec[2][1].animate.shift(LEFT*0.6*2))
        vec.shift_left(self, 3, fill=0)
        self.wait(1)

        # vec.swap(self, 1, 4)
        # self.wait(1)

        self.play(vec[4].animate.to_edge(UP))
        self.wait(1)
