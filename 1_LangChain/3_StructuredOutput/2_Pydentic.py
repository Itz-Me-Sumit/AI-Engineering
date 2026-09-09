from pydantic import BaseModel , EmailStr , Field
from typing import Optional

class Student(BaseModel):
    name : str = "Sumit"
    age : Optional[int] = None
    email : EmailStr
    cgpa : float = Field(
        gt=0 , lt = 10 , default = 5 ,
        description = "A decimal value representing cgpa of student."
    )
    # gt(Greater then) , lt(less then) ,
    # ge(greater then or equal to ) , le(less then or equal to)

new_std = {
    "name" : "sumit",
    "age" : 22,
    "email" : "sumit@gmail.com",
    "cgpa" : 6
}

new_std1 = {
    "name" : "sumit"
}
new_std2 = {
    "age" : 22
}

std = Student(**new_std)

std_dict = std.model_dump() # to convert it into dict

print(std_dict['name'])

std_json = std.model_dump_json() # to convert it into json