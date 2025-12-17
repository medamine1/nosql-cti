import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load dataset
df = pd.read_csv(r'C:\Users\Othmane\OneDrive\Desktop\nosql\train_dataset.csv')
df.columns = df.columns.str.strip()

# Clean inf / NaN
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)

# 🔥 Binary label
df['BinaryLabel'] = df['Label'].apply(
    lambda x: 'Benign' if x == 'Benign' else 'Malicious'
)

# Features / Target
X = df.drop(columns=['Label', 'BinaryLabel'])
y = df['BinaryLabel']

# Train / Test split (stratified)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Model (anti-overfitting)
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    min_samples_leaf=10,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Cross-validation
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(model, X, y, cv=skf, scoring='f1_macro')

print("\nCV F1 scores:", cv_scores)
print("Mean CV F1:", cv_scores.mean())

# Save model
joblib.dump(model, 'model/model.pkl')
print("\n✅ Binary IDS model saved")
