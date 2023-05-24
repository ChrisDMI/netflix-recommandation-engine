from ray.job_submission import JobSubmissionClient
import ast

with open(".env") as my_file:
    file = my_file.read()

AWS_ACCESS_KEY_ID = ast.literal_eval(file)['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = ast.literal_eval(file)['AWS_SECRET_ACCESS_KEY']
BACKEND_STORE_URI = ast.literal_eval(file)['BACKEND_STORE_URI']

job_submitter = JobSubmissionClient(address="http://127.0.0.1:8265")
job_id = job_submitter.submit_job(
    entrypoint="python train.py",
    runtime_env={
        "working_dir": "./",
        "pip": ["numpy", "joblib", "scikit-learn", "scikit-surprise", "mlflow"],
        # Environment variables for our MLFlow sample app server 👇
        "env_vars": {
            "MLFLOW_EXPERIMENT_ID": "1",
            "MLFLOW_TRACKING_URI": "https://chris-mlflow-tracking.herokuapp.com/",
            "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
            "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
            "BACKEND_STORE_URI": BACKEND_STORE_URI,
            "ARTIFACT_STORE_URI": "s3://netflix-project-bucket/mlflow/",
             }
    }
)
print(f"Job submitted with id: {job_id}")
