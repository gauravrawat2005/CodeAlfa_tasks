import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# NLP and ML libraries
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import transformers
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

# Visualization
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Download required data
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("deep")