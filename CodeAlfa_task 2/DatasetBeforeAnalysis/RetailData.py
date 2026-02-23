def ecommerce_questions(df):
    """Questions for product/customer data"""
    
    questions = {
        "Product Analysis": [
            "What are the top 10 best-selling products?",
            "Which products have the highest/lowest profit margins?",
            "Is there seasonality in product sales?",
            "What's the average order value (AOV)?",
            "Which categories drive the most revenue?",
            "What's the product return rate by category?"
        ],
        "Customer Behavior": [
            "What's the customer acquisition cost (CAC)?",
            "What's the customer lifetime value (LTV)?",
            "What's the repeat purchase rate?",
            "Which customer segments are most profitable?",
            "What's the average time between purchases?",
            "Where do customers drop off in the funnel?"
        ],
        "Pricing Strategy": [
            "How price-sensitive are different customer segments?",
            "What's the optimal price point for each product?",
            "How do competitor prices affect our sales?",
            "What's the impact of discounts on profitability?"
        ]
    }
    return questions