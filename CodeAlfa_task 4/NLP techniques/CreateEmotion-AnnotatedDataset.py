# Create a comprehensive emotion dataset
emotion_texts = {
    'joy': [
        "I'm absolutely thrilled with this wonderful news!",
        "This makes me so happy and grateful!",
        "What a delightful surprise, I'm overjoyed!",
        "I feel so blessed and content right now.",
        "This is fantastic! I'm ecstatic!",
        "My heart is full of joy and appreciation.",
        "What a beautiful day, everything is perfect!",
        "I'm bursting with happiness and excitement!",
        "This brought such a big smile to my face.",
        "I feel so lucky and cheerful today!"
    ],
    'sadness': [
        "I feel so heartbroken and alone right now.",
        "This news has left me feeling deeply sad.",
        "I'm overwhelmed with grief and sorrow.",
        "Everything seems so hopeless and gloomy.",
        "My heart aches with this terrible loss.",
        "I can't stop crying, feeling so depressed.",
        "This is so disappointing and upsetting.",
        "I feel empty and miserable inside.",
        "The sadness is just too much to bear.",
        "I'm feeling down and melancholic today."
    ],
    'anger': [
        "This is absolutely infuriating! I'm furious!",
        "I'm so angry I could scream right now!",
        "This injustice makes my blood boil!",
        "How dare they treat me this way!",
        "I'm outraged by this complete disrespect!",
        "This is maddening and completely unacceptable!",
        "I'm seething with rage about this!",
        "This provokes such irritation and frustration!",
        "I'm livid about how they handled this!",
        "This makes me so hostile and aggressive!"
    ],
    'fear': [
        "I'm terrified about what might happen.",
        "This situation fills me with dread and anxiety.",
        "I'm so scared and worried about the future.",
        "My heart is racing with fear and panic.",
        "I feel threatened and vulnerable right now.",
        "This is causing me so much stress and worry.",
        "I'm horrified by what I just saw.",
        "The uncertainty is making me so nervous.",
        "I'm trembling with fear and apprehension.",
        "This gives me such an uneasy feeling."
    ],
    'surprise': [
        "Wow! I never expected this at all!",
        "I'm completely stunned and amazed!",
        "This is so shocking and unexpected!",
        "Oh my god, I can't believe this!",
        "What a remarkable and astonishing surprise!",
        "I'm speechless, this is so unexpected!",
        "This caught me completely off guard!",
        "Incredible! I'm so surprised right now!",
        "This is absolutely mind-blowing!",
        "I'm astonished by this revelation!"
    ],
    'disgust': [
        "This is absolutely revolting and disgusting!",
        "I feel sick just looking at this.",
        "This is so gross and repulsive!",
        "I'm utterly appalled by this behavior.",
        "This makes me want to vomit.",
        "How vile and contemptible!",
        "This is so distasteful and offensive.",
        "I'm completely repulsed by this.",
        "This is nauseating and horrible!",
        "I find this utterly loathsome."
    ]
}

# Create DataFrame
data = []
for emotion, texts in emotion_texts.items():
    for text in texts:
        data.append({'text': text, 'emotion': emotion})

df = pd.DataFrame(data)
print(f"Dataset shape: {df.shape}")
print(f"\nEmotion distribution:\n{df['emotion'].value_counts()}")