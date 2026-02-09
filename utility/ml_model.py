import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def get_ml_prediction(df, team, driver, circuit):
    # 1. Define Features and Target
    X = df[['team_name', 'driver_full_name', 'circuit_name']]
    y = df['is_win'] # Assuming 1 for win, 0 for loss

    # 2. Split Data (The "Testing Phase")
    # This takes 20% of your data and hides it from the model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. Create Pipeline
    preprocessor = ColumnTransformer(
        transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), ['team_name', 'driver_full_name', 'circuit_name'])]
    )
    model = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', LinearRegression())])

    # 4. Train and Verify Accuracy
    model.fit(X_train, y_train)
    
    # Check predictions on the "Hidden" 20%
    y_pred_raw = model.predict(X_test)
    y_pred_binary = [1 if p > 0.5 else 0 for p in y_pred_raw] # Convert to Win/Loss
    acc = accuracy_score(y_test, y_pred_binary)

    # 5. Final Prediction for User Input
    input_data = pd.DataFrame([[team, driver, circuit]], columns=['team_name', 'driver_full_name', 'circuit_name'])
    raw_prob = model.predict(input_data)[0]
    win_prob = max(0, min(100, round(raw_prob * 100, 2)))

    return win_prob, round(acc * 100, 2)