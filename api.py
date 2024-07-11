from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Ticket(BaseModel):
    issue: str

@app.post("/predict_priority")
def predict_priority(ticket: Ticket):
    # Aqui se realizara la prediccion con tu modelo de machine learning
    # Por ahora, simplemente devolvemos "Medio"
    return {"priority": "Medio"}