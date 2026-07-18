import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PowerTransformer
from sklearn.metrics import mean_squared_error, r2_score
import mlflow
import mlflow.xgboost
import pickle
import os

def main():
    # Setup MLflow
    mlflow.set_experiment("Concrete_Strength_Prediction")
    
    with mlflow.start_run():
        # Load data
        data_path = os.path.join(os.path.dirname(__file__), "concrete_data.csv")
        df = pd.read_csv(data_path)
        
        # Preprocessing: drop duplicates
        df = df.drop_duplicates()
        
        X = df.drop(columns=["Strength"])
        y = df["Strength"]
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Transform features
        transformer = PowerTransformer(method='box-cox', standardize=True)
        # Adding a small constant to avoid zero values for box-cox
        X_train_transformed = transformer.fit_transform(X_train + 1e-6)
        X_test_transformed = transformer.transform(X_test + 1e-6)
        
        # Model training
        n_estimators = 200
        learning_rate = 0.1
        max_depth = 5
        
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("learning_rate", learning_rate)
        mlflow.log_param("max_depth", max_depth)
        
        model = xgb.XGBRegressor(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            random_state=42
        )
        
        model.fit(X_train_transformed, y_train)
        
        # Evaluation
        y_pred = model.predict(X_test_transformed)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        
        print(f"Model trained. RMSE: {rmse:.4f}, R2: {r2:.4f}")
        
        # Save model bundle
        bundle = {
            "model": model,
            "transformer": transformer,
            "features": X.columns.tolist(),
            "r2": r2,
            "rmse": rmse,
            "y_min": y.min(),
            "y_max": y.max(),
            "y_mean": y.mean()
        }
        
        model_path = os.path.join(os.path.dirname(__file__), "model_bundle.pkl")
        with open(model_path, "wb") as f:
            pickle.dump(bundle, f)
            
        mlflow.log_artifact(model_path)
        print(f"Model bundle saved to {model_path}")

if __name__ == "__main__":
    main()
