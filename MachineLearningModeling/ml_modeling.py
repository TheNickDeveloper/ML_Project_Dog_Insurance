import pandas as pd
import pickle
import numpy as np
from sklearn.model_selection import KFold, cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# --- 1. Load Data ---
print("--- 1. Loading Data ---")
try:
    # Ensure 'transformed_dog_bites.csv' is accessible
    df = pd.read_csv("transformed_dog_bites.csv")
    print("CSV file loaded successfully.")
    print(f"Original Data (first 5 rows):\n{df.head()}\n")
    print(f"Original Data Info:\n")
    df.info() # Check data types to confirm columns are numeric
    print("\n")
except FileNotFoundError:
    print("Error: 'transformed_dog_bites.csv' not found. Please ensure the file is in the correct directory.")
    exit()

# Define features (X) and target (y)
# IMPORTANT: All these features are now assumed to be numeric in your CSV.
# If any were one-hot encoded, you must list ALL those individual one-hot encoded columns here.
# For simplicity, this code assumes they are single numeric columns (e.g., label encoded).
features = ['Breed', 'Age', 'Gender', 'SpayNeuter', 'Borough', 'IsBite'] # 'IsBite' added back
target = 'Score'

# Check if all required columns exist
missing_cols = [col for col in features + [target] if col not in df.columns]
if missing_cols:
    print(f"Error: Missing columns in CSV file: {missing_cols}. Please check your CSV file and the 'features' list.")
    exit()

X = df[features]
y = df[target]

print(f"Features used: {features}")
print(f"Target variable: {target}\n")
print(f"Target variable statistics:\n{y.describe()}\n")

# --- 2. Preprocessing Setup ---
print("--- 2. Setting up Preprocessing ---")

# Define numerical features that you explicitly want to scale.
# 'Age' is typically a continuous numerical feature that benefits from scaling.
# The other features ('Breed', 'Gender', 'SpayNeuter', 'Borough', 'IsBite') are now numeric
# but might be label encoded (ordinal) or one-hot encoded (binary).
# For RandomForest, scaling these typically doesn't harm but also isn't strictly necessary.
# We'll scale 'Age' and pass the rest through.
numerical_features_to_scale = ['Age']

# Create a preprocessor using ColumnTransformer
# It applies StandardScaler only to `numerical_features_to_scale`.
# All other columns in `features` (which are already numeric) will be passed through without transformation.
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features_to_scale)
    ],
    remainder='passthrough' # Pass through all other columns (your now-numeric categorical features)
)

print("Preprocessing pipeline created: StandardScaler for 'Age', others passed through.\n")


# --- 3. Model Pipeline Setup ---
print("--- 3. Setting up Model Pipeline ---")
# Combine preprocessing and the model into a single pipeline
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)) # RandomForestRegressor
])

print("Model pipeline created: Preprocessing -> RandomForestRegressor\n")

# --- 4. Model Evaluation using K-Fold Cross-Validation ---
print("--- 4. Evaluating Model with K-Fold Cross-Validation ---")

# For regression, we use KFold
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Define scoring metrics for regression
scoring_metrics = ['neg_mean_squared_error', 'r2', 'neg_mean_absolute_error']

cv_results_detailed = cross_validate(model_pipeline, X, y, cv=kf,
                                     scoring=scoring_metrics,
                                     return_train_score=True)

print("Detailed Cross-Validation Results:")
print(f"  Mean R-squared (Test): {np.mean(cv_results_detailed['test_r2']):.4f} +/- {np.std(cv_results_detailed['test_r2']):.4f}")
print(f"  Mean MSE (Test): {-np.mean(cv_results_detailed['test_neg_mean_squared_error']):.4f} +/- {np.std(cv_results_detailed['test_neg_mean_squared_error']):.4f}")
print(f"  Mean MAE (Test): {-np.mean(cv_results_detailed['test_neg_mean_absolute_error']):.4f} +/- {np.std(cv_results_detailed['test_neg_mean_absolute_error']):.4f}\n")


# --- 5. Final Model Training (on the entire dataset) ---
print("--- 5. Training Final Model on Entire Dataset ---")
final_model = model_pipeline # The pipeline is now our final model
final_model.fit(X, y) # Train on all available data

print("Final model training complete on the entire dataset.\n")

# Quick sanity check on the full dataset predictions (before clipping)
y_full_pred_raw = final_model.predict(X)
full_r2 = r2_score(y, y_full_pred_raw)
full_mse = mean_squared_error(y, y_full_pred_raw)
print(f"R-squared on full dataset (sanity check, raw): {full_r2:.4f}")
print(f"MSE on full dataset (sanity check, raw): {full_mse:.4f}\n")

# --- 6. Model Export (Pickling) ---
print("--- 6. Exporting the Final Model as a Pickle File ---")
model_filename = 'dog_bite_score_predictor.pkl' # Updated filename for clarity

try:
    with open(model_filename, 'wb') as file:
        pickle.dump(final_model, file)
    print(f"Final model successfully saved to '{model_filename}'\n")
except Exception as e:
    print(f"Error saving model: {e}\n")


# --- 7. Model Import (Unpickling) for Application Use ---
print("--- 7. Importing the Model from Pickle File for Application Use ---")
loaded_model = None
try:
    with open(model_filename, 'rb') as file:
        loaded_model = pickle.load(file)
    print(f"Model successfully loaded from '{model_filename}'\n")
except FileNotFoundError:
    print(f"Error: The file '{model_filename}' was not found. Did you run the export step?\n")
except Exception as e:
    print(f"Error loading model: {e}\n")


# --- 8. Prediction with the Loaded Model (and Clipping) ---
if loaded_model:
    print("--- 8. Making Predictions with the Loaded Model (with Clipping) ---")
    # Simulate new data points for prediction in your application
    # IMPORTANT: New data MUST have the same columns as training features
    # and in the same numeric format as used during training.
    new_data = pd.DataFrame({
        'Breed': [0, 1, 2], # Example numeric values for Breed
        'Age': [3, 7, 1],
        'Gender': [0, 1, 0], # Example numeric values for Gender (e.g., Male=0, Female=1)
        'SpayNeuter': [1, 0, 2], # Example numeric values for SpayNeuter (e.g., Neutered=1, Spayed=0, Not Spayed=2)
        'Borough': [5, 3, 1], # Example numeric values for Borough
        'IsBite': [1, 0, 0] # Example numeric values for IsBite (e.g., Yes=1, No=0)
    })

    print(f"New data for prediction:\n{new_data}\n")

    # Make raw predictions using the loaded model
    new_predictions_raw = loaded_model.predict(new_data)

    # Apply clipping to constrain predictions between 0 and 100
    new_predictions_clipped = np.clip(new_predictions_raw, 0, 100)

    print("Predictions for new data (raw vs. clipped):")
    for i, (raw_pred, clipped_pred) in enumerate(zip(new_predictions_raw, new_predictions_clipped)):
        print(f"Data Point {i+1}: Raw Score = {raw_pred:.2f}, Clipped Score = {clipped_pred:.2f}")

else:
    print("Cannot proceed with predictions as the model could not be loaded.")