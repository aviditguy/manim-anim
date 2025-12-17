from manim import *

def insertion_sort(scene):
    arr = Vector(data=[12, 11, 13, 5, 6])
    scene.play(Write(arr))
    scene.wait(1)

    move_bg = arr.focus_nodes(1, color=BLUE, buff=0)
    comp_bg = arr.focus_nodes(0, color=RED, buff=0)

    scene.play(Write(arr.focus_nodes(0, buff=0)))
    scene.play(Write(move_bg), Write(comp_bg))

    arr.swap_and_shift_nodes(scene, 1, 0)
    scene.play(FadeOut(comp_bg))

    scene.play(
        Write(arr.focus_nodes(1, 3, buff=0)),
        move_bg.animate.shift(RIGHT * 2 * arr.cell_width),
    )

    comp_bg = arr.focus_nodes(2, color=RED, buff=0)
    scene.play(Write(comp_bg))
    scene.play(comp_bg.animate.shift(LEFT * 2 * arr.cell_width))

    arr.swap_and_shift_nodes(scene, 3, 0)
    scene.play(FadeOut(comp_bg))

    scene.play(
        Write(arr.focus_nodes(3, buff=0)),
        move_bg.animate.shift(RIGHT * arr.cell_width),
    )

    comp_bg = arr.focus_nodes(3, color=RED, buff=0)
    scene.play(Write(comp_bg))
    scene.play(comp_bg.animate.shift(LEFT * 2 * arr.cell_width))

    arr.swap_and_shift_nodes(scene, 4, 1)
    scene.play(FadeOut(comp_bg), FadeOut(move_bg), Write(arr.focus_nodes(4, buff=0)))
    scene.wait(2)
