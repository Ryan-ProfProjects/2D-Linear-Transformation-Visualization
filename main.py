from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import os
from manim import *
from fastapi.responses import FileResponse

app = FastAPI()

import os
from fastapi.responses import FileResponse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/")
async def get_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MEDIA_DIR = os.path.join(os.path.dirname(__file__), "media")
os.makedirs(MEDIA_DIR, exist_ok=True)

class TransformData(BaseModel):
    vector: list[float]
    matrix: list[list[float]]

@app.post("/transform")
async def apply_transformation(data: TransformData):
    vector = data.vector
    matrix = np.array(data.matrix)

    # Safe filename
    file_name = f"{vector[0]}_{vector[1]}_{matrix[0][0]}_{matrix[0][1]}_{matrix[1][0]}_{matrix[1][1]}.mp4"
    file_path = os.path.join(MEDIA_DIR, file_name)

    # Only render if not cached
    if not os.path.exists(file_path):
        class Matrix(LinearTransformationScene):
            def __init__(self):
                LinearTransformationScene.__init__(self, show_coordinates=True, leave_ghost_vectors=True, show_basis_vectors=True)

            def construct(self):
                self.plane.background_lines.set_opacity(0.3)

                A = matrix
                latex_str = r"A = \begin{bmatrix} " \
                    f"{int(A[0,0])} & {int(A[0,1])} \\\\ " \
                    f"{int(A[1,0])} & {int(A[1,1])}" \
                    r" \end{bmatrix}"
                A_lbl = MathTex(latex_str).to_edge(UL).add_background_rectangle()

                # unit_square = self.get_unit_square()
                v = self.get_vector([2, -1], color=YELLOW)

                self.add_transformable_mobject(v)
                self.add_background_mobject(A_lbl)
                self.apply_matrix(A)
                self.wait(2)

        scene = Matrix()
        scene.render()

        latest_video = scene.renderer.file_writer.movie_file_path
        os.rename(latest_video, file_path)

    return FileResponse(file_path, media_type="video/mp4")
