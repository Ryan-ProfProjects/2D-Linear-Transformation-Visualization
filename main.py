from manim import *
import numpy as np

class Matrix(LinearTransformationScene):
    def __init__(self):
        LinearTransformationScene.__init__(self, show_coordinates=True, leave_ghost_vectors=True, show_basis_vectors=True)

    def construct(self):
        self.plane.background_lines.set_opacity(0.3)

        A = np.array([[-1, 1], [1, 1]])
        A_lbl = MathTex(r"A = \begin{bmatrix} -1 & 1 \\ 1 & 1 \end{bmatrix}").to_edge(UL).add_background_rectangle()

        # unit_square = self.get_unit_square()
        v = self.get_vector([2, -1], color=YELLOW)

        self.add_transformable_mobject(v)
        self.add_background_mobject(A_lbl)
        self.apply_matrix(A)
        self.wait(2)


if __name__ == "__main__":
    scene = Matrix()
    scene.render()
