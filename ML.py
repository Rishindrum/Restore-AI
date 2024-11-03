import random
import pandas as pd
import numpy as np
from tqdm import tqdm
import pickle

# Using Kaggles Titanic dataset
df = pd.read_csv('train.csv')
df.head()

# Get rid of missing values - replace with average
df.loc[df['Age'].isnull(), 'Age'] = np.round(df['Age'].mean())
df.loc[df['Embarked'].isnull(), 'Embarked'] = df['Embarked'].value_counts().index[0]

# Will use seven features to create a classification RF ML

# Split data into training and testing
features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
nb_train = int(np.floor(0.9 * len(df)))
df = df.sample(frac=1, random_state=217)  # Randomize
X_train = df[features][:nb_train]
y_train = df['Survived'][:nb_train].values
X_test = df[features][nb_train:]
y_test = df['Survived'][nb_train:].values

# Constructs binary tree classifier through entropy (measurement of uncertainty/randomness)
#   Entropy is minimized when all samples in a Node belong to the same class (Essentially, all samples are the same)
#   Entropy is maximized when samples are evenly distributed across classes - Want to start uncertain!
#   Information gain is the difference in entropy before and after a split - Want to maximize information gain
def entropy(p):
    if p == 0 or p == 1:
        return 0
    else:
        return - (p * np.log2(p) + (1 - p) * np.log2(1 - p))

# The gain in information after a split (Check parent, left child, right child)
def information_gain(left_child, right_child):
    parent = left_child + right_child
    p_parent = parent.count(1) / len(parent) if len(parent) > 0 else 0
    p_left = left_child.count(1) / len(left_child) if len(left_child) > 0 else 0
    p_right = right_child.count(1) / len(right_child) if len(right_child) > 0 else 0
    IG_p = entropy(p_parent)
    IG_l = entropy(p_left)
    IG_r = entropy(p_right)
    return IG_p - len(left_child) / len(parent) * IG_l - len(right_child) / len(parent) * IG_r

# Split the data based on a feature and a threshold
def draw_bootstrap(X_train, y_train):
    bootstrap_indices = list(np.random.choice(range(len(X_train)), len(X_train), replace=True))
    oob_indices = [i for i in range(len(X_train)) if i not in bootstrap_indices]
    X_bootstrap = X_train.iloc[bootstrap_indices].values
    y_bootstrap = y_train[bootstrap_indices]
    X_oob = X_train.iloc[oob_indices].values
    y_oob = y_train[oob_indices]
    return X_bootstrap, y_bootstrap, X_oob, y_oob

# Return observations that were left out for training
def oob_score(tree, X_test, y_test):
    mis_label = 0
    for i in range(len(X_test)):
        pred = predict_tree(tree, X_test[i])
        if pred != y_test[i]:
            mis_label += 1
    return mis_label / len(X_test)

# This is the recursive function that builds the tree
# Algorithm:
# 1. Draw a bootstrap sample (Selects m features at random out of the total M features)
# 2. For each feature, find the best split point - iterate through all possible split points and find best info gain
def find_split_point(X_bootstrap, y_bootstrap, max_features):
    feature_ls = list()
    num_features = len(X_bootstrap[0])

    while len(feature_ls) <= max_features:
        feature_idx = random.sample(range(num_features), 1)
        if feature_idx not in feature_ls:
            feature_ls.extend(feature_idx)

    best_info_gain = -999
    node = None
    for feature_idx in feature_ls:
        for split_point in X_bootstrap[:, feature_idx]:
            left_child = {'X_bootstrap': [], 'y_bootstrap': []}
            right_child = {'X_bootstrap': [], 'y_bootstrap': []}

            # split children for continuous variables
            if isinstance(split_point, (int, float)):
                for i, value in enumerate(X_bootstrap[:, feature_idx]):
                    if value <= split_point:
                        left_child['X_bootstrap'].append(X_bootstrap[i])
                        left_child['y_bootstrap'].append(y_bootstrap[i])
                    else:
                        right_child['X_bootstrap'].append(X_bootstrap[i])
                        right_child['y_bootstrap'].append(y_bootstrap[i])
            # split children for list variables
            elif isinstance(split_point, list):
                for i, value in enumerate(X_bootstrap[:, feature_idx]):
                    if set(value).issubset(set(split_point)):
                        left_child['X_bootstrap'].append(X_bootstrap[i])
                        left_child['y_bootstrap'].append(y_bootstrap[i])
                    else:
                        right_child['X_bootstrap'].append(X_bootstrap[i])
                        right_child['y_bootstrap'].append(y_bootstrap[i])
            # split children for categoric variables
            else:
                for i, value in enumerate(X_bootstrap[:, feature_idx]):
                    if value == split_point:
                        left_child['X_bootstrap'].append(X_bootstrap[i])
                        left_child['y_bootstrap'].append(y_bootstrap[i])
                    else:
                        right_child['X_bootstrap'].append(X_bootstrap[i])
                        right_child['y_bootstrap'].append(y_bootstrap[i])

            split_info_gain = information_gain(left_child['y_bootstrap'], right_child['y_bootstrap'])
            if split_info_gain > best_info_gain:
                best_info_gain = split_info_gain
                left_child['X_bootstrap'] = np.array(left_child['X_bootstrap'])
                right_child['X_bootstrap'] = np.array(right_child['X_bootstrap'])
                node = {'information_gain': split_info_gain,
                        'left_child': left_child,
                        'right_child': right_child,
                        'split_point': split_point,
                        'feature_idx': feature_idx}

    return node

