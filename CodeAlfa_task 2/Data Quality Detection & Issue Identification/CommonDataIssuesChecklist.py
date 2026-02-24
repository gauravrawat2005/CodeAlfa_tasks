data_issues_checklist = {
    "Missing Data": [
        "Random missing values",
        "Systematic missing patterns",
        "Missing not at random (MNAR)",
        "Excessive missing rates (>30%)"
    ],
    "Duplicate Data": [
        "Exact duplicate rows",
        "Partial duplicates",
        "Near-duplicate records",
        "Duplicate indices"
    ],
    "Outliers": [
        "Univariate outliers (Z-score > 3)",
        "Multivariate outliers",
        "Contextual outliers",
        "Invalid values (negative ages, etc.)"
    ],
    "Inconsistencies": [
        "Mixed data types",
        "Inconsistent formatting",
        "Leading/trailing spaces",
        "Case inconsistencies",
        "Special characters"
    ],
    "Distribution Issues": [
        "High skewness (>2 or <-2)",
        "Multimodal distributions",
        "Heavy tails (high kurtosis)",
        "Bimodal patterns"
    ],
    "Relationship Issues": [
        "High multicollinearity (r > 0.8)",
        "Non-linear relationships",
        "Heteroscedasticity",
        "Spurious correlations"
    ],
    "Time Series Issues": [
        "Missing timestamps",
        "Irregular intervals",
        "Seasonal patterns",
        "Trends and drift",
        "Structural breaks"
    ],
    "Categorical Issues": [
        "High cardinality",
        "Class imbalance",
        "Rare categories",
        "Label inconsistencies"
    ],
    "Text Data Issues": [
        "Encoding problems",
        "Noise and typos",
        "Stop words",
        "Stemming/lemmatization needs",
        "Language detection"
    ]
}

# Print checklist
for category, issues in data_issues_checklist.items():
    print(f"\n{category}:")
    for issue in issues:
        print(f"  • {issue}")