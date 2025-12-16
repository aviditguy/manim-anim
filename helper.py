from manim import *


NODE_POSITION = [
    [0.0, 2.25, 0.0],
    [-1.4, 1.5, 0.0],
    [1.4, 1.5, 0.0],
    [-2.1, 0.75, 0.0],
    [-0.7, 0.75, 0.0],
    [0.7, 0.75, 0.0],
    [2.1, 0.75, 0.0],
    [-2.45, 0.0, 0.0],
    [-1.75, 0.0, 0.0],
    [-1.05, 0.0, 0.0],
    [-0.35, 0.0, 0.0],
    [0.35, 0.0, 0.0],
    [1.05, 0.0, 0.0],
    [1.75, 0.0, 0.0],
    [2.45, 0.0, 0.0]
]



class Node(VGroup):
    def __init__(self, value=" ", label=True, label_value=" ", label_pos=UP, is_rect=True, width=0.6, height=0.6, radius=0.25, font_size=22, **kwargs):
        super().__init__(**kwargs)

        self.value       = value
        self.label_value = label_value
        self.label_pos   = label_pos
        self.is_rect     = is_rect
        self.font_size   = font_size
        self.label_size  = font_size * 0.7

        node_cell  = (Rectangle(width=width, height=height).set_fill(BLACK, opacity=1)
                      if is_rect else
                      Circle(radius=radius, color=WHITE).set_fill(BLACK, opacity=1))
        node_text  = Text(str(value), font_size=font_size, z_index=1).move_to(node_cell.get_center())
        node_label = Text(str(label_value), font_size=self.label_size).next_to(node_cell, label_pos)

        self.add(node_cell, node_text)
        if label:
            self.add(node_label)

            
    def set_value(self, new_value=" "):
        node_text  = Text(str(new_value), font_size=self.font_size).move_to(self[0].get_center())
        self.value = new_value
        self[1].become(node_text)

        
    def set_label(self, new_label=" "):
        node_label = Text(str(new_label), font_size=self.label_size).next_to(self[0], self.label_pos)        
        self.label_value = new_label
        self[2].become(node_label)

        
    def focus(self, color=GREEN, buff=None):
        buff = (0.2 if self.is_rect else 1) if buff is None else buff
        return (SurroundingRectangle(self[0], buff=buff).set_fill(color=color, opacity=0.3).set_stroke(color, width=3)
                if self.is_rect else
                Circle().surround(self[0], buffer_factor=0.8*buff).set_fill(color, opacity=0.3).set_stroke(color, width=3))


def _swap_nodes(scene, nodea, nodeb):
    arcup = ArcBetweenPoints(nodea[0].get_center(), nodeb[0].get_center(), angle=-PI)
    arcdwn = ArcBetweenPoints(nodeb[0].get_center(), nodea[0].get_center(), angle=-PI)

    scene.play(MoveAlongPath(nodea[1], arcup), MoveAlongPath(nodeb[1], arcdwn))

    nodea_val, nodeb_val = nodea.value, nodeb.value
    nodea.set_value(nodeb_val)
    nodeb.set_value(nodea_val)

    

