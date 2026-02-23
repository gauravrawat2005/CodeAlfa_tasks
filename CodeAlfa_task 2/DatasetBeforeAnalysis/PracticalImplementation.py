class DataQuestionnaire:
    """Systematic approach to asking dataset questions"""
    
    def __init__(self, df, dataset_name, domain):
        self.df = df
        self.dataset_name = dataset_name
        self.domain = domain
        self.questions_answered = {}
        
    def ask_fundamental_questions(self):
        """Start with basic questions about the data"""
        print(f"\n{'='*60}")
        print(f"DATA QUESTIONNAIRE: {self.dataset_name}")
        print(f"{'='*60}")
        
        # Data quality questions
        print("\n📊 FUNDAMENTAL QUESTIONS:")
        print("-" * 40)
        print(f"1. How was this data collected?")
        print(f"2. What's the time period covered?")
        print(f"3. Who/what is the unit of analysis?")
        print(f"4. Are there known biases in collection?")
        print(f"5. What's the data update frequency?")
        
    def ask_domain_specific_questions(self):
        """Ask questions based on domain"""
        print(f"\n🎯 DOMAIN-SPECIFIC QUESTIONS ({self.domain}):")
        print("-" * 40)
        
        if self.domain == "ecommerce":
            questions = ecommerce_questions(self.df)
        elif self.domain == "finance":
            questions = financial_questions(self.df)
        elif self.domain == "healthcare":
            questions = healthcare_questions(self.df)
        else:
            questions = {"General": ["What business problem does this solve?"]}
            
        for category, q_list in questions.items():
            print(f"\n{category}:")
            for i, q in enumerate(q_list[:3], 1):  # Show top 3
                print(f"   {i}. {q}")
                
    def ask_analytical_questions(self):
        """Questions about potential analysis"""
        print(f"\n🔬 ANALYTICAL QUESTIONS:")
        print("-" * 40)
        
        questions = [
            "What's the key metric we're trying to improve?",
            "What's the baseline for comparison?",
            "What success looks like? (success metrics)",
            "What confounders might affect results?",
            "What's the minimum detectable effect?"
        ]
        
        for i, q in enumerate(questions, 1):
            print(f"{i}. {q}")
            
    def generate_analysis_plan(self):
        """Create analysis plan based on questions"""
        print(f"\n📋 PRELIMINARY ANALYSIS PLAN:")
        print("-" * 40)
        
        analysis_steps = [
            "1. Data cleaning & validation",
            "2. Exploratory data analysis (EDA)",
            "3. Hypothesis formulation",
            "4. Statistical testing",
            "5. Modeling & prediction",
            "6. Results validation",
            "7. Insights & recommendations"
        ]
        
        for step in analysis_steps:
            print(step)

# Example usage
def analyze_dataset(file_path, domain="general"):
    """Complete analysis workflow starting with questions"""
    
    # Load data
    df = pd.read_csv(file_path)
    
    # Initialize questionnaire
    qa = DataQuestionnaire(df, file_path, domain)
    
    # Ask questions
    qa.ask_fundamental_questions()
    qa.ask_domain_specific_questions()
    qa.ask_analytical_questions()
    qa.generate_analysis_plan()
    
    return qa

# Run analysis
qa = analyze_dataset("sales_data.csv", "ecommerce")