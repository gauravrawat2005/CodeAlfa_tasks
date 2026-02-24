visualization_best_practices = {
    "Color Usage": [
        "Use colorblind-friendly palettes",
        "Limit to 6-8 colors per chart",
        "Use sequential scales for ordered data",
        "Use diverging scales for deviation data"
    ],
    "Chart Selection": [
        "Bar charts for comparisons",
        "Line charts for trends",
        "Scatter plots for relationships",
        "Pie charts only for parts-of-whole (≤5 segments)",
        "Heatmaps for correlation matrices"
    ],
    "Layout Design": [
        "Maintain consistent margins and spacing",
        "Use grid lines sparingly",
        "Place titles at top-left or top-center",
        "Include data sources and legends"
    ],
    "Typography": [
        "Use sans-serif fonts for readability",
        "Minimum font size: 10pt for labels, 12pt for titles",
        "Maintain consistent font hierarchy"
    ],
    "Interactivity": [
        "Include tooltips for detailed data",
        "Add zoom/pan for large datasets",
        "Provide filters for drill-down analysis",
        "Include download options"
    ]
}

# Print best practices
for category, practices in visualization_best_practices.items():
    print(f"\n{category}:")
    for practice in practices:
        print(f"  • {practice}")