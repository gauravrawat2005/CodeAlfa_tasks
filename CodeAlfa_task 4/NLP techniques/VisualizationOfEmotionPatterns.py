# Create comprehensive emotion visualization dashboard
fig = plt.figure(figsize=(20, 15))
fig.patch.set_facecolor('#f8f9fa')

# Define grid
gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)

# 1. Emotion Distribution
ax1 = fig.add_subplot(gs[0, 0])
emotion_counts = df['emotion'].value_counts()
colors_emotion = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffe194', '#d4a5a5']
bars = ax1.bar(emotion_counts.index, emotion_counts.values, color=colors_emotion)
ax1.set_title('Emotion Distribution in Dataset', fontsize=14, fontweight='bold')
ax1.set_xlabel('Emotion')
ax1.set_ylabel('Count')
ax1.tick_params(axis='x', rotation=45)
for bar, count in zip(bars, emotion_counts.values):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{count}', ha='center', va='bottom')

# 2. Emotion Intensity Heatmap
ax2 = fig.add_subplot(gs[0, 1:3])
# Create sample emotion intensity matrix
np.random.seed(42)
intensity_matrix = np.random.rand(6, 6) * 0.8 + 0.2  # Simulated intensities
np.fill_diagonal(intensity_matrix, 1.0)  # Perfect self-correlation

emotions = emotion_lexicons.get_all_emotions()
sns.heatmap(intensity_matrix, annot=True, fmt='.2f', 
            xticklabels=emotions, yticklabels=emotions,
            cmap='YlOrRd', ax=ax2, cbar_kws={'label': 'Intensity'})
ax2.set_title('Emotion Intensity Correlation Matrix', fontsize=14, fontweight='bold')

# 3. Emotion Word Cloud
ax3 = fig.add_subplot(gs[0, 3])
emotion_text = ' '.join(df['text'])
wordcloud = WordCloud(width=800, height=400, 
                     background_color='white',
                     colormap='viridis',
                     max_words=50).generate(emotion_text)
ax3.imshow(wordcloud, interpolation='bilinear')
ax3.axis('off')
ax3.set_title('Overall Emotion Word Cloud', fontsize=14, fontweight='bold')

# 4. Emotion Radar Chart
ax4 = fig.add_subplot(gs[1, 0], projection='polar')
from math import pi

# Sample emotion profiles for different texts
categories = emotions
N = len(categories)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

# Sample data for 3 different texts
values1 = [0.8, 0.2, 0.1, 0.1, 0.3, 0.2]  # Joyful text
values2 = [0.1, 0.9, 0.2, 0.8, 0.1, 0.7]  # Angry/Fearful text
values3 = [0.2, 0.1, 0.7, 0.1, 0.8, 0.2]  # Surprising text

for values, label, color in zip([values1, values2, values3], 
                                 ['Joyful Text', 'Angry Text', 'Surprising Text'],
                                 ['green', 'red', 'orange']):
    values += values[:1]
    ax4.plot(angles, values, 'o-', linewidth=2, label=label, color=color)
    ax4.fill(angles, values, alpha=0.1, color=color)

ax4.set_xticks(angles[:-1])
ax4.set_xticklabels(categories)
ax4.set_ylim(0, 1)
ax4.set_title('Emotion Profiles Comparison', fontsize=14, fontweight='bold', pad=20)
ax4.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))

# 5. Lexicon Coverage
ax5 = fig.add_subplot(gs[1, 1])
lexicon_coverage = []
for emotion in emotions:
    words = emotion_lexicons.get_emotion_words(emotion)
    coverage = sum(1 for text in df[df['emotion'] == emotion]['text'] 
                  if any(word in text.lower() for word in words))
    lexicon_coverage.append(coverage / len(df[df['emotion'] == emotion]) * 100)

bars = ax5.bar(emotions, lexicon_coverage, color=colors_emotion)
ax5.set_title('Lexicon Coverage by Emotion', fontsize=14, fontweight='bold')
ax5.set_xlabel('Emotion')
ax5.set_ylabel('Coverage (%)')
ax5.tick_params(axis='x', rotation=45)
ax5.set_ylim(0, 100)
for bar, cov in zip(bars, lexicon_coverage):
    height = bar.get_height()
    ax5.text(bar.get_x() + bar.get_width()/2., height,
             f'{cov:.0f}%', ha='center', va='bottom')

# 6. Emotion Transition Network (simulated)
ax6 = fig.add_subplot(gs[1, 2:4])
# Create sample emotion transition matrix
transitions = np.array([
    [0.1, 0.3, 0.2, 0.1, 0.2, 0.1],  # Joy -> others
    [0.2, 0.1, 0.4, 0.2, 0.05, 0.05], # Sadness -> others
    [0.1, 0.3, 0.1, 0.3, 0.1, 0.1],   # Anger -> others
    [0.15, 0.2, 0.3, 0.1, 0.15, 0.1], # Fear -> others
    [0.3, 0.1, 0.1, 0.1, 0.1, 0.3],   # Surprise -> others
    [0.1, 0.1, 0.4, 0.1, 0.2, 0.1]    # Disgust -> others
])

sns.heatmap(transitions, annot=True, fmt='.2f',
            xticklabels=emotions, yticklabels=emotions,
            cmap='Blues', ax=ax6, cbar_kws={'label': 'Transition Probability'})
ax6.set_title('Emotion Transition Network', fontsize=14, fontweight='bold')

# 7. Model Performance Comparison
ax7 = fig.add_subplot(gs[2, :2])
models = ['Lexicon-Based', 'TF-IDF + RF', 'TF-IDF + SVM', 'Advanced Detector']
accuracies = [0.72, 0.83, 0.85, 0.91]  # Sample accuracies
colors_models = ['#95a5a6', '#3498db', '#2ecc71', '#e74c3c']
bars = ax7.bar(models, accuracies, color=colors_models)
ax7.set_title('Model Performance Comparison', fontsize=14, fontweight='bold')
ax7.set_xlabel('Model')
ax7.set_ylabel('Accuracy')
ax7.set_ylim(0, 1)
ax7.tick_params(axis='x', rotation=45)
for bar, acc in zip(bars, accuracies):
    height = bar.get_height()
    ax7.text(bar.get_x() + bar.get_width()/2., height,
             f'{acc:.0%}', ha='center', va='bottom')

# 8. Emotion Timeline (simulated)
ax8 = fig.add_subplot(gs[2, 2:4])
time_points = np.arange(20)
joy_trend = 0.5 + 0.3 * np.sin(time_points * 0.5) + np.random.normal(0, 0.1, 20)
sad_trend = 0.3 + 0.2 * np.cos(time_points * 0.5) + np.random.normal(0, 0.1, 20)
anger_trend = 0.2 + 0.15 * np.sin(time_points * 0.8) + np.random.normal(0, 0.05, 20)

ax8.plot(time_points, joy_trend, label='Joy', color='green', linewidth=2)
ax8.plot(time_points, sad_trend, label='Sadness', color='blue', linewidth=2)
ax8.plot(time_points, anger_trend, label='Anger', color='red', linewidth=2)
ax8.fill_between(time_points, 0, joy_trend, alpha=0.1, color='green')
ax8.set_title('Emotion Timeline Analysis', fontsize=14, fontweight='bold')
ax8.set_xlabel('Time')
ax8.set_ylabel('Emotion Intensity')
ax8.legend()
ax8.grid(True, alpha=0.3)

plt.suptitle('EMOTION DETECTION DASHBOARD: Comprehensive Analysis\n', 
            fontsize=20, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()