# Create visualizations to understand the text data
fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# 1. Sentiment Distribution
ax1 = axes[0, 0]
sentiment_counts = df['sentiment_label'].value_counts()
colors = ['#2ecc71', '#e74c3c', '#3498db']
bars = ax1.bar(sentiment_counts.index, sentiment_counts.values, color=colors)
ax1.set_title('Sentiment Distribution in Dataset', fontsize=14, fontweight='bold')
ax1.set_xlabel('Sentiment')
ax1.set_ylabel('Count')
# Add value labels
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}', ha='center', va='bottom')

# 2. Text Length Analysis by Sentiment
ax2 = axes[0, 1]
df['text_length'] = df['text'].apply(len)
df['word_count'] = df['text'].apply(lambda x: len(x.split()))

for sentiment, color in zip(['Positive', 'Negative', 'Neutral'], colors):
    subset = df[df['sentiment_label'] == sentiment]
    ax2.hist(subset['text_length'], alpha=0.5, label=sentiment, color=color, bins=8)
ax2.set_title('Text Length Distribution by Sentiment', fontsize=14, fontweight='bold')
ax2.set_xlabel('Text Length (characters)')
ax2.set_ylabel('Frequency')
ax2.legend()

# 3. Word Count Analysis
ax3 = axes[0, 2]
df.boxplot(column='word_count', by='sentiment_label', ax=ax3)
ax3.set_title('Word Count by Sentiment', fontsize=14, fontweight='bold')
ax3.set_xlabel('Sentiment')
ax3.set_ylabel('Word Count')
plt.suptitle('')  # Remove automatic suptitle

# 4. Most Common Words by Sentiment
from collections import Counter

def get_top_words(texts, n=10):
    all_words = ' '.join(texts).split()
    return Counter(all_words).most_common(n)

ax4 = axes[1, 0]
positive_words = get_top_words(df[df['sentiment_label'] == 'Positive']['cleaned_text'])
words, counts = zip(*positive_words)
ax4.barh(words, counts, color='#2ecc71')
ax4.set_title('Top Words in Positive Reviews', fontsize=14, fontweight='bold')
ax4.set_xlabel('Frequency')

ax5 = axes[1, 1]
negative_words = get_top_words(df[df['sentiment_label'] == 'Negative']['cleaned_text'])
words, counts = zip(*negative_words)
ax5.barh(words, counts, color='#e74c3c')
ax5.set_title('Top Words in Negative Reviews', fontsize=14, fontweight='bold')
ax5.set_xlabel('Frequency')

ax6 = axes[1, 2]
neutral_words = get_top_words(df[df['sentiment_label'] == 'Neutral']['cleaned_text'])
words, counts = zip(*neutral_words)
ax6.barh(words, counts, color='#3498db')
ax6.set_title('Top Words in Neutral Reviews', fontsize=14, fontweight='bold')
ax6.set_xlabel('Frequency')

plt.tight_layout()
plt.show()