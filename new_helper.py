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
        node_value = Text(str(value), font_size=font_size, z_index=1).move_to(
            node_cell.get_center()
        )
        node_label = Text(str(label_value), font_size=self.label_size).next_to(
            node_cell, label_pos
        )

        self.add(node_cell, node_value)
        if label:
            self.add(node_label)

    def set_value(self, new_value=" "):
        node_value = Text(str(new_value), font_size=self.font_size, z_index=1).move_to(
            self[0].get_center()
        )
        self.value = new_value
        self[1].become(node_value)

    def set_label(self, new_label=" "):
        node_label = Text(str(new_label), font_size=self.label_size).next_to(
            self[0], self.label_pos
        )
        self.label_value = new_label
        self[2].become(node_label)

    def set_focus(self, color=GREEN, buff=1):
        return (
            SurroundingRectangle(self[0], color=color, buff=0.1 * buff)
            .set_fill(color, opacity=0.3)
            .set_stroke(color, width=3)
            if self.is_rect
            else Circle()
            .surround(self[0], buffer_factor=0.8 * buff)
            .set_fill(color, opacity=0.3)
            .set_stroke(color, width=3)
        )


def swap_nodes(scene, nodea, nodeb):
    arcup = ArcBetweenPoints(nodea[0].get_center(), nodeb[0].get_center(), angle=-PI)
    arcdwn = ArcBetweenPoints(nodeb[0].get_center(), nodea[0].get_center(), angle=-PI)

    nodea_bg = nodea.set_focus()
    nodeb_bg = nodeb.set_focus()

    scene.play(Write(nodea_bg), Write(nodeb_bg))
    scene.play(MoveAlongPath(nodea[1], arcup), MoveAlongPath(nodeb[1], arcdwn))
    scene.play(FadeOut(nodea_bg), FadeOut(nodeb_bg))

    nodea_val, nodeb_val = nodea.value, nodeb.value
    nodea.set_value(nodeb_val)
    nodeb.set_value(nodea_val)


