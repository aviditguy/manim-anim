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

        self.width = width
        self.height = height

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

    def set_text(self, *cells, texts=None, fill=" "):
        texts = texts or []
        texts += [fill] * (len(cells) - len(texts))

        for cell, text in zip(cells, texts):
            self[cell].set_text(text)


class Test(Scene):
    def construct(self):
        data = [1, 2, 3, 4, 5]
        vec = MyVector(data=data)
        self.play(Write(vec))
        self.wait(1)

        vec.set_text(1,2,texts=['a', 'b'])
        self.wait(2)

        self.play(vec[1].animate.to_edge(UP))
        self.wait(2)
