#To run our code: uvicorn main:app --reload

#Python
from doctest import Example
from typing import Optional
from enum import Enum
#Pydantic
from pydantic import BaseModel
from pydantic import Field
#Fast API
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()


#Models
class Location (BaseModel):
    city: str
    state: str
    country: str

#Validations Model
class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Person (BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example = "Orlando"
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Alemán"
        )
    age: int = Field(
        ...,
        gt=0,
        le=155,
        example = 26
    )
    hair_color: Optional[HairColor] = Field(default=None, example = "black")
    is_married: Optional[bool] = Field(default=None, example = True)

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Facundo",
    #             "last_name": "Hernandez Rivera",
    #             "age": 26,
    #             "hair_color": "brown",
    #             "is_married": "False"
    #         }
    #     }


@app.get("/")
def home():
    return {"Hello": "World"}


#request and response body
@app.post("/person/new")
def create_person(person: Person = Body()):
    #return {"200 Person Created": person.first_name+" "+person.last_name}
    return person

#Validaciones Query Parameters

@app.get("/person/detail") #Path Operations
#path operation function with query parameters
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description= "This is the person name. It's between 1 and 50 characters"
        ),
    age: str = Query(
        title="Person Age",
        description="This is the person age. It's required"
    )):
    return {name:age}


#Validaciones con Path Parameters
@app.get("/person/detail/{person_id}")
def show_person(person_id: int = Path(..., gt=0)):
    return {person_id: "It exists!"}


#Validaciones Request Body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        title= "Person ID",
        description="This is the person id",
        gt=0
    ),
    person: Person = Body(),
    #location: Location = Body()
):
    #results = person.dict()
    #results.update(location)
    #return results
    return person