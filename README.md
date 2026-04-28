# Network Security MLOps Pipeline

An end-to-end MLOps project for phishing website detection that builds a machine learning pipeline from MongoDB data ingestion to FastAPI-based inference, with experiment tracking through MLflow and DagsHub, artifact handling via AWS S3, and deployment support using Docker, Amazon ECR, GitHub Actions, and EC2.[1]

The project is structured around modular pipeline components for data ingestion, validation, transformation, model training, and production inference, making it suitable for both learning MLOps concepts and deploying a practical cybersecurity classification workflow.[1]

## Overview

This project predicts whether a website-related sample is phishing or legitimate using a supervised machine learning workflow built on structured tabular features such as URL characteristics, domain signals, HTTPS indicators, traffic attributes, and other security-related columns defined in `data_schema/schema.yaml`.[1]

The architecture connects four major layers: MongoDB Atlas for data storage, a local/cloud training pipeline for model development, MLflow and DagsHub for experiment tracking, and a CI/CD deployment path using GitHub, Docker, Amazon ECR, and Amazon EC2.[1]

## Features

- End-to-end training pipeline with clear MLOps stages: data ingestion, data validation, data transformation, and model training.[1]
- MongoDB-based source ingestion for phishing dataset storage and retrieval.[1]
- Schema-driven validation using `schema.yaml` to verify column consistency and numeric data types.[1]
- Data drift detection using the Kolmogorov-Smirnov test across train and test datasets.[1]
- Missing value handling through `KNNImputer` in a preprocessing pipeline.[1]
- Multi-model training and selection using classifiers such as Random Forest, Decision Tree, Gradient Boosting, Logistic Regression, and AdaBoost.[1]
- MLflow and DagsHub integration for logging model metrics and serialized model versions.[1]
- FastAPI inference endpoint for CSV-based batch prediction.[1]
- Dockerized application setup for deployment readiness.[1]
- AWS S3 sync utility for artifact movement between local storage and cloud buckets.[1]

## Architecture

The project follows the architecture shown in the diagram you shared, with a data-to-deployment lifecycle organized into four stages.[1]

1. **Data Infrastructure**: phishing data is stored in MongoDB Atlas and accessed through the ingestion module.[1]
2. **Machine Learning Pipeline**: data is ingested, validated, transformed, and used to train the best-performing classifier.[1]
3. **MLOps & Tracking**: training runs and metrics are logged with MLflow and DagsHub, while artifacts can be synchronized to AWS S3.[1]
4. **CI/CD & Deployment**: source code is versioned in GitHub, automated through GitHub Actions, containerized with Docker, pushed to Amazon ECR, and deployable on Amazon EC2.[1]

## Tech Stack

| Category | Tools / Frameworks |
|---|---|
| Programming Language | Python [1] |
| API Framework | FastAPI, Uvicorn [1] |
| Data Storage | MongoDB Atlas, PyMongo [1] |
| Data Processing | Pandas, NumPy [1] |
| ML / Preprocessing | scikit-learn, KNNImputer, Pipeline [1] |
| Experiment Tracking | MLflow, DagsHub [1] |
| Cloud / Storage | AWS S3, Amazon ECR, Amazon EC2 [1] |
| CI/CD | GitHub, GitHub Actions, Docker [1] |
| Config / Packaging | dotenv, setuptools [1] |

## Workflow

### Data Ingestion

The ingestion component connects to MongoDB using the `MONGO_DB_URL` environment variable, exports the configured collection into a Pandas DataFrame, removes MongoDB `_id`, replaces string `na` values with `NaN`, stores a feature-store CSV, and performs a train-test split using the configured split ratio of `0.2`.[1]

The default database and collection names are `KartikMehta` and `NetworkData`, defined in the training pipeline constants.[1]

### Data Validation

The validation stage checks whether the dataset matches the expected schema from `data_schema/schema.yaml`, confirms that all columns are numeric, and writes a drift report by comparing train and test distributions with `ks_2samp`.[1]

Validated datasets are then saved into the pipeline artifact directory for downstream transformation and training.[1]

### Data Transformation

The transformation stage separates the target column `Result`, converts target values of `-1` to `0`, applies a `KNNImputer` preprocessing pipeline, generates transformed NumPy arrays, and saves the fitted preprocessing object for inference reuse.[1]

The fitted preprocessing object is also stored in `final_models/preprocessing.pkl` for production prediction through the FastAPI app.[1]

### Model Training

The trainer evaluates multiple classifiers, including Random Forest, Decision Tree, Gradient Boosting, Logistic Regression, and AdaBoost, then selects the best-performing model based on the internal evaluation report.[1]

Training metrics such as F1-score, precision, and recall are logged to MLflow, and the selected model is saved to both the configured artifact path and `final_models/model.pkl`.[1]

### Inference API

The FastAPI application provides a `/train` route to trigger the training pipeline and a `/predict` route that accepts a CSV file, loads the saved preprocessing object and model, performs predictions, and returns the results rendered as an HTML table using Jinja templates.[1]

The root route redirects to `/docs`, giving you FastAPI's interactive Swagger UI for testing endpoints.[1]

## Project Structure

```text
.
├── app.py
├── main.py
├── push_data.py
├── DockerFile
├── setup.py
├── data_schema/
│   └── schema.yaml
├── networksecurity/
    ├── cloud/
    │   └── s3_syncer.py
    ├── components/
    │   ├── data_ingestion.py
    │   ├── data_validation.py
    │   ├── data_transformation.py
    │   └── model_trainer.py
    ├── constant/
    │   └── training_pipeline/
    ├── entity/
    │   ├── artifacts.py
    │   └── config_entity.py
    ├── exception/
    │   └── exception.py
    ├── logging/
    │   └── logger.py
    ├── pipeline/
    │   ├── training_pipeline.py
    │   └── batch_prediction.py
├── final_models/
│   ├── model.pkl
│   └── preprocessing.pkl
├── mlartifacts/
└── Network_data/
    └── phisingData.csv
```

