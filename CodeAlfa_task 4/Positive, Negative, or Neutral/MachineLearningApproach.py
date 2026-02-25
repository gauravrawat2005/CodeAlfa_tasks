# Prepare features and labels
X = df['cleaned_text']
y = df['sentiment']  # -1, 0, 1

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

print(f"Training set size: {len(X_train)}")
print(f"Test set size: {len(X_test)}")

# Create pipelines for different classifiers
pipelines = {
    'Naive Bayes': Pipeline([
        ('vectorizer', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
        ('classifier', MultinomialNB())
    ]),
    'Logistic Regression': Pipeline([
        ('vectorizer', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
        ('classifier', LogisticRegression(random_state=42, max_iter=1000))
    ]),
    'SVM': Pipeline([
        ('vectorizer', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
        ('classifier', SVC(kernel='linear', random_state=42))
    ]),
    'Random Forest': Pipeline([
        ('vectorizer', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
}

# Train and evaluate models
results = {}
for name, pipeline in pipelines.items():
    # Train
    pipeline.fit(X_train, y_train)
    
    # Predict
    y_pred = pipeline.predict(X_test)
    
    # Evaluate
    accuracy = accuracy_score(y_test, y_pred)
    results[name] = {
        'pipeline': pipeline,
        'accuracy': accuracy,
        'predictions': y_pred
    }
    
    print(f"\n{name} Results:")
    print(f"Accuracy: {accuracy:.2%}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Negative', 'Neutral', 'Positive']))