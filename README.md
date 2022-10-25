# ML minimal project template

The repository presents a minimal structure for ML projects.

The code is structured in multiple steps. Each step, in the form of a python script, can be executed independently of the rest of the pipeline.

The term "pipeline" is used to indicate a sequences of steps.

A code structured this way can be easily integrated with Azure Machine Learning features.

&nbsp;
- #### data
    The folder containing the data and the artefacts in the different processing stages (raw data, prepared data, models, reports, predictions).

- #### src
    The script for the different stages (data preparation, model training, model evaluation, prediction, etc.)

- #### notebooks
    The exploration notebooks.

&nbsp;
-----
## data

The folder containing the data and the artefacts in the different processing stages (raw data, prepared data, models, reports, predictions).

Raw data is versionned with Git for illustration purposes only. In a real setting data should not be versionning with git and it should be only kept locally or in a cloud storage.

-  #### 0_raw
    The raw data ingested from sources before any processing.

- #### 1_prepared
    The data after being prepared for training. Can typically contain training, validation and testing data sets.

- #### 2_model
    The trained model(s).

- #### 3_reporting:
    The training or evaluation reports

- #### 4_prediction:
    The predictions for testing, evaluation or training data.

&nbsp;
-----
## src

The folder presents a proposition of structure for data.

- #### prep.py
    The script for preparing and splitting raw data.

    `python src/prep.py --raw_data "data/0_raw" --prepared_data "data/1_prepared"`

- #### train.py
    The script for training and saving the model.

    `python src/train.py --prepared_data "data/1_prepared" --model_output "data/2_model" --score_report "data/3_reports"`

- #### evaluate.py
    The script for model evaluation.

    `python src/evaluate.py --prepared_data "data/1_prepared" --model_input "data/2_model" --score_report "data/3_reports" --predictions "data/4_predictions"`