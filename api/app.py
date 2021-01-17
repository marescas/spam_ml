from fastapi import FastAPI
import joblib
from pymongo import MongoClient
import os
from datetime import datetime
from typing import Dict, List

# Get environment variables
HOST = os.getenv("MONGO_HOST")
PORT = int(os.getenv("MONGO_PORT"))
DATABASE = os.getenv("MONGO_INITDB_DATABASE")
USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
# load pretrained machine learning model
model = joblib.load("models/model.sav")
# connect to mongo
client = MongoClient(host=HOST, port=PORT, username=USERNAME, password=PASSWORD)
db = client[DATABASE]
# access to the collection, if not exist, create it when the first item is inserted
collection = db.sms_prediction

app = FastAPI(title="Ham or Spam API", description="API to predict if a SMS is ham or spam")


@app.post("/predict", summary="Make a prediction for a new SMS", tags=["Ham or Spam predictor"])
def predict(data: str) -> str:
    prediction = model.predict([data])[0]
    collection.insert_one({"sms": data, "prediction": prediction, "date": datetime.utcnow()})
    return prediction


@app.post("/predict_multiple", summary="Make a prediction for a new list of SMS", tags=["Ham or Spam predictor"])
def predict_multiple(data: List[str]) -> List[str]:
    prediction = model.predict(data)
    documents = [
        {"sms": sms_aux, "prediction": prediction_aux, "date": datetime.utcnow()} for sms_aux, prediction_aux in
        zip(data, prediction)]
    collection.insert(documents)
    return list(prediction)


@app.post("/get_predictions", summary="Get all the predictions saved on database", tags=["Ham or Spam predictor"])
def get_predictions(num_page: int = 1, page_size: int = 100) -> List[Dict]:
    n_skips = page_size * (num_page - 1)
    result = [item for item in collection.find().skip(n_skips).limit(page_size)]
    return result


@app.post("/stats", summary="Stats for the database", tags=["Ham or Spam predictor"])
def get_stats():
    results = list(collection.aggregate([{"$match": {}}, {"$group": {
        "_id": "$prediction", "total": {"$sum": 1}}}
                                         ]))
    return results
