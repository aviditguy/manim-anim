from manim import *


INSERTION_SORT = """
void insertion_sort(int *arr, int low, int high){
  for (int i=low+1; i<=high; ++i){
    int key = arr[i];
    int j = i - 1;
    while (j >= low && arr[j] > key) {
      arr[j + 1] = arr[j];
      j--;
    }
    arr[j + 1] = key;
  }
}"""


PARTITION_NAIVE = """
int partition_naive(int *arr, int *res, int low, int high){
  int pivot = arr[high];
  int i = low, start = low, j = high - 1, end = high;
  for (; i < high && j >= low; i++, j--){
    if (arr[i] <= pivot) res[start++] = arr[i];
    if (arr[j] > pivot) res[end--] = arr[j];
  }
  res[start] = pivot;
  return start;
}"""


PARTITION_LOMUTO = """
int partition_lomuto(int *arr, int low, int high){
  int pivot = arr[high];
  int i = low-1;
  for (int j = low; j <= high; ++j){
    if (arr[j] < pivot)
      swap(&arr[++i], &arr[j]);
  }
  swap(&arr[++i], &arr[high]);
  return i;
}"""


def show_code(scene, code_string, language="C"):
    code = Code(code_string=code_string, language=language).scale(0.9)
    scene.play(Write(code))
    scene.wait(2)
    scene.play(code.animate.scale(0.6).to_edge(UR))
    return code


class InsertionSort(Scene):
    def construct(self):
        code = show_code(self, INSERTION_SORT)
        self.play(code.animate.shift(DOWN))

        vec = Vector(data=[13, 11, 12, 5, 6]).next_to(code, LEFT).shift(LEFT)
        self.play(Write(vec))
        self.wait(1)

        move_bg = vec.focus_nodes(1, color=BLUE, buff=0)
        for i in range(1, vec.size):
            comp_bg = vec.focus_nodes(i - 1, color=RED, buff=0)

            self.play(
                FadeIn(vec.focus_nodes(i - 1, buff=0)),
                move_bg.animate.move_to(vec[i][0].get_center()),
            )
            self.play(Write(comp_bg))

            key = int(vec[i].value)
            j = i - 1
            while j >= 0 and key < int(vec[j].value):
                j -= 1

            if (j + 1) != i:
                self.play(comp_bg.animate.move_to(vec[j + 1][0].get_center()))
                vec.swap_and_shift_nodes(self, i, j + 1)
            self.play(FadeOut(comp_bg))

        self.play(FadeIn(vec.focus_nodes(vec.size - 1, buff=0)), FadeOut(move_bg))
        self.wait(2)


class PartitionNaive(Scene):
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


class PartitionLomuto(Scene):
    def construct(self):
        code = show_code(self, PARTITION_LOMUTO)
        self.play(code.animate.shift(DOWN))

        vec = Vector(data=[10, 3, 7, 4, 9, 1, 5]).next_to(code, LEFT).shift(LEFT)
        self.play(Write(vec))
        self.wait(1)

        pivot_bg = vec.focus_nodes(vec.size - 1, color=RED, buff=0)
        move_bg = vec.focus_nodes(0, color=BLUE, buff=0)
        insert_bg = vec.focus_nodes(0, buff=0).shift(LEFT * vec.cell_width)

        self.play(Write(pivot_bg), Write(insert_bg), Write(move_bg))

        i = -1
        for j in range(vec.size - 1):
            self.play(move_bg.animate.move_to(vec[j][0].get_center()))
            if int(vec[j].value) < int(vec[-1].value):
                i += 1
                self.play(insert_bg.animate.move_to(vec[i][0].get_center()))
                vec.swap_nodes(self, i, j)

        i += 1
        self.play(FadeOut(move_bg), insert_bg.animate.move_to(vec[i][0].get_center()))
        vec.swap_nodes(self, i, vec.size - 1)
        self.play(
            FadeOut(insert_bg),
            FadeOut(pivot_bg),
            Write(vec.focus_nodes(i, color=RED, buff=0)),
        )

        self.wait(1)

