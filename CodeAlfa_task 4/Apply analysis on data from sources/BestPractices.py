"""
MULTI-SOURCE SENTIMENT ANALYSIS: KEY FINDINGS

1. Amazon Reviews [citation:4][citation:7]:
   - Strong correlation between star ratings and text sentiment (87% agreement)
   - Emojis significantly improve sentiment detection accuracy (up to 97%) [citation:4]
   - Helpfulness votes correlate with review length and sentiment extremity
   - Recommendation: Use ensemble methods combining ratings, text, and emojis

2. Social Media [citation:2][citation:8]:
   - Platform-specific sentiment patterns: Bluesky most positive, Voat most negative/controversial
   - Toxicity levels vary significantly by platform (Voat shows highest toxicity) [citation:8]
   - Engagement (likes, reposts) correlates with sentiment extremity
   - Recommendation: Platform-specific models needed for accurate analysis

3. News Articles [citation:3][citation:9]:
   - Financial news requires specialized lexicons (positive/negative financial terms)
   - Topic significantly influences sentiment (sports most positive, politics most mixed)
   - Headline sentiment often differs from article content
   - Recommendation: Use domain-specific models (financial, political, sports)

4. Cross-Source Patterns:
   - Emotion distribution varies: Joy dominant in reviews, anger/fear in social media
   - News tends toward neutral, while social media shows more extreme sentiment
   - Confidence scores highest for Amazon (clear rating signals), lowest for social media
   - Temporal patterns show weekly cycles in social media, event-driven in news

5. Technical Best Practices:
   - Use FAIR-compliant datasets with standardized structures [citation:8]
   - Implement emoji-enhanced models for social/e-commerce data [citation:4]
   - Consider platform-specific biases in cross-platform analysis [citation:2]
   - Validate with human-annotated ground truth when available [citation:1][citation:6]
"""