class Vector(VGroup):
    def __init__(self, data=None, dir_right=True, index=True, index_from=0, index_step=1, index_pos=UP, width=0.6, height=0.6, font_size=22, buff=0, **kwargs):
        super().__init__(**kwargs)

        self.data = [" "] if data is None else data
        self.size = len(self.data)

        self.cell_width = width
        self.cell_height = height
        
        self.index = index
        self.index_from = index_from
        self.index_step = index_step
        self.index_pos  = index_pos

        self.dir_right = dir_right
        self.direction = RIGHT if dir_right else UP

        self.font_size = font_size
        self.index_size = font_size * 0.7

        self.buff = buff

        self.add(*self._create_nodes(self.data))
        self._update_indices()


    def _create_nodes(self, data):
        return VGroup(*[
            Node(value=str(x), label=self.index, label_value=str(i), label_pos=self.index_pos,
                 width=self.cell_width, height=self.cell_height, font_size=self.font_size)
            for i, x in enumerate(data)
        ]).arrange(self.direction, buff=self.buff)


    def _update_indices(self):
        if not self.index:
            return

        indices = range(self.index_from, self.index_from + (self.index_step * self.size), self.index_step)
        for idx, index in enumerate(indices):
            self[idx].set_label(index)


    def swap_nodes(self, scene, swapx, swapy):
        _swap_nodes(scene, self[swapx], self[swapy])
        self.data[swapx], self.data[swapy] = self.data[swapy], self.data[swapx]


    def focus_nodes(self, start=0, end=None, color=GREEN, buff=0.1):
        end = start+1 if end is None else end
        node_cells = VGroup(*[node[0] for node in self[start:end]])
        return SurroundingRectangle(node_cells, buff=buff).set_fill(color, opacity=0.3).set_stroke(color, width=3)

    
    def add_nodes(self, scene, data, at=None):
        if not isinstance(data, list):
            data = [data]

        nodes = self._create_nodes(data)
        at = self.size if at is None else at
        
        if self.size > 0:
            if at == self.size:
                nodes.next_to(self[-1], (RIGHT if self.dir_right else UP), buff=0)

        highlight = SurroundingRectangle(VGroup(*[node[0] for node in nodes]), color=GREEN, buff=0.1).set_fill(GREEN, opacity=0.3)
        scene.play(Write(highlight), Write(nodes))
        scene.play(FadeOut(highlight))
            
        for idx, node in enumerate(nodes):
            if self.size == 0:
                self.add(node)
            else:
                self.submobjects.insert(at+idx, node)
            self.data.insert(at+idx, data[idx])

        self.size = len(self.data)
        self._update_indices()

        
    def remove_nodes(self, scene, start, end=None):
        end = start+1 if end is None else end
        count = end - start
    
        highlight = self.focus_nodes(start, end, color=RED)
        scene.play(Write(highlight))
        scene.wait(0.4)
        
        shift_dir = LEFT if self.dir_right else DOWN
        to_remove = VGroup(*self.submobjects[start:end])

        scene.play(
            FadeOut(highlight),
            FadeOut(to_remove),
            self[end:].animate.shift(shift_dir * count * self.cell_width)
        )

        for node in to_remove:
            self.remove(node)

        # Update data model
        del self.data[start:end]
        self.size = len(self.data)

        self._update_indices()

        
        


class Stack(VGroup):
    def __init__(self, data=None, index=True, index_pos=LEFT, font_size=22, width=0.6, height=0.6, **kwargs):
        super().__init__(**kwargs)

        self.stack = Vector(data=data, dir_right=False, index=index, index_pos=index_pos, width=width, height=height, font_size=font_size)
        self.highlight = self.stack[-1].focus(buff=0).set_z_index(10)
        self.add(self.stack, self.highlight)


    def push_node(self, scene, value=" "):
        self.stack.add_nodes(scene, value, self.stack.size)

        new_highlight = self.stack[-1].focus(buff=0)
        new_highlight.set_z_index(10)

        scene.play(ReplacementTransform(self.highlight, new_highlight))
        self.highlight = new_highlight
        print("size = ", self.stack.size)


    def pop_node(self, scene, count=1):
        start = self.stack.size - count
        self.stack.remove_nodes(scene, start, self.stack.size)

        # If stack is now empty → remove highlight
        if self.stack.size == 0:
            scene.play(FadeOut(self.highlight))
            self.highlight = None
            return

        new_highlight = self.stack[self.stack.size-1].focus(buff=0)
        scene.play(ReplacementTransform(self.highlight, new_highlight))
        self.highlight = new_highlight



