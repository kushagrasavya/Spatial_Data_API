from fastapi import FastAPI, HTTPException
from models import PointCreate, PolygonCreate, PointUpdate, PolygonUpdate
from database import db, setup_indexes
from bson import ObjectId
from typing import List, Dict, Any
from fastapi.encoders import jsonable_encoder
from bson import ObjectId, errors as bson_errors
import traceback

app = FastAPI()

@app.on_event("startup")
async def init():
    await setup_indexes()

@app.post("/points")
async def create_point(point: PointCreate):
    result = await db.points.insert_one(point.dict())
    return {"id": str(result.inserted_id)}

def fix_mongo_ids(doc: Dict[str, Any]) -> Dict[str, Any]:
    if "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
    return doc

@app.get("/points")
async def get_points() -> List[Dict[str, Any]]:
    raw_points = await db.points.find().to_list(length=100)
    cleaned = [fix_mongo_ids(p) for p in raw_points]
    return jsonable_encoder(cleaned)

@app.get("/point-by-id/{point_id}", tags=["Points"])
async def get_point_by_id(point_id: str):
    point = await db.points.find_one({"_id": ObjectId(point_id)})
    if not point:
        raise HTTPException(status_code=404, detail="Point not found")

    point["id"] = str(point["_id"])
    del point["_id"]

    return {"point": point}


@app.patch("/points/{name}", tags=["Points"])
async def update_point(name: str, update_data: PointUpdate):
    update_fields = {
        k: v for k, v in update_data.dict(exclude_unset=True).items()
    }
    if not update_fields:
        raise HTTPException(status_code=400, detail="No valid fields provided for update")

    result = await db.points.update_one({"name": name}, {"$set": update_fields})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Point with name '{name}' not found")
    return {"message": f"Point '{name}' updated"}


@app.delete("/points/by-name/{name}", tags=["Points"])
async def delete_point_by_name(name: str):
    result = await db.points.delete_one({"name": name})
    if result.deleted_count == 0:
        return {"message": f"No point found with name '{name}'"}
    return {"message": f"Point '{name}' deleted successfully"}

@app.post("/polygons")
async def create_polygon(polygon: PolygonCreate):
    result = await db.polygons.insert_one(polygon.dict())
    return {"id": str(result.inserted_id)}

@app.get("/polygons")
async def get_polygons():
    polygons = await db.polygons.find().to_list(100)
    for poly in polygons:
        poly["id"] = str(poly["_id"])  
        del poly["_id"]  
    return polygons

@app.get("/polygon-by-id/{polygon_id}", tags=["Polygons"])
async def get_polygon_by_id(polygon_id: str):
    polygon = await db.polygons.find_one({"_id": ObjectId(polygon_id)})
    if not polygon:
        raise HTTPException(status_code=404, detail="Polygon not found")

    polygon["id"] = str(polygon["_id"])
    del polygon["_id"]

    return {"polygon": polygon}

    

@app.delete("/polygons/by-name/{name}", tags=["Polygons"])
async def delete_polygon_by_name(name: str):
    result = await db.polygons.delete_one({"name": name})
    if result.deleted_count == 0:
        return {"message": f"No polygon found with name '{name}'"}
    return {"message": f"Polygon '{name}' deleted successfully"}

@app.patch("/polygons/{name}", tags=["Polygons"])
async def update_polygon(name: str, update_data: PolygonUpdate):
    update_fields = {k: v for k, v in update_data.dict(exclude_unset=True).items()}
    if not update_fields:
        raise HTTPException(status_code=400, detail="No valid fields provided for update")

    result = await db.polygons.update_one({"name": name}, {"$set": update_fields})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Polygon with name '{name}' not found")
    return {"message": f"Polygon '{name}' updated"}


