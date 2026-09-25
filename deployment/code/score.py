import json
import os
import mlflow.pyfunc
import pandas as pd

model = None


def init():
    global model

    model_path = os.environ["AZUREML_MODEL_DIR"]
    model = mlflow.pyfunc.load_model(model_path)

    print("Model loaded successfully")


def run(raw_data):
    data = json.loads(raw_data)

    columns = data["input_data"]["columns"]
    rows = data["input_data"]["data"]

    df = pd.DataFrame(rows, columns=columns)

    predictions = model.predict(df)

    return {
        "predictions": predictions.tolist()
    }