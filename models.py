from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class PointGeoJSON(BaseModel):
    type: Literal["Point"] = "Point"
    coordinates: List[float]  

class PointCreate(BaseModel):
    name: str
    description: str
    location: PointGeoJSON

class PointUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[PointGeoJSON] = None

class PolygonGeoJSON(BaseModel):
    type: Literal["Polygon"] = "Polygon"
    coordinates: List[List[List[float]]]

class PolygonCreate(BaseModel):
    name: str
    colour: str
    area: PolygonGeoJSON

class PolygonUpdate(BaseModel):
    name:   Optional[str] = None
    colour: Optional[str] = None
    area:   Optional[PolygonGeoJSON] = None

