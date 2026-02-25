from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.pipeline import Pipeline

# Prepare features
X = df['text']
y = df['emotion']

# Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

print(f"Training set size: {len(X_train)}")
print(f"Test set size: {len(X_test)}")
print(f"\nClasses: {label_encoder.classes_}")

# Create pipelines with different features
pipelines = {
    'TF-IDF + Random Forest': Pipeline([
        ('vectorizer', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ]),
    'TF-IDF + SVM': Pipeline([
        ('vectorizer', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
        ('classifier', SVC(kernel='linear', probability=True, random_state=42))
    ])
}

# Train and evaluate models
ml_results = {}
for name, pipeline in pipelines.items():
    print(f"\n{'='*50}")
    print(f"Training {name}...")
    
    # Train
    pipeline.fit(X_train, y_train)
    
    # Predict
    y_pred = pipeline.predict(X_test)
    y_pred_proba = pipeline.predict_proba(X_test)
    
    # Evaluate
    accuracy = accuracy_score(y_test, y_pred)
    ml_results[name] = {
        'pipeline': pipeline,
        'accuracy': accuracy,
        'predictions': y_pred,
        'probabilities': y_pred_proba
    }
    
    print(f"Accuracy: {accuracy:.2%}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))