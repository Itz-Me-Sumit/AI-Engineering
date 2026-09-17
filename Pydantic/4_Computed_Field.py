from pydantic import Field , BaseModel , EmailStr , AnyUrl , computed_field
from typing import List , Dict , Optional , Annotated

class Patient(BaseModel):

    name:str
    email : EmailStr
    linkdin_url : AnyUrl
    age: int 
    weight: float
    height : float
    merried:bool
    allergies: List[str]
    contact_details : Dict[str,str] # Dict[key , value]


    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(
            (self.weight/self.height ** 2),
            2
        )
        return bmi


def insert_patient_info(patient):
    print(patient.name)
    print(patient.email)
    print(patient.linkdin_url)
    print(patient.age)
    print(patient.weight)
    print(patient.height)
    print("BMI" , patient.bmi)
    print(patient.merried)
    print(patient.allergies)
    print(patient.contact_details)
    print("inserted into database")


patient_info = {
    "name" : "nitish",
    "email" :"hehehe@hdfc.com",
    "linkdin_url" : "http://linkdin.com/123",
    "age": 30,
    "weight" : 78.4,
    "height" : 1.7,
    "merried" : True,
    "allergies" : ["lactos" , "dust mites" , "pet dande"],
    "contact_details" : {"contact_number":"9878764898" , "email":"sumit@gmail.com"}
}


patient_obj = Patient(**patient_info)

insert_patient_info(patient_obj)