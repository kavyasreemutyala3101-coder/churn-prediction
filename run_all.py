"""
Master execution script for Telco Customer Churn Prediction MLOps project.
Executes all stages from the beginning of the project through to deployment and monitoring.
"""

import os
import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
PYTHON = sys.executable

STEPS = [
    {
        "name": "Lab 3: Baseline ML Pipeline",
        "command": [PYTHON, "pipelines/run_lab3_baseline.py"],
        "description": "Preprocess data, train baseline Random Forest, evaluate metrics."
    },
    {
        "name": "Lab 4: MLflow Experiment Tracking & Reproducibility",
        "command": [PYTHON, "pipelines/run_lab4_tracking.py"],
        "description": "Track runs and metrics in MLflow, test reproducible seeds."
    },
    {
        "name": "Lab 5: Production Data Pipeline",
        "command": [PYTHON, "pipelines/run_lab5_pipeline.py"],
        "description": "Schema validation, ColumnTransformer pipeline, output verification."
    },
    {
        "name": "Lab 6: Model Registry & Lifecycle Promotion",
        "command": [PYTHON, "pipelines/run_lab6_registry.py"],
        "description": "Register model in MLflow Registry, automated Champion promotion."
    },
    {
        "name": "Labs 7-10: Full Modular End-to-End MLOps Pipeline",
        "command": [PYTHON, "src/mlops_pipeline/churn_prediction_pipeline.py", "--force"],
        "description": "All 10 stages: ingest, validate, train, evaluate, quality gate, deploy, infer."
    },
    {
        "name": "Lab 11: FastAPI Endpoint Test Suite",
        "command": [PYTHON, "-m", "pytest", "-p", "no:typeguard", "tests/test_api.py", "-v"],
        "description": "23 automated tests for API endpoints, schemas, and error handling."
    },
    {
        "name": "Lab 12: Drift Monitoring & Retraining Trigger",
        "command": [PYTHON, "src/mlops_pipeline/12_data_drift.py"],
        "description": "Detect KS & JS divergence on features."
    },
    {
        "name": "Lab 12: Prediction Drift Monitoring",
        "command": [PYTHON, "src/mlops_pipeline/12_prediction_drift.py"],
        "description": "Monitor prediction and probability drift."
    },
    {
        "name": "Lab 12: Concept Drift Monitoring",
        "command": [PYTHON, "src/mlops_pipeline/12_concept_drift.py"],
        "description": "Assess metric degradation on evolving data."
    },
    {
        "name": "Lab 12: Combined Drift Analysis",
        "command": [PYTHON, "src/mlops_pipeline/12_drift_analysis.py"],
        "description": "Synthesize data, prediction, and concept drift reports."
    },
    {
        "name": "Lab 13: Automated Retraining Trigger",
        "command": [PYTHON, "src/mlops_pipeline/12_monitor_trigger.py"],
        "description": "Conditionally trigger pipeline based on drift and new data presence."
    }
]

def main():
    os.chdir(PROJECT_ROOT)
    os.makedirs("outputs/drift", exist_ok=True)
    os.makedirs("outputs/monitoring", exist_ok=True)
    os.makedirs("artifacts", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    print("=" * 80)
    print(" TELCO CHURN PREDICTION - COMPLETE PROJECT EXECUTION RUNNER")
    print(f" Working Directory : {PROJECT_ROOT}")
    print(f" Python Interpreter: {PYTHON}")
    print("=" * 80)

    results = []

    for idx, step in enumerate(STEPS, start=1):
        print(f"\n[{idx}/{len(STEPS)}] >>> {step['name']}")
        print(f"       Description: {step['description']}")
        print(f"       Command    : {' '.join(step['command'])}\n")

        res = subprocess.run(step["command"])
        status = "PASSED" if res.returncode == 0 else "FAILED"
        results.append((step["name"], status, res.returncode))

        if res.returncode != 0:
            print(f"\n[ERROR] Step '{step['name']}' exited with code {res.returncode}.")
            break

    print("\n" + "=" * 80)
    print(" EXECUTION SUMMARY")
    print("=" * 80)
    all_ok = True
    for name, status, code in results:
        status_symbol = "[OK]" if status == "PASSED" else "[FAIL]"
        print(f" {status_symbol} {name.ljust(55)} : {status}")
        if status != "PASSED":
            all_ok = False

    print("=" * 80)
    if all_ok and len(results) == len(STEPS):
        print("ALL PROJECT STAGES EXECUTED SUCCESSFULLY FROM START TO FINISH!")
    else:
        print("EXECUTION COMPLETED WITH ERRORS OR EARLY HALT.")
    print("=" * 80)

if __name__ == "__main__":
    main()
