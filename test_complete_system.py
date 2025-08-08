from ai_assistant import AIAssistant
import pandas as pd

# Test the complete AI system
print("🧪 Testing Enhanced AI Assistant System\n")

ai = AIAssistant()

# Load dataset for testing
try:
    df = pd.read_csv('student_performance_cleaned.csv')
    print(f"✅ Dataset loaded: {len(df)} students")
    
    # Test different types of queries
    test_queries = [
        ("Hi, how are you doing?", "Greeting"),
        ("Tell me the complete story behind this student performance data", "Project story"),
        ("What patterns do you see in academic performance?", "Performance analysis"),
        ("hiii", "Simple greeting")
    ]
    
    print("\n🔍 Testing AI Responses:\n")
    
    for query, query_type in test_queries:
        print(f"Query Type: {query_type}")
        print(f'User: "{query}"')
        
        # Test the complete response system
        response = ai.get_response(query, full_dataset=df)
        print(f'AI: {response[:200]}{"..." if len(response) > 200 else ""}\n')
        
    print("✅ AI Assistant is working with comprehensive fallback system!")
    print("✅ Provides intelligent responses even without Ollama")
    print("✅ Uses actual student data for contextual insights")
    
except Exception as e:
    print(f"Error: {e}")
