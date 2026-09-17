from fastapi import FastAPI , HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel , computed_field , Field
from typing import Annotated , Literal , Optional
import uvicorn
import json


app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json' , "w") as f:
        json.dump(data , f)

class Patient(BaseModel):

    id:Annotated[
        str,
        Field(
            ...,
            description = "ID of the patient",
            example =["P001"]
        )
    ]
    name:Annotated[
        str,
        Field(
            ...,
            description = "name of the patient",
        )
    ]
    city:Annotated[
        str,
        Field(
            ...,
            description = "city where patient lives"
        )
    ]
    age: Annotated[
        int,
        Field(
            ...,
            gt=0 , lt=120,
            description = "Age of patient"
        )
    ]
    gender:Annotated[
        Literal['male' , 'female' , 'others'],
        Field(
            ...,
            description="Gender of patient"
        ),
        
    ]
    height:Annotated[
        float,
        Field(
            ...,
            gt=0,
            description = "Height of the patient in meters"
        )
    ]
    weight:Annotated[
        float,
        Field(
            ...,
            gt=0,
            description = 'weight of the patient'
        )
    ]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(
            self.weight/(self.height**2),
            2
        )

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.4:
            return "under weight"
        elif self.bmi < 25:
            return "normal"
        elif self.bmi < 30:
            return "over weight"
        else:
            return "obese"


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

@app.get('/')
def patient_home():
    return {"message" : "patient APIs"}

@app.post("/create")
def create_patient(patient : Patient):

    # Load existing data
    data = load_data()

    # check if the patient id in data
    if patient.id in data:
        raise HTTPException(
            status_code = 400,
            detail = "Patient already existed"
        )

    # new patient will ne added to JSON file
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save into json
    save_data(data)

    return JSONResponse(
        status_code = 200,
        content = {
            "message" : "patient created successfully"
        }
    )


@app.put('/edit/{patient_id}')

def update_patient(patient_id:str , patient_update:PatientUpdate):

    data = load_data()

    if(patient_id not in data):
        raise HTTPException(status_code=404 , detail = "Patient does not exist")

    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.dump_model(exclude_unset=True)

    for key , value in updated_patient_info.items():
        existing_patient_info[key] = value

    existing_patient_info["id"] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)
    final_updated_patient = patient_pydantic_obj.model_dump(exclude=["id"])

    data[patient_id] = final_updated_patient

    save_data(data)

    return JSONResponse(
        status_code = 200,
        content = "patient details successfully updated"
    )


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code = 404 , detail="patint not found")
    del data[patient_id]

    return JSONResponse(
        status_code = 200,
        content = "Patient details deleted"
    )


if __name__ == "__main__":
    uvicorn.run(app , reload=True)