import argparse
from pathlib import Path
import os
import pickle

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


TARGET_COL = "cost"

NUMERIC_COLS = [
    "distance",
    "dropoff_latitude",
    "dropoff_longitude",
    "passengers",
    "pickup_latitude",
    "pickup_longitude",
    "pickup_weekday",
    "pickup_month",
    "pickup_monthday",
    "pickup_hour",
    "pickup_minute",
    "pickup_second",
    "dropoff_weekday",
    "dropoff_month",
    "dropoff_monthday",
    "dropoff_hour",
    "dropoff_minute",
    "dropoff_second",
]

CAT_NOM_COLS = [
    "store_forward",
    "vendor",
]

CAT_ORD_COLS = [
]

SENSITIVE_COLS = ["vendor"] # for fairlearn dashborad


def parse_args():
        
    parser = argparse.ArgumentParser("predict")
    parser.add_argument("--model_input", type=str, help="Path of input model")
    parser.add_argument("--prepared_data", type=str, help="Path to transformed data")
    parser.add_argument("--predictions", type=str, help="Path of predictions")
    parser.add_argument("--score_report", type=str, help="Path to score report")

    args = parser.parse_args()

    return args


def main():

    args = parse_args()

    lines = [
        f"Model path: {args.model_input}",
        f"Test data path: {args.prepared_data}",
        f"Predictions path: {args.predictions}",
        f"Scoring output path: {args.score_report}",
    ]

    for line in lines:
        print(line)

    # ---------------- Model Evaluation ---------------- #

    # Load the test data

    print("mounted_path files: ")
    arr = os.listdir(args.prepared_data)

    train_data = pd.read_csv((Path(args.prepared_data) / "train.csv"))
    test_data = pd.read_csv((Path(args.prepared_data) / "test.csv"))

    y_train = train_data[TARGET_COL]
    X_train = train_data[NUMERIC_COLS + CAT_NOM_COLS + CAT_ORD_COLS]

    y_test = test_data[TARGET_COL]
    X_test = test_data[NUMERIC_COLS + CAT_NOM_COLS + CAT_ORD_COLS]

    # Load the model from input port
    model = pickle.load(open((Path(args.model_input) / "model.pkl"), "rb"))

    # Get predictions to y_test (y_test)
    yhat_test = model.predict(X_test)

    # Save the output data with feature columns, predicted cost, and actual cost in csv file
    output_data = X_test.copy()
    output_data["real_label"] = y_test
    output_data["predicted_label"] = yhat_test
    output_data.to_csv((Path(args.predictions) / "predictions.csv"))

    # Evaluate Model performance with the test set
    r2 = r2_score(y_test, yhat_test)
    mse = mean_squared_error(y_test, yhat_test)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, yhat_test)

    # Print score report to a text file
    (Path(args.score_report) / "score.txt").write_text(
        "Scored with the following model:\n{}".format(model)
    )
    with open((Path(args.score_report) / "score.txt"), "a") as f:
        f.write("Mean squared error: %.2f \n" % mse)
        f.write("Root mean squared error: %.2f \n" % rmse)
        f.write("Mean absolute error: %.2f \n" % mae)
        f.write("Coefficient of determination: %.2f \n" % r2)

    # Visualize results
    plt.scatter(y_test, yhat_test,  color='black')
    plt.plot(y_test, y_test, color='blue', linewidth=3)
    plt.xlabel("Real value")
    plt.ylabel("Predicted value")
    plt.title("Comparing Model Predictions to Real values - Test Data")
    plt.savefig(Path(args.score_report) / "predictions.png")

    # -------------------- Promotion ------------------- #
    scores = {}
    predictions = {}
    score = r2_score(y_test, yhat_test) # current model
    print(scores)
                
    scores["current model"] = score
    perf_comparison_plot = pd.DataFrame(scores, index=["r2 score"]).plot(kind='bar', figsize=(15, 10))
    perf_comparison_plot.figure.savefig(Path(args.score_report) / "perf_comparison.png")



if __name__ == "__main__":
    main()