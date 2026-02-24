// Sample calculated fields for deeper insights

// 1. YoY Growth Calculation
IIF(ISNULL(LOOKUP(SUM([Sales]), -12)), 
    NULL, 
    (SUM([Sales]) - LOOKUP(SUM([Sales]), -12)) / 
    LOOKUP(SUM([Sales]), -12)
)

// 2. Customer Segmentation
IF [Spending Score] > 70 THEN "High Value"
ELSEIF [Spending Score] > 40 THEN "Medium Value"
ELSE "Low Value"
END

// 3. Performance Against Target
IF SUM([Sales]) > SUM([Target]) THEN 
    "Above Target"
ELSEIF SUM([Sales]) = SUM([Target]) THEN 
    "On Target"
ELSE 
    "Below Target"
END

// 4. Rolling Average
WINDOW_AVG(SUM([Sales]), -3, 0)

// 5. Pareto Classification (80/20)
IF RUNNING_SUM(SUM([Sales])) / TOTAL(SUM([Sales])) <= 0.8 
THEN "Top 80%" 
ELSE "Bottom 20%" 
END