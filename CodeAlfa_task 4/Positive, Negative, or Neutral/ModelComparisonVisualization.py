# Compare model performance
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# 1. Model Accuracy Comparison
ax1 = axes[0, 0]
model_names = list(results.keys())
accuracies = [results[name]['accuracy'] for name in model_names]
colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']
bars = ax1.bar(model_names, accuracies, color=colors)
ax1.set_title('Model Accuracy Comparison', fontsize=14, fontweight='bold')
ax1.set_xlabel('Model')
ax1.set_ylabel('Accuracy')
ax1.set_ylim(0, 1)
# Add value labels
for bar, acc in zip(bars, accuracies):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{acc:.1%}', ha='center', va='bottom')

# 2. Confusion Matrix for Best Model
best_model_name = max(results, key=lambda x: results[x]['accuracy'])
best_model = results[best_model_name]
y_pred_best = best_model['predictions']

ax2 = axes[0, 1]
cm = confusion_matrix(y_test, y_pred_best)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax2,
            xticklabels=['Negative', 'Neutral', 'Positive'],
            yticklabels=['Negative', 'Neutral', 'Positive'])
ax2.set_title(f'Confusion Matrix - {best_model_name}', fontsize=14, fontweight='bold')
ax2.set_xlabel('Predicted')
ax2.set_ylabel('Actual')

# 3. VADER vs Best Model Comparison
ax3 = axes[0, 2]
comparison_data = pd.DataFrame({
    'Actual': df['sentiment_label'],
    'VADER': df['vader_sentiment'],
    'Best Model': [['Negative', 'Neutral', 'Positive'][pred+1] for pred in y_pred_best]
})

# Create comparison heatmap
vader_correct = (comparison_data['VADER'] == comparison_data['Actual']).sum()
model_correct = (comparison_data['Best Model'] == comparison_data['Actual']).sum()
total = len(comparison_data)

ax3.bar(['VADER', best_model_name], [vader_correct/total, model_correct/total], 
        color=['#3498db', '#2ecc71'])
ax3.set_title('Model vs VADER Accuracy', fontsize=14, fontweight='bold')
ax3.set_ylabel('Accuracy')
ax3.set_ylim(0, 1)
ax3.text(0, vader_correct/total + 0.02, f'{vader_correct}/{total}', ha='center')
ax3.text(1, model_correct/total + 0.02, f'{model_correct}/{total}', ha='center')

# 4. Sentiment Distribution Comparison
ax4 = axes[1, 0]
sentiment_comparison = pd.DataFrame({
    'Actual': df['sentiment_label'].value_counts(),
    'VADER': df['vader_sentiment'].value_counts(),
    best_model_name: pd.Series([sum(y_pred_best == -1), sum(y_pred_best == 0), sum(y_pred_best == 1)],
                              index=['Negative', 'Neutral', 'Positive'])
})
sentiment_comparison.plot(kind='bar', ax=ax4, color=['#2ecc71', '#3498db', '#e74c3c'])
ax4.set_title('Sentiment Distribution Comparison', fontsize=14, fontweight='bold')
ax4.set_xlabel('Sentiment')
ax4.set_ylabel('Count')
ax4.legend()
ax4.tick_params(axis='x', rotation=0)

# 5. Prediction Confidence (if available for Logistic Regression)
if 'Logistic Regression' in results:
    ax5 = axes[1, 1]
    lr_pipeline = results['Logistic Regression']['pipeline']
    # Get prediction probabilities
    if hasattr(lr_pipeline.named_steps['classifier'], 'predict_proba'):
        proba = lr_pipeline.predict_proba(X_test)
        confidence = np.max(proba, axis=1)
        ax5.hist(confidence, bins=20, color='#3498db', edgecolor='black', alpha=0.7)
        ax5.set_title('Prediction Confidence Distribution', fontsize=14, fontweight='bold')
        ax5.set_xlabel('Confidence Score')
        ax5.set_ylabel('Frequency')
    else:
        ax5.text(0.5, 0.5, 'Probability not available for this model', 
                ha='center', va='center', transform=ax5.transAxes)

# 6. Error Analysis
ax6 = axes[1, 2]
# Find misclassified examples
misclassified = df[df['vader_sentiment'] != df['sentiment_label']].copy()
if len(misclassified) > 0:
    misclassified['text_length'] = misclassified['text'].apply(len)
    ax6.scatter(misclassified['text_length'], [1]*len(misclassified), 
               alpha=0.6, s=100, c='red')
    ax6.set_title(f'Misclassified Examples (n={len(misclassified)})', fontsize=14, fontweight='bold')
    ax6.set_xlabel('Text Length')
    ax6.set_yticks([])
    ax6.set_ylim(0.5, 1.5)
    
    # Add text labels for a few examples
    for i, row in misclassified.head(3).iterrows():
        ax6.annotate(row['text'][:30] + '...', 
                    (row['text_length'], 1),
                    xytext=(5, 10), textcoords='offset points',
                    fontsize=8, bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.5))
else:
    ax6.text(0.5, 0.5, 'No misclassified examples', ha='center', va='center', transform=ax6.transAxes)

plt.tight_layout()
plt.show()