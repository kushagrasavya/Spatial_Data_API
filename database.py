from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.spatial_data

# Ensure indexes
async def setup_indexes():
    await db.points.create_index([("location", "2dsphere")])
    await db.polygons.create_index([("area", "2dsphere")])