def infix_to_postfix_ex1(scene):
    expr = MathTex("a", "+", "b", r"\times", "c", r"\longrightarrow", "a", "b", "c", r"\times", "+")
    stk = Stack(data=["+"]).next_to(expr, RIGHT)
    sr = VGroup(*[SurroundingRectangle(exp) for exp in expr[:5]])
        
    scene.play(Write(expr[:6]))
    scene.wait(1)

    scene.play(Write(sr[0]))
    scene.play(Write(expr[6]))

    scene.play(ReplacementTransform(sr[0], sr[1]))
    scene.play(Write(stk))

    scene.play(ReplacementTransform(sr[1], sr[2]))
    scene.play(Write(expr[7]))

    scene.play(ReplacementTransform(sr[2], sr[3]))
    stk.push_node(scene, "×")
        
    scene.play(ReplacementTransform(sr[3], sr[4]))
    scene.play(Write(expr[8]), FadeOut(sr[4]))

    stk.pop_node(scene)
    scene.play(Write(expr[9]))

    stk.pop_node(scene)
    scene.play(Write(expr[10]))
    scene.wait(1)
    scene.play(expr.animate.to_edge(UL))
    scene.wait(1)


def infix_to_postfix_ex2(scene):
    expr = MathTex("a", r"\times", "b", "+", "c", r"\longrightarrow", "a", "b", r"\times", "c", "+")
    stk = Stack(data=["×"]).next_to(expr, RIGHT)
    sr = VGroup(*[SurroundingRectangle(exp) for exp in expr[:5]])
        
    scene.play(Write(expr[:6]))
    scene.wait(1)

    scene.play(Write(sr[0]))
    scene.play(Write(expr[6]))

    scene.play(ReplacementTransform(sr[0], sr[1]))
    scene.play(Write(stk))

    scene.play(ReplacementTransform(sr[1], sr[2]))    
    scene.play(Write(expr[7]))

    scene.play(ReplacementTransform(sr[2], sr[3]))
    stk.pop_node(scene)
    scene.play(Write(expr[8]))
    stk = Stack(data=["+"]).next_to(expr, RIGHT)
    scene.play(Write(stk))

    scene.play(ReplacementTransform(sr[3], sr[4]))
    scene.play(Write(expr[9]), FadeOut(sr[4]))

    stk.pop_node(scene)
    scene.play(Write(expr[10]))
    scene.play(expr.animate.to_edge(UL).shift(DOWN*0.7))
    scene.wait(1)


def infix_to_postfix_ex3(scene):
    expr = MathTex("(", "a", "+", "b", r"\times", "c", ")", r"/", "d", r"\longrightarrow", "a", "b", "c", r"\times", "+", "d", "/")
    stk = Stack(data=["("]).next_to(expr, RIGHT)
    sr = VGroup(*[SurroundingRectangle(exp) for exp in expr[:9]])
        
    scene.play(Write(expr[:10]))
    scene.wait(1)

    scene.play(Write(sr[0]))
    scene.play(Write(stk))

    scene.play(ReplacementTransform(sr[0], sr[1]))
    scene.play(Write(expr[10]))
    
    scene.play(ReplacementTransform(sr[1], sr[2]))
    stk.push_node(scene, "+")

    scene.play(ReplacementTransform(sr[2], sr[3]))
    scene.play(Write(expr[11]))

    scene.play(ReplacementTransform(sr[3], sr[4]))
    stk.push_node(scene, "×")

    scene.play(ReplacementTransform(sr[4], sr[5]))
    scene.play(Write(expr[12]))

    scene.play(ReplacementTransform(sr[5], sr[6]))
    stk.pop_node(scene, 3)
    scene.play(Write(expr[13:15]))

    scene.play(ReplacementTransform(sr[6], sr[7]))
    stk = Stack(data=["/"]).next_to(expr, RIGHT)
    scene.play(Write(stk))

    scene.play(ReplacementTransform(sr[7], sr[8]))
    scene.play(Write(expr[15]), FadeOut(sr[8]))
    stk.pop_node(scene)
    scene.play(Write(expr[16]))
    scene.wait(1)
    scene.play(expr.animate.to_edge(UL).shift(DOWN*1.4))
    scene.wait(1)


