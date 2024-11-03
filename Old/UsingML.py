import pickle
import numpy as np
import pandas as pd

# Load the model from the file
with open('ml_model.pkl', 'rb') as file:
	model = pickle.load(file)


# Use this to predict the class of a new observation from the tree
def predict_tree(tree, X_test):
	feature_idx = tree['feature_idx']
	split_point = tree['split_point']

	if isinstance(split_point, list):
		if set(X_test[feature_idx]).issubset(set(split_point)):
			if isinstance(tree['left_split'], dict):
				return predict_tree(tree['left_split'], X_test)
			else:
				return tree['left_split']
		else:
			if isinstance(tree['right_split'], dict):
				return predict_tree(tree['right_split'], X_test)
			else:
				return tree['right_split']
	else:
		if X_test[feature_idx] <= split_point:
			if isinstance(tree['left_split'], dict):
				return predict_tree(tree['left_split'], X_test)
			else:
				return tree['left_split']
		else:
			if isinstance(tree['right_split'], dict):
				return predict_tree(tree['right_split'], X_test)
			else:
				return tree['right_split']

# Use this to predict the class of a new observation from the forest
def predict_rf(tree_ls, X_test):
	pred_ls = list()
	for i in range(len(X_test)):
		ensemble_preds = [predict_tree(tree, X_test.values[i]) for tree in tree_ls]
		final_pred = max(ensemble_preds, key=ensemble_preds.count)
		pred_ls.append(final_pred)
	return np.array(pred_ls)


# Preprocess the input data
# input_data = preprocess_input_data(Pclass, Sex, Age, SibSp, Parch, Fare, Embarked)

df = pd.read_csv("appwrite_collection_final.csv")
# Also, convert the lists that are read in as strings into actual lists
for i in range(len(df)):
	count = 0
	# In each row, if there is an instance of 'KR', add 1 to the count
	if 'KR' in df['invasive'][i]:
		count += 1
	if 'JG' in df['invasive'][i]:
		count += 2
	if 'P' in df['invasive'][i]:
		count += 3
	df.loc[i, 'invasive'] = count
	count = 0
	if 'native_grass' in df['seed_type'][i]:
		count += 1
	if 'wildflower' in df['seed_type'][i]:
		count += 2
	df.loc[i, 'seed_type'] = count
features = ['invasive', 'woody_species_percentage', 'water_sources', 'seed_type', 'years_since_prescribed_burn']
input_to_predict = df[features][0:100]

# Predict the class of the input data
prediction = predict_rf(model, input_to_predict)

# Output the prediction
# print("Survived" if prediction[0] == 1 else "Did not survive")
for i in range(100):
	# print("Fall" if prediction[i] == 1 else "Spring")
	print(prediction[i])