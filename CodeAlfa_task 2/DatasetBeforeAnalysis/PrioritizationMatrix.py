def prioritize_questions(questions):
    """Prioritize questions based on impact and feasibility"""
    
    priority_matrix = {
        "High Impact, Easy": [],    # Do first
        "High Impact, Hard": [],     # Plan carefully
        "Low Impact, Easy": [],      # Quick wins
        "Low Impact, Hard": []       # Consider skipping
    }
    
    for question in questions:
        impact = assess_impact(question)      # 1-10 scale
        feasibility = assess_feasibility(question)  # 1-10 scale
        
        if impact >= 7 and feasibility >= 7:
            priority_matrix["High Impact, Easy"].append(question)
        elif impact >= 7 and feasibility < 7:
            priority_matrix["High Impact, Hard"].append(question)
        elif impact < 7 and feasibility >= 7:
            priority_matrix["Low Impact, Easy"].append(question)
        else:
            priority_matrix["Low Impact, Hard"].append(question)
            
    return priority_matrix

def assess_impact(question):
    """Estimate business/analytical impact"""
    # Implementation depends on context
    pass

def assess_feasibility(question):
    """Estimate difficulty of answering"""
    # Implementation depends on data/ resources
    pass