class Vector(VGroup):
    def __init__(
        self,
        data=None,
        dir_right=True,
        index=True,
        index_from=0,
        index_step=1,
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
        self.index_pos = index_pos
        self.dir_right = dir_right
        self.direction = RIGHT if dir_right else UP
        self.cell_width = width
        self.cell_height = height
        self.font_size = font_size
        self.label_size = font_size * 0.7
        self.buff = buff

        self.add(*self._create_nodes(self.data))
        self._update_indices()

    def _create_nodes(self, data):
        return VGroup(
            *[
                Node(
                    value=str(val),
                    label=self.index,
                    label_value=str(val),
                    label_pos=self.index_pos,
                    width=self.cell_width,
                    height=self.cell_height,
                    font_size=self.font_size,
                )
                for val in data
            ]
        ).arrange(self.direction, buff=self.buff)

    def _update_indices(self):
        if not self.index:
            return

        indices = range(
            self.index_from,
            self.index_from + (self.size * self.index_step),
            self.index_step,
        )
        for idx, index in enumerate(indices):
            self[idx].set_label(index)

    def focus_nodes(self, start, end=None, color=GREEN, buff=0.1):
        end = start + 1 if end is None else end + 1
        nodes = VGroup(*[self[idx][0] for idx in range(start, end)])
        return (
            SurroundingRectangle(nodes, buff=buff)
            .set_fill(color, opacity=0.3)
            .set_stroke(color, width=3)
        )

    def set_nodes(self, scene, index, values=None):
        if index is None or index == []:
            return

        if not isinstance(index, list):
            index = [index]

        if values is None:
            values = [" "] * len(index)

        if not isinstance(values, list):
            values = [values]

        values += [" "] * (len(index) - len(values))
        data = list(sorted(zip(index, values)))

        highlight = self.focus_nodes(data[0][0], data[-1][0] if len(data) > 1 else None)
        scene.play(Write(highlight))

        for idx, val in data:
            self[idx].set_value(val)
            self.data[idx] = val

        scene.play(FadeOut(highlight))

    def add_nodes(self, scene, data, at=None):
        if not isinstance(data, list):
            data = [data]

        at = self.size if at is None else min(at, self.size)
        nodes = self._create_nodes(data)

        if self.size > 0:
            if at == self.size:
                nodes.next_to(self[-1], self.direction, buff=0)
            else:
                scene.play(
                    self[at:].animate.shift(
                        self.direction * self.cell_width * len(data)
                    )
                )
                nodes.next_to(self[at], (LEFT if self.dir_right else DOWN), buff=0)

        for idx, node in enumerate(nodes):
            if self.size == 0:
                self.add(node)
            else:
                self.submobjects.insert(at + idx, node)
            self.data.insert(at + idx, data[idx])
            self.size += 1

        highlight = (
            SurroundingRectangle(VGroup(*[node[0] for node in nodes]), buff=0.1)
            .set_fill(GREEN, opacity=0.3)
            .set_stroke(GREEN, width=3)
        )
        scene.play(Write(highlight), Write(nodes))
        self._update_indices()
        scene.play(FadeOut(highlight))

    def remove_nodes(self, scene, at=None, count=1):
        at = self.size - 1 if at is None else at
        end = at + count

        highlight = self.focus_nodes(at, at + count - 1, color=RED)
        shift_by = (LEFT if self.dir_right else DOWN) * count * self.cell_width
        nodes = VGroup(*self.submobjects[at:end])
        print(nodes)

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

    def swap_nodes(self, scene, swap_from, swap_to):
        if swap_from == swap_to:
            return

        swap_nodes(scene, self[swap_from], self[swap_to])
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


PARTITION_HOARE = """

"""


def show_code(scene, code_string, language="C"):
    code = Code(code_string=code_string, language=language).scale(0.9)
    scene.play(Write(code))
    scene.wait(2)
    scene.play(code.animate.scale(0.6).to_edge(UR))
    return code


class Test(Scene):
    def construct(self):
        code = show_code(self, PARTITION_NAIVE)
        self.play(code.animate.shift(DOWN))

        vec = Vector(data=[10, 3, 7, 4, 9, 1, 5]).next_to(code, LEFT).shift(LEFT)
        res = Vector(data=[" "] * vec.size, index=False).next_to(vec, DOWN)

        self.play(Write(vec), Write(res))
        self.wait(1)

        i, j, start, end = 0, vec.size - 2, 0, vec.size - 1
        pivot = int(vec[-1].value)

        ibg = vec.focus_nodes(i, buff=0)
        jbg = vec.focus_nodes(j, color=BLUE, buff=0)
        pivotbg = vec.focus_nodes(end, color=RED, buff=0)
        startbg = res.focus_nodes(start, buff=0)
        endbg = res.focus_nodes(end, color=BLUE, buff=0)

        self.play(Write(ibg), Write(jbg), Write(pivotbg), Write(startbg), Write(endbg))

        while i < vec.size - 1 and j >= 0:
            self.play(
                ibg.animate.move_to(vec[i][0].get_center()),
                jbg.animate.move_to(vec[j][0].get_center()),
            )

            ival = int(vec[i].value)
            jval = int(vec[j].value)

            indexes = []
            values = []
            if ival <= pivot:
                indexes.append(start)
                values.append(ival)
                start += 1
            if jval > pivot:
                indexes.append(end)
                values.append(jval)
                end -= 1

            res.set_nodes(self, index=indexes, values=values)
            self.play(
                startbg.animate.move_to(res[start][0].get_center()),
                endbg.animate.move_to(res[end][0].get_center()),
            )

            i += 1
            j -= 1

        res.set_nodes(self, start, pivot)
        self.play(FadeOut(ibg), FadeOut(jbg), FadeOut(startbg), FadeOut(endbg))
        self.play(Write(res[start].set_focus(color=RED, buff=0)))
        self.wait(2)
