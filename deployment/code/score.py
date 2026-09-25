import json
import os
import mlflow.pyfunc
import pandas as pd

model = None


def init():
    global model

    model_root = os.environ["AZUREML_MODEL_DIR"]
    model_path = os.path.join(model_root, "model_output")

    print(f"Loading model from: {model_path}")

    model = mlflow.pyfunc.load_model(model_path)

    print("Model loaded successfully")


def run(raw_data):
    data = json.loads(raw_data)
    deployment_name = os.environ.get("DEPLOYMENT_NAME", "unknown")


    columns = data["input_data"]["columns"]
    rows = data["input_data"]["data"]

    df = pd.DataFrame(rows, columns=columns)

    predictions = model.predict(df)

    return {
        "deployment": deployment_name,
        "predictions": predictions.tolist()
    }