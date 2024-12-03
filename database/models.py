from pydantic import BaseModel, Field
from typing import List, Optional

class Address(BaseModel):
    city: str
    country: str

class Students(BaseModel):
    name: str
    age: int
    address: Address

class GetStudentData(BaseModel):
    name: str
    age: int

class GetStudent(BaseModel):
    data: Optional[List[GetStudentData]] = Field(default=None, example=[{"name": "string", "age": 0}])

class PostStudent(BaseModel):
    id: Optional[str] = None

class UpdateAddress(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[UpdateAddress] = None

class EmptyResponseModel(BaseModel):
    __annotations__ = {}
    
    class Config:
        schema_extra = {
            "example": {}
        }