## Important Files

- `app.py` defines the FastAPI service for training and prediction endpoints.[1]
- `main.py` runs the full local training flow stage by stage.[1]
- `push_data.py` uploads raw phishing CSV records into MongoDB.[1]
- `components/data_ingestion.py` exports data from MongoDB and splits it into train and test sets.[1]
- `components/data_validation.py` checks schema consistency, numeric columns, and data drift.[1]
- `components/data_transformation.py` handles preprocessing and saves transformed artifacts.[1]
- `components/model_trainer.py` trains and tracks multiple ML models.[1]
- `cloud/s3_syncer.py` syncs folders to and from an AWS S3 bucket using AWS CLI commands.[1]
- `data_schema/schema.yaml` defines the expected feature schema and numeric columns.[1]

## Dataset Schema

The dataset contains 30 input features and 1 target column named `Result`, covering phishing-related indicators such as URL length, HTTPS token, subdomain usage, DNS record status, web traffic, Google indexing, and statistical reports.[1]

The schema file explicitly declares each column as `int64`, and the validation stage expects the same number of columns during ingestion and training.[1]

## Setup

### Prerequisites

Make sure you have the following installed or configured before running the project:[1]

- Python 3.10 or later.[1]
- MongoDB Atlas access and a valid connection string in `MONGO_DB_URL`.[1]
- AWS CLI if you want to use S3 sync features.[1]
- Docker for containerized runs.[1]
- A DagsHub and MLflow setup for experiment tracking if you want tracking enabled.[1]

### Environment Variables

Create a `.env` file in the project root with at least the following variable:[1]

```env
MONGO_DB_URL=your_mongodb_connection_string
```

The code loads environment variables using `python-dotenv` in both ingestion and API layers.[1]

### Install Dependencies

The repository includes `setup.py` and expects a `requirements.txt` file for package installation.[1]

A typical installation flow is:[1]

```bash
pip install -r requirements.txt
pip install -e .
```

## Running the Project

### 1. Push Data to MongoDB

If your phishing dataset is stored locally as CSV, first load it into MongoDB using the data upload utility:[1]

```bash
python push_data.py
```

This script converts the CSV records to JSON and inserts them into the configured MongoDB database and collection.[1]

### 2. Train the Pipeline Locally

To execute the full pipeline manually from ingestion to model training, run:[1]

```bash
python main.py
```

This triggers the sequence of ingestion, validation, transformation, and model training defined in the project modules.[1]

### 3. Run the FastAPI Application

Start the API server with:[1]

```bash
python app.py
```

Or, if preferred, launch it through Uvicorn directly:[1]

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

After startup, visit `/docs` to test the API interactively.[1]

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Redirects to FastAPI docs.[1] |
| `/train` | GET | Runs the full training pipeline.[1] |
| `/predict` | POST | Accepts a CSV file and returns predictions in table format.[1] |

## Docker Support

The project includes a `DockerFile` based on `python:3.10-slim-bookworm`, installs AWS CLI, installs Python dependencies from `requirements.txt`, and starts the app with `python3 app.py`.[1]

You can build and run it with:[1]

```bash
docker build -t network-security-mlops -f DockerFile .
docker run -p 8000:8000 network-security-mlops
```

## AWS and Deployment Flow

The architecture diagram indicates a deployment path in which GitHub Actions builds the Docker image, pushes it to Amazon ECR, and deploys it to an Amazon EC2 production instance.[1]

The S3 sync helper also shows that artifact folders can be uploaded to or downloaded from AWS S3 using the AWS CLI.[1]

## Outputs and Artifacts

The project stores important outputs in these locations:[1]

- `Artifacts/` for timestamped pipeline outputs.[1]
- `final_models/model.pkl` for the trained model.[1]
- `final_models/preprocessing.pkl` for the fitted preprocessing pipeline.[1]
- `mlartifacts/` for MLflow-related outputs.[1]
- `data_validation/drift_report/report.yaml` for drift analysis artifacts under the generated artifact directory structure.[1]

## Example Prediction Flow

1. Train the model using `/train` or `python main.py`.[1]
2. Ensure `final_models/model.pkl` and `final_models/preprocessing.pkl` exist.[1]
3. Send a CSV file containing the phishing feature columns to `/predict`.[1]
4. The API loads the preprocessor and model, predicts the result, and returns a table with a `predicted_column` appended to the uploaded data.[1]

## Future Improvements

- Add a proper `requirements.txt` if it is not already finalized in the repository.[1]
- Add model versioning and registry workflows in MLflow.[1]
- Add unit tests and CI validation checks for every pipeline stage.[1]
- Implement better batch prediction and monitoring flows in `pipeline/batch_prediction.py`.[1]
- Add authentication and production-grade API security controls.[1]
- Add automated deployment scripts for EC2 rollout from ECR.[1]

## Notes

A few file and path names in the shared project details appear slightly inconsistent, such as `DockerFile` instead of the conventional `Dockerfile`, and `phisingData.csv` instead of `phishingData.csv`, so you may want to standardize them before publishing the repository.[1]

The logging module also appears to contain commented alternative implementations, which can be cleaned up to make the codebase easier to maintain.[1]

## License

Add your preferred open-source license here, such as MIT, Apache-2.0, or another license that matches your intended use.[1]