def infix_to_postfix_ex4(scene):
    expr = MathTex("(", "a", r"\times", "b", r"+", "c", ")", r"/", "d", r"\longrightarrow", "a", "b", r"\times", "c", "+", "d", "/")
    stk = Stack(data=["("]).next_to(expr, RIGHT)
    sr = VGroup(*[SurroundingRectangle(exp) for exp in expr[:9]])
        
    scene.play(Write(expr[:10]))
    scene.wait(1)

    scene.play(Write(sr[0]))
    scene.play(Write(stk))

    scene.play(ReplacementTransform(sr[0], sr[1]))
    scene.play(Write(expr[10]))
    
    scene.play(ReplacementTransform(sr[1], sr[2]))
    stk.push_node(scene, "×")

    scene.play(ReplacementTransform(sr[2], sr[3]))
    scene.play(Write(expr[11]))

    scene.play(ReplacementTransform(sr[3], sr[4]))
    stk.pop_node(scene)
    scene.play(Write(expr[12]))
    stk.push_node(scene, "+")

    scene.play(ReplacementTransform(sr[4], sr[5]))
    scene.play(Write(expr[13]))

    scene.play(ReplacementTransform(sr[5], sr[6]))
    stk.pop_node(scene, 2)
    scene.play(Write(expr[14]))

    scene.play(ReplacementTransform(sr[6], sr[7]))
    stk = Stack(data=["/"]).next_to(expr, RIGHT)
    scene.play(Write(stk))

    scene.play(ReplacementTransform(sr[7], sr[8]))
    scene.play(Write(expr[15]), FadeOut(sr[8]))
    stk.pop_node(scene)
    scene.play(Write(expr[16]))
    scene.wait(1)
    scene.play(expr.animate.to_edge(UL).shift(DOWN*2.1))
    scene.wait(1)




