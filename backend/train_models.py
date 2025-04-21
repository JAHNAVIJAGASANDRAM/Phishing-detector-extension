import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

# Create models directory if it doesn't exist
if not os.path.exists('models'):
    os.makedirs('models')

# Generate some sample training data
# This is simplified training data - in a real scenario, you'd use actual phishing/legitimate URLs
np.random.seed(42)
n_samples = 1000

# Generate features for legitimate URLs (0)
legitimate_features = np.random.normal(loc=0.3, scale=0.1, size=(n_samples // 2, 15))
legitimate_labels = np.zeros(n_samples // 2)

# Generate features for phishing URLs (1)
phishing_features = np.random.normal(loc=0.7, scale=0.1, size=(n_samples // 2, 15))
phishing_labels = np.ones(n_samples // 2)

# Combine the datasets
X = np.vstack([legitimate_features, phishing_features])
y = np.hstack([legitimate_labels, phishing_labels])

# Train Random Forest model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X, y)

# Train Decision Tree model
dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X, y)

# Save the models
joblib.dump(rf_model, 'models/random_forest_model.pkl')
joblib.dump(dt_model, 'models/decision_tree_model.pkl')

print("Models trained and saved successfully!") 