def statistical_questions(df):
    """Questions requiring statistical analysis"""
    
    questions = {
        "Distributions": [
            "Are the variables normally distributed?",
            "What's the skewness/kurtosis of key metrics?",
            "Are there multimodal distributions?"
        ],
        "Relationships": [
            "What's the correlation between variables?",
            "Is there multicollinearity among predictors?",
            "Which features have strongest association with target?"
        ],
        "Comparisons": [
            "Are there significant differences between groups?",
            "Is the trend statistically significant?",
            "What's the effect size of interventions?"
        ],
        "Predictions": [
            "Which model best fits this data?",
            "What's the prediction interval vs confidence interval?",
            "How robust are the patterns across subsamples?"
        ]
    }
    return questions