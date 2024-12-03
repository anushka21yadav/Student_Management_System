from fastapi import FastAPI, APIRouter, HTTPException, Query, Path, Body
from typing import Optional
from configuration import collection
from database.models import Students, GetStudent, PostStudent, UpdateStudent, EmptyResponseModel
from bson import ObjectId

app = FastAPI()
router = APIRouter()

@router.get("/students",
            response_model=GetStudent,
            status_code=200,
            summary="List Students", 
            description="An API to find a list of students. You can apply filters on this API by passing the query parameters as listed below.",
            response_description="sample response")
async def get_specific_students(country: Optional[str] = Query(None,
                                                               description="To apply filter of country. If not given or empty, this filter should be applied."),
                                age: Optional[int] = Query(None,
                                                           description="Only records which have age greater than equal to the provided age should be present in the result. If not given or empty, this filter should be applied.")):
    try:
        query = {}
        if country:
            query["address.country"] = country
        if age is not None:
            query["age"] = {"$gte": age}

        students = list(collection.find(query, {"name": 1, "age": 1, "_id": 0}))

        return GetStudent(data=students)
    
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occoured {e}")

@router.get("/students/{id}",
            response_model=Students,
            status_code=200,
            summary="Fetch student",
            response_description="sample response"
)
async def get_student_by_id(id: str = Path(..., description="The ID of the student previously created.")):
    try:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID format.")

        student = collection.find_one({"_id": ObjectId(id)})
        if not student:
            raise HTTPException(status_code=404, detail="Student not found.")

        return Students(
            name=student["name"],
            age=student["age"],
            address={
                "city": student["address"]["city"],
                "country": student["address"]["country"]
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")
    
@router.post("/students", 
             response_model=PostStudent,
             status_code=201, 
             summary="Create Students", 
             description="API to create a student in the system. All fields are mandatory and required while creating the student in the system.",
             response_description="A JSON response sending back the ID of the newly created student record")
async def post_student(new_student: Students):
    try:
        new_student_dict = new_student.dict()
        new_student_data = collection.insert_one(new_student_dict)
        return PostStudent(id=str(new_student_data.inserted_id))
        
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occoured {e}")
    
@router.patch("/students/{id}",
              status_code=204,
              summary="Update student",
              description="API to update the student's properties based on information provided. Not mandatory that all information would be sent in PATCH, only what fields are sent should be updated in the Database.",
              response_description="No content")
async def update_student(id: str, update_data: UpdateStudent):
    try:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID format.")
        
        update_fields = {}
        if update_data.name:
            update_fields["name"] = update_data.name
        if update_data.age is not None:
            update_fields["age"] = update_data.age
        if update_data.address:
            if update_data.address.city:
                update_fields["address.city"] = update_data.address.city
            if update_data.address.country:
                update_fields["address.country"] = update_data.address.country
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No valid fields provided for update.")
        
        result = collection.update_one({"_id": ObjectId(id)}, {"$set": update_fields})
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Student not found.")
        
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")

@router.delete("/students/{id}",
               response_model=EmptyResponseModel,
               status_code=200,
               summary="Delete student",
               response_description="sample response"
)
async def delete_student(id: str):
    try:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID format.")
        
        result = collection.delete_one({"_id": ObjectId(id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Student not found.")
        
        return {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")


app.include_router(router)

