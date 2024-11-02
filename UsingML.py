import pickle
import numpy as np
import pandas as pd

# Load the model from the file
with open('random_forest_model.pkl', 'rb') as file:
    model = pickle.load(file)

# # Predict if the following survived or not:
# Pclass = 3
# Sex = "male"
# Age = 2
# SibSp = 1
# Parch = 0
# Fare = 10
# Embarked = "S"


# Function to preprocess input data - Must create a DataFrame with the same columns as the training data
def preprocess_input_data(Pclass, Sex, Age, SibSp, Parch, Fare, Embarked):
    input_data = pd.DataFrame({
        'Pclass': [Pclass],
        'Sex': [Sex],
        'Age': [Age],
        'SibSp': [SibSp],
        'Parch': [Parch],
        'Fare': [Fare],
        'Embarked': [Embarked]
    })
    input_data['Sex'] = input_data['Sex'].map({'male': 0, 'female': 1})
    input_data['Embarked'] = input_data['Embarked'].map({'C': 0, 'Q': 1, 'S': 2})
    return input_data.astype(float)


# Use this to predict the class of a new observation from the tree
def predict_tree(tree, X_test):
    feature_idx = tree['feature_idx']

    if X_test[feature_idx] <= tree['split_point']:
        if type(tree['left_split']) == dict:
            return predict_tree(tree['left_split'], X_test)
        else:
            value = tree['left_split']
            return value
    else:
        if type(tree['right_split']) == dict:
            return predict_tree(tree['right_split'], X_test)
        else:
            return tree['right_split']


# Use this to predict the class of a new observation from the forest
def predict_rf(tree_ls, X_test):
    pred_ls = list()
    for i in range(len(X_test)):
        ensemble_preds = [predict_tree(tree, X_test.values[i]) for tree in tree_ls]
        final_pred = max(ensemble_preds, key = ensemble_preds.count)
        pred_ls.append(final_pred)
    return np.array(pred_ls)


# Preprocess the input data
# input_data = preprocess_input_data(Pclass, Sex, Age, SibSp, Parch, Fare, Embarked)

df = pd.read_csv("train.csv")
df.head()
df.loc[df['Age'].isnull(),'Age'] = np.round(df['Age'].mean())
df.loc[df['Embarked'].isnull(),'Embarked'] = df['Embarked'].value_counts().index[0]
features = ['Pclass','Sex','Age','SibSp','Parch', 'Fare', 'Embarked']
input_to_predict = df[features][3:4]

# Predict the class of the input data
prediction = predict_rf(model, input_to_predict)

# Output the prediction
print("Survived" if prediction[0] == 1 else "Did not survive")