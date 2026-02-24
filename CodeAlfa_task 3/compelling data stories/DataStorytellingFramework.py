import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, FancyBboxPatch
import seaborn as sns
from datetime import datetime, timedelta

# Set professional style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("deep")

# Create sample business data
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='M')
n_months = len(dates)

business_data = pd.DataFrame({
    'date': dates,
    'revenue': np.random.normal(500000, 100000, n_months).cumsum() + 1000000,
    'costs': np.random.normal(300000, 50000, n_months).cumsum() + 800000,
    'customers': np.random.normal(1000, 200, n_months).cumsum() + 2000,
    'satisfaction': 75 + np.cumsum(np.random.normal(0, 2, n_months)).clip(-10, 10),
    'market_share': 15 + np.cumsum(np.random.normal(0.1, 0.3, n_months)).clip(0, 30)
})

# Add a turning point (important business event)
business_data.loc[12:, 'revenue'] += 200000 * np.arange(1, n_months-11)
business_data.loc[12:, 'customers'] += 100 * np.arange(1, n_months-11)