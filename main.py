from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Literal
import pandas as pd

from src.gwo_basic_tsp import run_gwo_basic
from src.gwo_advanced2_tsp import run_gwo_advanced2
from src.ga_tsp import run_ga
from src.aco_tsp import run_aco
from src.pso_tsp import run_pso

app = FastAPI()

# Enable CORS for all domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supported algorithms
AlgorithmType = Literal["GWO Basic", "GWO Advanced 2.0", "GA", "ACO", "PSO"]

@app.post("/solve_tsp/")
async def solve_tsp(
    file: UploadFile = File(...),
    algorithm: AlgorithmType = Form(...)
):
    # Load uploaded CSV
    df = pd.read_csv(file.file)
    if not {'X', 'Y'}.issubset(df.columns):
        return {"error": "CSV must have 'X' and 'Y' columns"}

    coords = list(zip(df['X'], df['Y']))

    # Run the selected algorithm
    if algorithm == "GWO Basic":
        route, dist, convergence = run_gwo_basic(coords)
    elif algorithm == "GWO Advanced 2.0":
        route, dist, convergence = run_gwo_advanced2(coords)
    elif algorithm == "GA":
        route, dist, convergence = run_ga(coords)
    elif algorithm == "ACO":
        route, dist, convergence = run_aco(coords)
    elif algorithm == "PSO":
        route, dist, convergence = run_pso(coords)
    else:
        return {"error": "Invalid algorithm selected."}

    return {
        "final_distance": dist,
        "route": route,
        "coordinates": coords,
        "convergence": convergence
    }
