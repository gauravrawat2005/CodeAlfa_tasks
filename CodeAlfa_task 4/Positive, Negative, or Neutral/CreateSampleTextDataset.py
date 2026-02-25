# Create a diverse sample dataset
sample_texts = [
    # Positive reviews
    "This product is absolutely amazing! I love everything about it.",
    "Excellent service, very satisfied with the quick delivery.",
    "Best purchase I've made this year. Highly recommend to everyone!",
    "Wonderful experience, the staff was incredibly helpful and friendly.",
    "Five stars! Works perfectly and exceeded all my expectations.",
    "Great value for money, definitely buying again.",
    "I'm so happy with this, it changed my life!",
    "Perfect condition, fast shipping, couldn't ask for more.",
    "Outstanding quality, beautiful design, very impressed.",
    "Thrilled with my purchase, customer service was top-notch.",
    
    # Negative reviews
    "Terrible product, broke after one use. Very disappointed.",
    "Worst customer service ever, rude staff and no help.",
    "Complete waste of money, doesn't work as advertised.",
    "Avoid at all costs! Poor quality and expensive.",
    "Frustrating experience, took forever to arrive and damaged.",
    "Not worth the price, cheap materials, falling apart.",
    "Disappointing quality, expected much better for this brand.",
    "Horrible, wish I could return it. Don't buy this!",
    "Scam! False advertising, totally different from description.",
    "Regret buying this, customer support unresponsive.",
    
    # Neutral/Mixed reviews
    "Average product, does the job but nothing special.",
    "It's okay, not great but not terrible either.",
    "Decent quality for the price, serves its purpose.",
    "Mixed feelings about this, some good some bad.",
    "Standard product, works as expected nothing more.",
    "Fair value, meets basic requirements.",
    "Not bad but could be improved in some areas.",
    "Mediocre experience, neither impressed nor disappointed.",
    "Acceptable quality, shipping was slow though.",
    "It's fine for occasional use, wouldn't recommend for daily."
]

# Create sentiment labels (1=positive, 0=neutral, -1=negative)
sentiments = [1] * 10 + [-1] * 10 + [0] * 10

# Create DataFrame
df = pd.DataFrame({
    'text': sample_texts,
    'sentiment': sentiments,
    'sentiment_label': ['Positive']*10 + ['Negative']*10 + ['Neutral']*10
})

print("Dataset Sample:")
print(df.head(10))
print(f"\nDataset shape: {df.shape}")
print(f"\nSentiment distribution:\n{df['sentiment_label'].value_counts()}")