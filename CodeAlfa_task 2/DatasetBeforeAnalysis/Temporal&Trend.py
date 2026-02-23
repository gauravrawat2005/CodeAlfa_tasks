def temporal_questions(df, date_column):
    """Questions about time-based patterns"""
    
    questions = {
        "Trends": [
            f"What's the overall trend in {date_column}?",
            "Is there a significant upward/downward trend?",
            "What's the compound annual growth rate (CAGR)?"
        ],
        "Seasonality": [
            "Are there weekly patterns?",
            "What's the monthly/quarterly seasonality?",
            "Are there holiday effects?"
        ],
        "Anomalies": [
            "Are there unusual spikes/drops?",
            "What caused major deviations?",
            "Are there structural breaks in the time series?"
        ],
        "Forecasting": [
            "What methods best capture the time patterns?",
            "How far ahead can we reliably forecast?",
            "What's the forecast uncertainty?"
        ]
    }
    return questions