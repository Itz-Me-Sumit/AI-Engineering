from pydantic import BaseModel
from typing import Literal

class Address(BaseModel):
    state : str
    district : str
    pincode : str

class Patient(BaseModel):

    name : str
    gender : Literal["male" , "female" , "others"]
    age : int
    address : Address

address_dict = {
    "state" : "Bihar",
    "district" : "Khagaria",
    "pincode" : "438434" 
}

address1 = Address(**address_dict)

patient_dict = {
    "name" : "sumit",
    "gender": "male",
    "age":22,
    "address" : address1
}

patient1 = Patient(**patient_dict)

temp = patient1.model_dump(exclude={"address":["state"]})

print(type(temp))
print(temp)