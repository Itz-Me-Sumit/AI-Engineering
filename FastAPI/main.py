from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message" : "Hello World"}

@app.get("/about")
def about():
    return {"message" : "hello i'm Sumit\n learning FastAPI"}

@app.get('/patient/{patient_id}')
def view_patient(patient_id : str):
    