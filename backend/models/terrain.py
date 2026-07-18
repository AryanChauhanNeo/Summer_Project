"""
models/terrain.py
=================
Pydantic models for terrain data exchanged between the Navigation module
and the backend.
"""

from pydantic import BaseModel


class TerrainData(BaseModel):
    grid: list[list[int]]
    rows: int
    cols: int
    start: list[int]
    goal: list[int]


class TerrainResponse(BaseModel):
    message: str
    data: TerrainData