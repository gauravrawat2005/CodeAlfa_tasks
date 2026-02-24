# Quick reference guide
statistical_tests = {
    'One Sample T-test': {
        'use': 'Compare sample mean to population mean',
        'assumptions': 'Normal distribution, independent observations',
        'code': 'stats.ttest_1samp(data, popmean)'
    },
    'Independent T-test': {
        'use': 'Compare means of two independent groups',
        'assumptions': 'Normal distribution, equal variances',
        'code': 'stats.ttest_ind(group1, group2)'
    },
    'Paired T-test': {
        'use': 'Compare means of related groups (before/after)',
        'assumptions': 'Normal distribution of differences',
        'code': 'stats.ttest_rel(before, after)'
    },
    'ANOVA': {
        'use': 'Compare means of three or more groups',
        'assumptions': 'Normal distribution, equal variances',
        'code': 'stats.f_oneway(group1, group2, group3)'
    },
    'Mann-Whitney U': {
        'use': 'Non-parametric alternative to independent t-test',
        'assumptions': 'Independent samples',
        'code': 'stats.mannwhitneyu(group1, group2)'
    },
    'Wilcoxon': {
        'use': 'Non-parametric alternative to paired t-test',
        'assumptions': 'Paired samples',
        'code': 'stats.wilcoxon(before, after)'
    },
    'Kruskal-Wallis': {
        'use': 'Non-parametric alternative to ANOVA',
        'assumptions': 'Independent samples',
        'code': 'stats.kruskal(group1, group2, group3)'
    },
    'Chi-square': {
        'use': 'Test independence of categorical variables',
        'assumptions': 'Expected frequencies > 5',
        'code': 'stats.chi2_contingency(contingency_table)'
    },
    'Pearson Correlation': {
        'use': 'Linear relationship between two continuous variables',
        'assumptions': 'Normal distribution, linear relationship',
        'code': 'stats.pearsonr(x, y)'
    },
    'Spearman Correlation': {
        'use': 'Monotonic relationship (non-parametric)',
        'assumptions': 'Monotonic relationship',
        'code': 'stats.spearmanr(x, y)'
    }
}

# Print reference
for test, details in statistical_tests.items():
    print(f"\n{test}:")
    print(f"  Use: {details['use']}")
    print(f"  Assumptions: {details['assumptions']}")
    print(f"  Code: {details['code']}")