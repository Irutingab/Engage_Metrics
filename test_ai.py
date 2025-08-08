from ai_assistant import AIAssistant
import pandas as pd

# Test the AI assistant with different types of questions
ai = AIAssistant()

# Load a sample dataset for testing
try:
    df = pd.read_csv('student_performance_cleaned.csv')
    print(f'Dataset loaded: {len(df)} students\n')
    
    # Test conversational queries
    test_questions = [
        'Hi, how are you doing?',
        'What does this project do?', 
        'What would you say about parental involvement?',
        'Tell me something interesting',
        'Hello',
        'Bonjour',
        'Thank you'
    ]
    
    for question in test_questions:
        print(f'Question: "{question}"')
        response = ai._handle_conversational_queries(question, df)
        if response:
            print(f'Response: {response[:300]}{"..." if len(response) > 300 else ""}\n')
        else:
            print('Would proceed to full AI analysis\n')
            
except Exception as e:
    print(f'Error testing: {e}')
