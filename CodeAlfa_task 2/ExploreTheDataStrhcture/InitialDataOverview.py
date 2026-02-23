import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

def initial_data_overview(df, dataset_name="Dataset"):
    """Complete initial data structure examination"""
    
    print(f"\n{'='*60}")
    print(f"📊 DATA STRUCTURE ANALYSIS: {dataset_name}")
    print(f"{'='*60}")
    
    # Basic info
    print(f"\n📏 BASIC INFORMATION:")
    print(f"• Number of rows: {df.shape[0]:,}")
    print(f"• Number of columns: {df.shape[1]}")
    print(f"• Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"• Duplicate rows: {df.duplicated().sum():,}")
    
    # Column overview
    print(f"\n📋 COLUMN OVERVIEW:")
    print(f"• Numeric columns: {len(df.select_dtypes(include=[np.number]).columns)}")
    print(f"• Categorical columns: {len(df.select_dtypes(include=['object', 'category']).columns)}")
    print(f"• DateTime columns: {len(df.select_dtypes(include=['datetime64']).columns)}")
    print(f"• Boolean columns: {len(df.select_dtypes(include=['bool']).columns)}")
    
    return {
        'shape': df.shape,
        'memory': df.memory_usage(deep=True).sum() / 1024**2,
        'duplicates': df.duplicated().sum(),
        'column_types': df.dtypes.value_counts().to_dict()
    }

# Example usage
df = pd.read_csv('sample_data.csv')
overview = initial_data_overview(df, "Customer Sales Data")