# Predict the class of a new observation - Creates a terminal node instead of splitting further
def terminal_node(node):
    y_bootstrap = node['y_bootstrap']
    pred = max(y_bootstrap, key=y_bootstrap.count)
    return pred

# Recursive function to predict the class of a new observation
# 1. Removes left and right children from the node
# 2. If the node is empty (0 observations within them), create a terminal node
# 3. If the depth is greater than the max depth, create a terminal node
def split_node(node, max_features, min_samples_split, max_depth, depth):
    left_child = node['left_child']
    right_child = node['right_child']

    del(node['left_child'])
    del(node['right_child'])

    if len(left_child['y_bootstrap']) == 0 or len(right_child['y_bootstrap']) == 0:
        empty_child = {'y_bootstrap': left_child['y_bootstrap'] + right_child['y_bootstrap']}
        node['left_split'] = terminal_node(empty_child)
        node['right_split'] = terminal_node(empty_child)
        return

    if depth >= max_depth:
        node['left_split'] = terminal_node(left_child)
        node['right_split'] = terminal_node(right_child)
        return node

    if len(left_child['X_bootstrap']) <= min_samples_split:
        node['left_split'] = node['right_split'] = terminal_node(left_child)
    else:
        node['left_split'] = find_split_point(left_child['X_bootstrap'], left_child['y_bootstrap'], max_features)
        split_node(node['left_split'], max_features, min_samples_split, max_depth, depth + 1)
    if len(right_child['X_bootstrap']) <= min_samples_split:
        node['right_split'] = node['left_split'] = terminal_node(right_child)
    else:
        node['right_split'] = find_split_point(right_child['X_bootstrap'], right_child['y_bootstrap'], max_features)
        split_node(node['right_split'], max_features, min_samples_split, max_depth, depth + 1)

# Builds the tree using the above functions
def build_tree(X_bootstrap, y_bootstrap, max_depth, min_samples_split, max_features):
    root_node = find_split_point(X_bootstrap, y_bootstrap, max_features)
    split_node(root_node, max_features, min_samples_split, max_depth, 1)
    return root_node

# Uses the tree to predict the class of a new observation - Modified with tqdm
def random_forest(X_train, y_train, n_estimators, max_features, max_depth, min_samples_split):
    tree_ls = list()
    oob_ls = list()
    for i in tqdm(range(n_estimators), desc="Building Trees"):
        X_bootstrap, y_bootstrap, X_oob, y_oob = draw_bootstrap(X_train, y_train)
        tree = build_tree(X_bootstrap, y_bootstrap, max_features, max_depth, min_samples_split)
        tree_ls.append(tree)
        oob_error = oob_score(tree, X_oob, y_oob)
        oob_ls.append(oob_error)
    print("OOB estimate: {:.2f}".format(np.mean(oob_ls)))
    return tree_ls

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

# Parameters necessary:
n_estimators = 100  # Number of trees in the "forest"
max_features = 3  # Number of features to consider when looking for the best split
max_depth = 5  # Maximum depth of the tree
min_samples_split = 2  # Minimum number of samples required to split a node

# Training the model
model = random_forest(X_train, y_train, n_estimators=100, max_features=3, max_depth=10, min_samples_split=2)

# Save the model to a file
with open('random_forest_model.pkl', 'wb') as file:
    pickle.dump(model, file)

# Predicting the class of the testing data
preds = predict_rf(model, X_test)
acc = sum(preds == y_test) / len(y_test)
print("Testing accuracy: {}".format(np.round(acc, 3)))