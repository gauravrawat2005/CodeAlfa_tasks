# Analyze important words for classification
if 'Logistic Regression' in results:
    # Get feature names and coefficients
    lr_pipeline = results['Logistic Regression']['pipeline']
    vectorizer = lr_pipeline.named_steps['vectorizer']
    lr_model = lr_pipeline.named_steps['classifier']
    
    feature_names = vectorizer.get_feature_names_out()
    coefficients = lr_model.coef_[0]
    
    # Create dataframe of features and coefficients
    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'coefficient': coefficients
    }).sort_values('coefficient', ascending=False)
    
    # Plot top positive and negative features
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    # Top positive (predict positive sentiment)
    top_positive = feature_importance.head(15)
    axes[0].barh(range(len(top_positive)), top_positive['coefficient'].values, color='#2ecc71')
    axes[0].set_yticks(range(len(top_positive)))
    axes[0].set_yticklabels(top_positive['feature'].values)
    axes[0].set_title('Top Words Indicating Positive Sentiment', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Coefficient Value')
    axes[0].invert_yaxis()
    
    # Top negative (predict negative sentiment)
    top_negative = feature_importance.tail(15).sort_values('coefficient')
    axes[1].barh(range(len(top_negative)), top_negative['coefficient'].values, color='#e74c3c')
    axes[1].set_yticks(range(len(top_negative)))
    axes[1].set_yticklabels(top_negative['feature'].values)
    axes[1].set_title('Top Words Indicating Negative Sentiment', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Coefficient Value')
    axes[1].invert_yaxis()
    
    plt.tight_layout()
    plt.show()