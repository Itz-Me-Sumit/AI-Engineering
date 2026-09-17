from pydantic import Field , BaseModel , EmailStr , AnyUrl , field_validator
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


    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        val = value.split('@')[-1]
        valid_domains = ['hdfc.com' , "icici.com"]
        if val not in valid_domains:
            raise ValueError("Not a valid domain")
        return value

    @field_validator("name")
    @classmethod
    def transform_name(cls , value):
        return value.upper()



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
    "age": 30,
    "weight" : 78.4,
    "merried" : True,
    "allergies" : ["lactos" , "dust mites" , "pet dande"],
    "contact_details" : {"contact_number":"9878764898" , "email":"sumit@gmail.com"}
}


patient_obj = Patient(**patient_info)

insert_patient_info(patient_obj)