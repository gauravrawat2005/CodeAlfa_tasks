def financial_questions(df):
    """Questions for financial analysis"""
    
    questions = {
        "Performance Metrics": [
            "What's the revenue growth rate QoQ/YoY?",
            "Which segments are most/least profitable?",
            "What's the cash conversion cycle?",
            "How efficient is working capital management?"
        ],
        "Risk Assessment": [
            "What's the debt-to-equity ratio trend?",
            "How volatile are earnings?",
            "What's the customer concentration risk?",
            "Are there any red flags in financial ratios?"
        ],
        "Forecasting": [
            "What's the seasonal pattern in revenue?",
            "Which leading indicators predict performance?",
            "How accurate were previous forecasts?",
            "What external factors impact financials?"
        ]
    }
    return questions