class Tree(VGroup):
    def __init__(self, data=None, index=None, **kwargs):
        super().__init__(**kwargs)

        self.max_nodes = len(NODE_POSITION)
        self.treedata = [{"data": i, "alive": False} for i in range(self.max_nodes)]

        nodes = VGroup(*[Node(value=str(x), label=False, is_rect=False).move_to(NODE_POSITION[x]) for x in range(self.max_nodes)])
        edges = VGroup(VGroup(), *[Line(nodes[(i-1)//2][0].get_bottom(), nodes[i][0].get_top()) for i in range(1, self.max_nodes)])

        self.tree = VGroup(VGroup(edge, node).set_opacity(0) for edge, node in zip(edges, nodes))
        
        data = list(range(self.max_nodes)) if data is None else data
        index = list(range(len(data))) if index is None else index
        for idx, value in zip(index, data):
            self.treedata[idx] = {"data": value, "alive": True}
            self.tree[idx].set_opacity(1)

        self.add(self.tree)

        
    def focus(self, index, color=GREEN, buff=None):
        if index >= self.max_nodes:
            return VGroup()
        return self.get_node(index).focus(color=color, buff=buff)
    

    def get_node(self, index):
        return self.tree[index][-1] if index < self.max_nodes else None

    
    def get_info(self, index):
        return {
            "node": self.get_node(index),
            "parent": self.get_node((index-1)//2) if index > 0 else None,
            "left": self.get_node(2*index+1),
            "right": self.get_node(2*index+2)
        }

    def get_edge_path(self, parent, child):
        if child >= self.max_nodes:
            return None

        parent_node = self.get_node(parent)
        child_node = self.get_node(child)

        if not parent_node or not child_node:
            return None

        return Line(
            parent_node[0].get_center(),
            child_node[0].get_center()
        )




# def inorder_traversal(scene, tree, start, highlight):
#     if start >= tree.max_nodes or not tree.treedata[start]["alive"]:
#         return

#     left = 2*start+1
#     if left < tree.max_nodes and tree.treedata[left]["alive"]:
#         scene.play(highlight.animate.move_to(tree.get_node(left).get_center()))
#     inorder_traversal(scene, tree, left, highlight)

#     visiting = tree.focus(start, color=YELLOW)
#     scene.play(Write(visiting))

#     right = 2*start+2
#     if right < tree.max_nodes and tree.treedata[right]["alive"]:
#         scene.play(highlight.animate.move_to(tree.get_node(right).get_center()))
#     inorder_traversal(scene, tree, right, highlight)



def reversed_path(path):
    return Line(path.get_end(), path.get_start())


def inorder_traversal(scene, tree, index, highlight):
    if index >= tree.max_nodes or not tree.treedata[index]["alive"]:
        return

    left = 2*index + 1
    right = 2*index + 2

    # ⬇️ LEFT
    if left < tree.max_nodes and tree.treedata[left]["alive"]:
        down = tree.get_edge_path(index, left)
        up   = tree.get_edge_path(left, index)

        scene.play(MoveAlongPath(highlight, down), run_time=0.5)
        inorder_traversal(scene, tree, left, highlight)
        scene.play(MoveAlongPath(highlight, up), run_time=0.4)

    # 🟡 VISIT
    visit = tree.focus(index, color=YELLOW)
    scene.play(Write(visit))
    scene.wait(0.4)
    scene.play(FadeOut(visit))

    # ⬇️ RIGHT
    if right < tree.max_nodes and tree.treedata[right]["alive"]:
        down = tree.get_edge_path(index, right)
        up   = tree.get_edge_path(right, index)

        scene.play(MoveAlongPath(highlight, down), run_time=0.5)
        inorder_traversal(scene, tree, right, highlight)
        scene.play(MoveAlongPath(highlight, up), run_time=0.4)

    

        
        
class Test(Scene):
    def construct(self):
        # infix_to_postfix_ex1(self)
        # infix_to_postfix_ex2(self)
        # infix_to_postfix_ex3(self)
        # infix_to_postfix_ex4(self)

        tree = Tree(data=[1,2,3,4,5,6], index=[0, 1, 2, 3, 4, 6])
        vec = Vector(data=[3], index=False).next_to(tree, DOWN).shift(LEFT)

        self.play(Write(tree))
        self.wait(1)
        
        highlight = tree.focus(0)


        inorder_traversal(self, tree, 0, highlight)
        
        # self.play(Write(highlight))
        # self.play(highlight.animate.move_to(tree.get_node(1).get_center()))

        # self.play(highlight.animate.move_to(tree.get_node(3).get_center()))
        # self.play(tree.focus(3).animate.set_stroke(YELLOW, width=4))
        # self.play(Write(vec))

        # self.play(highlight.animate.move_to(tree.get_node(1).get_center()))
        # self.play(tree.focus(1).animate.set_stroke(YELLOW, width=4))
        # vec.add_nodes(self, 1)

        # self.play(highlight.animate.move_to(tree.get_node(4).get_center()))
        # self.play(tree.focus(4).animate.set_stroke(YELLOW, width=4))
        # vec.add_nodes(self, 4)
        
        # self.play(highlight.animate.move_to(tree.get_node(1).get_center()))
        # self.play(highlight.animate.move_to(tree.get_node(0).get_center()))
        # self.play(tree.focus(0).animate.set_stroke(YELLOW, width=4))
        # vec.add_nodes(self, 0)
        
        # self.play(highlight.animate.move_to(tree.get_node(2).get_center()))
        # self.play(tree.focus(2).animate.set_stroke(YELLOW, width=4))
        # vec.add_nodes(self, 2)
        
        # self.play(highlight.animate.move_to(tree.get_node(6).get_center()))
        # self.play(tree.focus(6).animate.set_stroke(YELLOW, width=4))
        # vec.add_nodes(self, 6)
        
        self.wait(1)
        
