import json
import os
import mlflow.pyfunc
import pandas as pd
from azureml.ai.monitoring import Collector

model = None
inputs_collector = None
outputs_collector = None


def init():
    global model, inputs_collector, outputs_collector

    model_root = os.environ["AZUREML_MODEL_DIR"]
    model_path = os.path.join(model_root, "model_output")

    model = mlflow.pyfunc.load_model(model_path)

    inputs_collector = Collector(name="model_inputs")
    outputs_collector = Collector(name="model_outputs")


def run(raw_data):
    data = json.loads(raw_data)

    columns = data["input_data"]["columns"]
    rows = data["input_data"]["data"]

    df = pd.DataFrame(rows, columns=columns)

    context = inputs_collector.collect(df)

    predictions = model.predict(df)

    output_df = pd.DataFrame({
        "prediction": predictions
    })

    outputs_collector.collect(output_df, context)

    return {
        "deployment": os.environ.get("DEPLOYMENT_NAME", "unknown"),
        "predictions": predictions.tolist()
    }