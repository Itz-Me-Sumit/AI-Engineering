from pydantic import Field , BaseModel , EmailStr , AnyUrl
from typing import List , Dict , Optional , Annotated

class Patient(BaseModel):

    name: Annotated[
        str,
        Field(
            max_lenght=50, 
            title = "Name of patient",
            description="Give the name of patient in less then 50 character",
            examples=["Nitish","Amit"]
        )
    ]
    email : EmailStr
    linkdin_url : AnyUrl
    age: int = Field(ge=18)
    weight: Annotated[
        str,
        Field(
            gt=0,
            strict=True # pydantic can allow '34' even if it is string, by strict = True it must be in int form
        )
    ]
    merried: Annotated[
        bool,
        Field(
            default=bool,
            title="patient marrige status",
            description="is patient married in True or False, by default it's False"
        )
    ]
    allergies: Annotated[
        Optional[List[str]],
        Field(
            default = None,
            max_length = 5,
            title = "Allergies of patient",
            description = "Give Atmost 5 allergies of a patient , by default it's None"
        )
    ]
    contact_details : Dict[str,str] # Dict[key , value]

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
    "email" :"hehehe@gmail.com",
    "linkdin_url" : "http://linkdin.com/123",
    "age": 30,
    "weight" : 78.4,
    "merried" : True,
    "allergies" : ["lactos" , "dust mites" , "pet dande"],
    "contact_details" : {"contact_number":"9878764898" , "email":"sumit@gmail.com"}
}


patient_obj = Patient(**patient_info)

insert_patient_info(patient_obj)