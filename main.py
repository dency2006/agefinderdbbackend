from fastapi import FastAPI
from database import users_collection
from pydantic import BaseModel

app = FastAPI()

class AgeRequest(BaseModel):
    age: int
    image_name: str

@app.get("/")
async def home():
    return {"message": "FastAPI Running"}

@app.post("/insert")
async def insert_data(data: AgeRequest):

    result = await users_collection.insert_one({
        "predicted_age": data.age,
        "image_name": data.image_name
    })

    return {
        "message": "Data inserted successfully",
        "id": str(result.inserted_id)
    }

@app.get("/count")
async def count_data():

    count = await users_collection.count_documents({})

    return {
        "total_records": count
    }

@app.get("/average-age")
async def average_age():

    result = await users_collection.aggregate([
        {
            "$group": {
                "_id": None,
                "average_age": {"$avg": "$predicted_age"}
            }
        }
    ]).to_list(length=1)

    if not result:
        return {"average_age": 0}

    return {
        "average_age": result[0]["average_age"]
    }