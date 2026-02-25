# Create word clouds for each sentiment
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for idx, (sentiment, color) in enumerate(zip(['Positive', 'Negative', 'Neutral'], 
                                             ['Greens', 'Reds', 'Blues'])):
    text = ' '.join(df[df['sentiment_label'] == sentiment]['cleaned_text'])
    
    wordcloud = WordCloud(width=800, height=400, 
                         background_color='white',
                         colormap=color,
                         max_words=50,
                         contour_width=1,
                         contour_color='steelblue').generate(text)
    
    axes[idx].imshow(wordcloud, interpolation='bilinear')
    axes[idx].axis('off')
    axes[idx].set_title(f'{sentiment} Sentiment Word Cloud', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.show()