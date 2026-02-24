def detect_text_issues(df, text_col):
    """Detect issues in text data"""
    issues = []
    
    # Basic text statistics
    text_lengths = df[text_col].astype(str).str.len()
    word_counts = df[text_col].astype(str).str.split().str.len()
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # 1. Missing/empty text
    empty_text = df[text_col].isnull() | (df[text_col].astype(str).str.strip() == '')
    if empty_text.sum() > 0:
        issues.append(f"Found {empty_text.sum()} empty text entries")
        axes[0, 0].pie([empty_text.sum(), len(df)-empty_text.sum()], 
                      labels=['Empty', 'Non-Empty'], autopct='%1.1f%%')
        axes[0, 0].set_title('Empty Text Entries')
    
    # 2. Text length distribution
    axes[0, 1].hist(text_lengths, bins=50, edgecolor='black')
    axes[0, 1].set_xlabel('Text Length')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].set_title('Text Length Distribution')
    axes[0, 1].axvline(text_lengths.median(), color='r', linestyle='--', 
                       label=f'Median: {text_lengths.median():.0f}')
    axes[0, 1].legend()
    
    # 3. Word count distribution
    axes[0, 2].hist(word_counts, bins=50, edgecolor='black')
    axes[0, 2].set_xlabel('Word Count')
    axes[0, 2].set_ylabel('Frequency')
    axes[0, 2].set_title('Word Count Distribution')
    axes[0, 2].axvline(word_counts.median(), color='r', linestyle='--', 
                       label=f'Median: {word_counts.median():.0f}')
    axes[0, 2].legend()
    
    # 4. Check for encoding issues
    special_chars = df[text_col].astype(str).str.contains('[^\x00-\x7F]').sum()
    if special_chars > 0:
        issues.append(f"Found {special_chars} entries with non-ASCII characters")
        axes[1, 0].pie([special_chars, len(df)-special_chars], 
                      labels=['Non-ASCII', 'ASCII'], autopct='%1.1f%%')
        axes[1, 0].set_title('Non-ASCII Characters')
    
    # 5. Check for duplicates in text
    duplicate_texts = df[text_col].duplicated().sum()
    if duplicate_texts > 0:
        issues.append(f"Found {duplicate_texts} duplicate text entries")
        axes[1, 1].pie([duplicate_texts, len(df)-duplicate_texts], 
                      labels=['Duplicates', 'Unique'], autopct='%1.1f%%')
        axes[1, 1].set_title('Duplicate Text')
    
    # 6. Summary
    axes[1, 2].axis('off')
    summary_text = "TEXT DATA ISSUES SUMMARY\n"
    summary_text += "="*30 + "\n\n"
    for i, issue in enumerate(issues, 1):
        summary_text += f"{i}. {issue}\n"
    axes[1, 2].text(0.1, 0.9, summary_text, fontsize=10, 
                   verticalalignment='top', fontfamily='monospace')
    
    plt.suptitle('Text Data Quality Analysis', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()
    
    return issues