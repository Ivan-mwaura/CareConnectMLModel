# -*- coding: utf-8 -*-
"""BOOTCAMP CODES

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17wmboPyCAHaMCFsJ0uD0dTVDRhQcQMIe

# **Loading the Data**
"""

import pandas as pd

# Load JSON data into a Pandas DataFrame
df = pd.read_json('E:\Care-connect\Model\cleaned_data.json')


# Display the first few rows of the DataFrame
print(df.head())

"""# Importing Libraries

"""

import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.model_selection import train_test_split
# Modelling
from imblearn.over_sampling import SMOTE
from sklearn.metrics import accuracy_score
from sklearn.model_selection import RepeatedStratifiedKFold, cross_validate
import xgboost as xgb
from xgboost import XGBClassifier
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler
import warnings as wr

wr.filterwarnings('ignore')
print('Libraries Imported')

"""# Feature Engineering"""

# Function to apply transformation
def transform_value(value):
    if value < 4:
        return 1
    else:
        return 0

# Apply transformation to the ANC column and create a new column 'Target Variable'
df['Target Variable'] = df['ANC'].apply(transform_value)

# Create new features
X = df.iloc[:, :-3].values

# 'ANC' is the name of the column you want to use as y
y = df['Target Variable'].values


# Creating a new DataFrame with column names
columns_to_keep = df.columns[:-3]  # Exclude the last two columns
new_data_X = pd.DataFrame(X, columns=columns_to_keep)

# Initialize the 'dropout combined' column to 0
y = y.reshape(-1, 1)  # The following code would convert the y variable to a 2-dimensional array with one row and 32156 columns:

print(new_data_X.shape)
print(y.shape)

from imblearn.over_sampling import RandomOverSampler

# Choose oversample
oversampler = RandomOverSampler(sampling_strategy='minority')

# Resample the dataset
X_resampled, y_resampled = oversampler.fit_resample(new_data_X, y)

# Convert the resampled data back to DataFrame
df_resampled = pd.concat([pd.DataFrame(X_resampled, columns=new_data_X.columns), pd.Series(y_resampled, name='Target_column')], axis=1)

"""# Model Selection"""

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Initialize the XGBoost classifier
model = XGBClassifier(subsample= 0.7, n_estimators= 190, min_child_weight= 4, max_depth= 19, learning_rate= 0.1, colsample_bytree= 0.8999999999999999, bootstrap= True)

"""# Model Training"""

# Train the model
model.fit(X_train, y_train)

"""# Model Evaluation"""

# Make predictions on the testing set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

"""# Model Deployment"""

# Save the trained model to a file for deployment
import joblib
joblib.dump(model, 'trained_model.pkl')

def predict_dropout():
    # Load the trained model
    model = joblib.load('trained_model.pkl')

    # Ask the user to input the variables
    user_input = []
    for column in new_data_X.columns:
        value = input(f"Please enter {column}: ")
        user_input.append(float(value))

    #Convert user input into a numpy array and reshape it
    user_input = np.array(user_input).reshape(1, -1)

    # Make a prediction
    prediction = model.predict(user_input)

    # Return the prediction
    return prediction

prediction = predict_dropout()

print("Predicted dropout stage:", prediction)