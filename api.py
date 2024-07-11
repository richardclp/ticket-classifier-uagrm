from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Ticket(BaseModel):
    issue: str

@app.post("/predict_priority")
def predict_priority(ticket: Ticket):
    # Aquí se realizaría la predicción con tu modelo de machine learning
    # Por ahora, simplemente devolvemos "Medio"
    return {"priority": "Medio"}