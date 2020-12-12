from fastapi import FastAPI
import joblib

model = joblib.load("models/model.sav")
app = FastAPI(title="Ham or Spam API", description="API to predict if a SMS is ham or spam")


@app.post("/predict", summary="Make a prediction for a new SMS", tags=["Ham or Spam predictor"])
def predict(data: str) -> str:
    return model.predict([data])[0]
