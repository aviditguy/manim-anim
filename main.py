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


class Test(Scene):
    def construct(self):
        data = [1, 2, 3, 4, 5]
        nodes = VGroup(*[MyNode(x, label=False) for i, x in enumerate(data)]).arrange(
            RIGHT, buff=0
        )
        self.play(Write(nodes))

        self.wait(2)
