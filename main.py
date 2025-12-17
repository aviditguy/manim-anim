from manim import *


class Node(VGroup):
    def __init__(
        self,
        value=" ",
        label=True,
        label_value=" ",
        label_pos=UP,
        is_rect=True,
        width=0.6,
        height=0.6,
        radius=0.25,
        font_size=22,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.value = value
        self.label = label
        self.label_value = label_value
        self.label_pos = label_pos
        self.is_rect = is_rect
        self.font_size = font_size
        self.label_size = font_size * 0.7

        node_cell = (
            Rectangle(width=width, height=height).set_fill(BLACK, opacity=1)
            if is_rect
            else Circle(radius=radius, color=WHITE).set_fill(BLACK, opacity=1)
        )
        node_text = Text(str(value), font_size=font_size, z_index=1).move_to(
            node_cell.get_center()
        )
        node_label = Text(str(label_value), font_size=self.label_size).next_to(
            node_cell, label_pos
        )

        self.add(node_cell, node_text)
        if label:
            self.add(node_label)

    def set_value(self, value=" "):
        node_text = Text(str(value), font_size=self.font_size, z_index=1).move_to(
            self[0].get_center()
        )
        self.value = value
        self[1].become(node_text)

    def set_label(self, label=" "):
        node_label = Text(str(label), font_size=self.label_size).next_to(
            self[0], self.label_pos
        )
        self.label_value = label
        self[2].become(node_label)

    def focus(self, color=GREEN, buff=1):
        buffer_factor = 0 if self.is_rect else 0.8
        return (
            SurroundingRectangle(self[0], buff=buff * buffer_factor).set_fill(
                color=color, opacity=0.2
            )
            if self.is_rect
            else Circle()
            .surround(self[0], buffer_factor=buffer_factor * buff)
            .set_fill(color)
        )


def _swap_nodes(scene, nodea, nodeb):
    arcup = ArcBetweenPoints(nodea[0].get_center(), nodeb[0].get_center(), angle=-PI)
    arcdwn = ArcBetweenPoints(nodeb[0].get_center(), nodea[0].get_center(), angle=-PI)

    nodea_hl = nodea.focus()
    nodeb_hl = nodeb.focus()
    nodea_val, nodeb_val = nodea.value, nodeb.value

    scene.play(Write(nodea_hl), Write(nodeb_hl))
    scene.play(MoveAlongPath(nodea[1], arcup), MoveAlongPath(nodeb[1], arcdwn))
    nodea.set_value(nodeb_val)
    nodeb.set_value(nodea_val)
    scene.play(FadeOut(nodea_hl), FadeOut(nodeb_hl))


class Vector(VGroup):
    def __init__(
        self,
        data=None,
        index=True,
        index_from=0,
        index_step=1,
        dir_right=True,
        index_pos=UP,
        width=0.6,
        height=0.6,
        font_size=22,
        buff=0,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.data = [] if data is None else data
        self.size = len(self.data)
        self.index = index
        self.index_from = index_from
        self.index_step = index_step
        self.dir_right = dir_right
        self.direction = RIGHT if dir_right else UP
        self.index_pos = index_pos
        self.cell_width = width
        self.cell_height = height
        self.font_size = font_size
        self.label_size = font_size * 0.7
        self.buff = buff

        self.add(*self._create_nodes(self.data))
        self._update_indices()

    def _create_nodes(self, data=[]):
        return VGroup(
            *[
                Node(
                    value=str(x),
                    label=self.index,
                    label_value=str(i),
                    label_pos=self.index_pos,
                    width=self.cell_width,
                    height=self.cell_height,
                    font_size=self.font_size,
                )
                for i, x in enumerate(data)
            ]
        ).arrange(self.direction, buff=self.buff)

    def _update_indices(self):
        if not self.index:
            return
        indices = range(
            self.index_from,
            self.index_from + (self.index_step * len(self.data)),
            self.index_step,
        )
        for idx, index in enumerate(indices):
            self[idx].set_label(str(index))
            
    def focus_nodes(self, start, end=None, color=GREEN, buff=0.1):
        end = start + 1 if end is None else end
        node_cells = VGroup(*[node[0] for node in self[start:end]])
        return (
            SurroundingRectangle(node_cells, buff=buff)
            .set_fill(color, opacity=0.3)
            .set_stroke(color, width=3)
        )

    def swap_nodes(self, scene, swap_from, swap_to):
        if swap_from == swap_to:
            return

        _swap_nodes(scene, self[swap_from], self[swap_to])
        self.data[swap_from], self.data[swap_to] = (
            self.data[swap_to],
            self.data[swap_from],
        )

    def swap_and_shift_nodes(self, scene, swap_from, swap_to):
        if swap_from == swap_to:
            return

        arc = ArcBetweenPoints(
            self[swap_from][0].get_center(), self[swap_to][0].get_center(), angle=-PI
        )

        step = 1 if swap_from < swap_to else -1
        cells = range(swap_from, swap_to + step, step)
        nodes = VGroup(*[self[i][0] for i in cells])
        labels = VGroup(*[self[i][1] for i in cells])

        shift_by = (LEFT if swap_from < swap_to else RIGHT) * self.cell_width
        if not self.dir_right:
            shift_by = (DOWN if swap_from < swap_to else UP) * self.cell_height

        highlight = SurroundingRectangle(nodes, color=GREEN, buff=0.1)
        scene.play(Write(highlight))
        scene.play(
            MoveAlongPath(labels[0], arc),
            labels[1:].animate.shift(shift_by),
        )
        scene.play(FadeOut(highlight))

        tmp = self.data[swap_from]
        for i in cells:
            self.data[i] = self.data[i + step]
        self.data[swap_to] = tmp

        for idx, val in enumerate(self.data):
            self[idx].set_value(str(val))

    def add_nodes(self, scene, data, at=None):
        if not isinstance(data, list):
            data = [data]

        at = self.size if at is None else min(at, self.size)
        nodes = self._create_nodes(data).arrange(
            RIGHT if self.dir_right else UP, buff=self.buff
        )

        if self.size > 0:
            nodes.next_to(self[-1], self.direction, buff=0)
            if at is not self.size:
                shift_by = self.direction * (
                    (self.cell_width if self.dir_right else self.cell_height)
                    * len(data)
                )
                scene.play(self[at:].animate.shift(shift_by))
                nodes.next_to(self[at], LEFT if self.dir_right else DOWN, buff=0)

        for idx, node in enumerate(nodes):
            if self.size == 0:
                self.add(node)
            else:
                self.submobjects.insert(at + idx, node)
            self.data.insert(at + idx, data[idx])
        self.size = len(self.data)

        highlight = SurroundingRectangle(
            VGroup(*[node[0] for node in nodes]), color=GREEN, buff=0.1
        )
        scene.play(Write(highlight), Write(nodes))
        scene.play(FadeOut(highlight))
        self._update_indices()

    def pop_nodes(self, scene, at=None, count=1):
        at = self.size - 1 if at is None else min(at, self.size - 1)
        end = at + count

        highlight = self.focus_nodes(at, at + count, color=RED)
        shift_by = (LEFT if self.dir_right else DOWN) * count * self.cell_width
        nodes = VGroup(*self.submobjects[at:end])

        scene.play(Write(highlight))
        scene.play(
            FadeOut(highlight),
            FadeOut(nodes),
            self[end:].animate.shift(shift_by),
        )

        del self.data[at:end]
        self.size = len(self.data)
        for node in nodes:
            self.remove(node)
        self._update_indices()






class Test(Scene):
    def construct(self):
        insertion_sort(self)
        
