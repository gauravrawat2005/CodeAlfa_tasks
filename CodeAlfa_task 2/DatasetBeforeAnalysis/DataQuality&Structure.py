import pandas as pd
import numpy as np

def explore_dataset(df):
    """Ask fundamental questions about data quality"""
    
    questions = {
        "Shape & Size": [
            f"How many rows and columns? ({df.shape[0]} rows, {df.shape[1]} columns)",
            f"What's the memory usage? ({df.memory_usage(deep=True).sum() / 1e6:.2f} MB)"
        ],
        "Data Types": [
            f"What data types exist? {df.dtypes.value_counts().to_dict()}",
            f"Are there mixed types in columns? Need to check: {df.select_dtypes(include=['object']).columns.tolist()}"
        ],
        "Missing Values": [
            f"Which columns have missing data? {df.isnull().sum()[df.isnull().sum() > 0].to_dict()}",
            f"What's the missing data pattern? {df.isnull().sum() / len(df) * 100:.1f}% overall missingness"
        ],
        "Duplicates": [
            f"Are there duplicate rows? {df.duplicated().sum()} duplicates found",
            f"Which columns should be unique? Check primary key candidates"
        ],
        "Data Ranges": [
            f"What are min/max values? Check outliers in numeric columns",
            f"Are dates within expected range? {df.select_dtypes(include=['datetime']).columns.tolist()}"
        ]
    }
    return questions

# Example usage
df = pd.read_csv('products_dataset.csv)
qa_results = explore_dataset(df)