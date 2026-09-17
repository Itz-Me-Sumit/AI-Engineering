from pydantic import Field , BaseModel , EmailStr , AnyUrl , model_validator
from typing import List , Dict , Optional , Annotated

class Patient(BaseModel):

    name:str
    email : EmailStr
    linkdin_url : AnyUrl
    age: int 
    weight: float
    merried:bool
    allergies: List[str]
    contact_details : Dict[str,str] # Dict[key , value]


    @model_validator(mode="after")
    def valid_emergency_contacts(cls , model):
        if model.age >= 60 and 'emergency' not in model.contact_details:
            raise ValueError(
                "Patient is older then 60 , So you must have to insert emergency contact detials"
            )
        return model

    



def insert_patient_info(patient):
    print(patient.name)
    print(patient.email)
    print(patient.linkdin_url)
    print(patient.age)
    print(patient.weight)
    print(patient.merried)
    print(patient.allergies)
    print(patient.contact_details)
    print("inserted into database")


patient_info = {
    "name" : "nitish",
    "email" :"hehehe@hdfc.com",
    "linkdin_url" : "http://linkdin.com/123",
    "age": 61,
    "weight" : 78.4,
    "merried" : True,
    "allergies" : ["lactos" , "dust mites" , "pet dande"],
    "contact_details" : {
        "contact_number":"9878764898", 
        "email":"sumit@gmail.com",
        "emergency" : "9838438734"
    }
}


patient_obj = Patient(**patient_info)

insert_patient_info(patient_obj)