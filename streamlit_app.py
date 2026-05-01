import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

# Define the regression models
models = {
    'Linear Regression': LinearRegression(),
    'Ridge Regression': Ridge(),
    'Lasso Regression': Lasso(),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
    'XGBoost': XGBRegressor(),
}

# Streamlit app title
st.title("Concrete Strength Prediction")

# File uploader for user data
uploaded_file = st.file_uploader("Upload your dataset (CSV file)", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file
    data = pd.read_csv(uploaded_file)
    st.write("Uploaded Dataset:")
    st.write(data.head())

    # Select features and target
    st.write("### Select Features and Target")
    features = st.multiselect("Select feature columns", options=data.columns)
    target = st.selectbox("Select target column", options=data.columns)

    if features and target:
        X = data[features]
        y = data[target]

        # Split the data
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Model selection
        st.write("### Select a Model")
        model_name = st.selectbox("Choose a regression model", options=list(models.keys()))
        model = models[model_name]

        # Train the model
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # Display results
        from sklearn.metrics import r2_score, mean_squared_error
        r2 = r2_score(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)

        st.write(f"### Model: {model_name}")
        st.write(f"R² Score: {r2:.2f}")
        st.write(f"Mean Squared Error: {mse:.2f}")

        # Allow user to make predictions
        st.write("### Make Predictions")
        input_data = {feature: st.number_input(f"Input {feature}", value=0.0) for feature in features}
        if st.button("Predict"):
            input_df = pd.DataFrame([input_data])
            prediction = model.predict(input_df)[0]
            st.write(f"Predicted {target}: {prediction:.2f}")