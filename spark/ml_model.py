import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

# --- Dummy Data Creation for Demonstration ---
# For a real project, replace this with data read from your data lake (HDFS/Hive) or a streaming source.
np.random.seed(42)
data = pd.DataFrame({
    'feature': np.random.rand(100) * 100,   # Example feature (e.g., product popularity score)
    'price': np.random.rand(100) * 1000       # Example product price
})

# --- Data Preparation ---
X = data[['feature']]
y = data['price']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Model Training ---
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# --- Save the Model ---
# The model is saved as a file to be loaded later for real-time inference.
joblib.dump(model, 'price_forecast_model.joblib')
print("Model saved as 'price_forecast_model.joblib'")
