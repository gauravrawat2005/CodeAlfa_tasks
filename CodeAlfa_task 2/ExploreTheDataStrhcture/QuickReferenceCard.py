# Essential structure exploration commands - Quick Reference

# Load data
df = pd.read_csv('data.csv')

# 1. Basic structure
df.info()                          # Concise summary
df.describe(include='all')         # Statistical summary
df.dtypes                           # Data types only
df.columns                          # Column names list

# 2. Shape and size
df.shape                            # (rows, columns)
len(df)                             # Number of rows
df.size                              # Total elements

# 3. Data types
df.select_dtypes(include=['object']).columns  # Categorical columns
df.select_dtypes(include=['number']).columns   # Numeric columns
df.select_dtypes(include=['datetime']).columns # Date columns

# 4. Missing data
df.isnull().sum()                    # Missing per column
df.isnull().sum().sort_values(ascending=False)  # Sorted missing
(df.isnull().sum() / len(df)) * 100   # Missing percentage

# 5. Value counts
df['column'].value_counts()           # Frequency counts
df['column'].value_counts(normalize=True)  # Percentages
df.nunique()                           # Unique values per column

# 6. Memory usage
df.memory_usage(deep=True)            # Memory per column
df.memory_usage(deep=True).sum() / 1024**2  # Total in MB