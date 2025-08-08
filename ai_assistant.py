import requests
import pandas as pd
import json
import pandas as pd

class AIAssistant:
    def __init__(self, ollama_url="http://localhost:11434", model="mistral"):
        self.ollama_url = ollama_url
        self.model = model
        self.conversation_history = []
    
    def add_message(self, role, content):
        """Add a message to conversation history"""
        self.conversation_history.append({"role": role, "content": content})
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def _format_conversation_history(self, max_messages=4):
        """Format recent conversation history for AI context"""
        if not self.conversation_history:
            return "No previous conversation."
        
        recent_messages = self.conversation_history[-max_messages:]
        formatted = []
        for msg in recent_messages[:-1]:  # Exclude current message
            role = "User" if msg["role"] == "user" else "Assistant"
            formatted.append(f"{role}: {msg['content']}")
        
        return "\n".join(formatted) if formatted else "No previous conversation."
    
    def get_response(self, user_input, dashboard_data=None, full_dataset=None):
        """Get intelligent response with enhanced conversational abilities"""
        # Add user message to history
        self.add_message("user", user_input)
        
        try:
            # Check for basic greetings and casual questions first
            user_lower = user_input.lower().strip()
            
            # Handle greetings
            if any(greeting in user_lower for greeting in ['hi', 'hello', 'hey', 'good morning', 'good afternoon']):
                response = "Hello! I'm your AI assistant for the Engage Metrics dashboard. I can help you analyze student performance data, answer questions about attendance, parental involvement, and academic success. What would you like to know?"
                self.add_message("assistant", response)
                return response
            
            # Handle "how are you" questions
            if any(phrase in user_lower for phrase in ['how are you', 'how do you do', 'whats up', "what's up"]):
                response = "I'm doing great, thank you for asking! I'm here and ready to help you explore the student performance data. Is there anything specific you'd like to analyze or learn about?"
                self.add_message("assistant", response)
                return response
            
            # Handle project-related questions
            if any(phrase in user_lower for phrase in ['what does this project do', 'what is this project', 'tell me about this project', 'project description']):
                response = "This is the Engage Metrics project - a comprehensive student performance dashboard that analyzes how different factors affect academic success. We examine relationships between parental involvement, school attendance, study hours, and student grades. The dashboard provides interactive visualizations and insights to help understand what drives student achievement. What aspect would you like to explore?"
                self.add_message("assistant", response)
                return response
            
            # Build educational context for data analysis questions
            context = "You are an intelligent educational data analyst AI assistant. You help analyze student performance data including exam scores, attendance rates, and parental involvement."
            
            # Add real data context if available
            if full_dataset is not None and len(full_dataset) > 0:
                context += f"\n\nCurrent dataset: {len(full_dataset)} students"
                
                if 'Exam_Score' in full_dataset.columns:
                    avg_score = full_dataset['Exam_Score'].mean()
                    high_performers = len(full_dataset[full_dataset['Exam_Score'] >= 90])
                    at_risk = len(full_dataset[full_dataset['Exam_Score'] < 60])
                    context += f"\nScores: Average {avg_score:.1f}, {high_performers} high performers (90+), {at_risk} at-risk (<60)"
                
                if 'Attendance' in full_dataset.columns:
                    avg_attendance = full_dataset['Attendance'].mean()
                    excellent_attendance = len(full_dataset[full_dataset['Attendance'] > 90])
                    poor_attendance = len(full_dataset[full_dataset['Attendance'] < 80])
                    context += f"\nAttendance: Average {avg_attendance:.1f}%, {excellent_attendance} excellent (>90%), {poor_attendance} poor (<80%)"
                
                if 'Parental_Involvement' in full_dataset.columns:
                    involvement_counts = full_dataset['Parental_Involvement'].value_counts().to_dict()
                    context += f"\nParental involvement: {involvement_counts}"
            else:
                context += "\n\nNo student data currently loaded."
            
            # Enhanced prompt for conversational responses
            prompt = f"""{context}

Conversation History:
{self._format_conversation_history()}

User question: {user_input}

Instructions: Be conversational and friendly. Answer the user's question directly and helpfully. If they're asking about data, use the specific numbers provided above and provide insights. If they're asking for custom analysis not covered by existing visualizations, mention that you can perform correlation analysis, group comparisons, and statistical summaries. Keep responses informative but concise and natural."""
            
            # Check if this might need custom analysis
            analysis_keywords = ['analyze', 'correlation', 'relationship', 'compare', 'difference', 'statistics', 'trend']
            needs_analysis = any(keyword in user_lower for keyword in analysis_keywords)
            
            if needs_analysis and full_dataset is not None:
                # Try to provide some custom analysis along with AI response
                custom_analysis = self.perform_custom_analysis(user_input, full_dataset)
                context += f"\n\nCustom Analysis Result: {custom_analysis}"
            
            # Make AI request with optimal settings for Mistral
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": 100,  # Shorter for faster responses
                        "temperature": 0.3,  # Focused but creative
                        "top_p": 0.9,
                        "repeat_penalty": 1.1
                    }
                },
                timeout=10  # Reduced timeout for faster responses
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get("response", "").strip()
                
                if ai_response:
                    self.add_message("assistant", ai_response)
                    return ai_response
            
            # Quick fallback for when AI is slow/unavailable
            fallback_response = self._get_fallback_response(user_input, full_dataset)
            self.add_message("assistant", fallback_response)
            return fallback_response
            
        except Exception as e:
            # Enhanced fallback system
            fallback_response = self._get_fallback_response(user_input, full_dataset)
            self.add_message("assistant", fallback_response)
            return fallback_response
    
    def perform_custom_analysis(self, question, full_dataset):
        """Perform custom data analysis based on user question"""
        if full_dataset is None or len(full_dataset) == 0:
            return "No data available for analysis."
        
        try:
            import pandas as pd
            import numpy as np
            from scipy import stats
            
            question_lower = question.lower()
            
            # Identify what the user wants to analyze
            if any(word in question_lower for word in ['correlation', 'relationship', 'connected', 'related']):
                # Correlation analysis
                numeric_cols = full_dataset.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) >= 2:
                    corr_matrix = full_dataset[numeric_cols].corr()
                    # Find strongest correlations
                    strong_corr = []
                    for i in range(len(corr_matrix.columns)):
                        for j in range(i+1, len(corr_matrix.columns)):
                            corr_val = corr_matrix.iloc[i, j]
                            if abs(corr_val) > 0.3:  # Strong correlation threshold
                                strong_corr.append(f"{corr_matrix.columns[i]} and {corr_matrix.columns[j]}: {corr_val:.3f}")
                    
                    if strong_corr:
                        return f"Strong correlations found:\n" + "\n".join(strong_corr[:5])
                    else:
                        return "No strong correlations found between numeric variables."
            
            elif any(word in question_lower for word in ['compare', 'difference', 'between']):
                # Comparison analysis
                if 'Parental_Involvement' in full_dataset.columns and 'Exam_Score' in full_dataset.columns:
                    comparison = full_dataset.groupby('Parental_Involvement')['Exam_Score'].agg(['mean', 'count']).round(2)
                    result = "Average exam scores by parental involvement:\n"
                    for level, row in comparison.iterrows():
                        result += f"{level}: {row['mean']} (n={row['count']})\n"
                    return result
            
            elif any(word in question_lower for word in ['predict', 'forecast', 'estimate']):
                return "I can help analyze trends in the current data. For predictions, I'd recommend using the correlation insights to understand which factors most influence student performance."
            
            # Default: provide basic statistics
            if 'Exam_Score' in full_dataset.columns:
                stats_summary = full_dataset['Exam_Score'].describe()
                return f"Exam Score Statistics:\nMean: {stats_summary['mean']:.2f}\nMedian: {stats_summary['50%']:.2f}\nStd Dev: {stats_summary['std']:.2f}\nMin: {stats_summary['min']:.2f}\nMax: {stats_summary['max']:.2f}"
            
            return "I can analyze correlations, comparisons between groups, and provide statistical summaries. What specific aspect would you like me to explore?"
            
        except Exception as e:
            return f"Analysis error: {str(e)}"
    
    def _get_fallback_response(self, user_input, full_dataset):
        """Provide intelligent fallback responses when AI is unavailable"""
        user_lower = user_input.lower().strip()
        
        # Handle greetings
        if any(greeting in user_lower for greeting in ['hi', 'hello', 'hey', 'good morning', 'good afternoon']):
            return "Hello! I'm your AI assistant for the Engage Metrics dashboard. I can help you analyze student performance data. What would you like to know?"
        
        # Handle "how are you" questions
        if any(phrase in user_lower for phrase in ['how are you', 'how do you do', 'whats up', "what's up"]):
            return "I'm doing great! I'm here to help you explore the student performance data. What would you like to analyze?"
        
        # Handle project questions
        if any(phrase in user_lower for phrase in ['what does this project do', 'what is this project', 'tell me about this project']):
            return "This is the Engage Metrics project - a student performance dashboard that analyzes relationships between parental involvement, attendance, and academic success. What aspect interests you?"
        
        # Data-related questions
        if full_dataset is not None and len(full_dataset) > 0:
            if any(word in user_lower for word in ['score', 'grade', 'performance']):
                avg_score = full_dataset.get('Exam_Score', pd.Series()).mean()
                if not pd.isna(avg_score):
                    return f"The average exam score in our dataset is {avg_score:.1f}. I can provide more detailed analysis about student performance factors."
            
            if any(word in user_lower for word in ['attendance']):
                avg_attendance = full_dataset.get('Attendance', pd.Series()).mean()
                if not pd.isna(avg_attendance):
                    return f"The average attendance rate is {avg_attendance:.1f}%. Attendance shows strong correlation with academic performance."
            
            if any(word in user_lower for word in ['parent', 'involvement']):
                if 'Parental_Involvement' in full_dataset.columns:
                    involvement_counts = full_dataset['Parental_Involvement'].value_counts()
                    return f"Parental involvement levels: {dict(involvement_counts)}. Higher involvement typically correlates with better academic outcomes."
        
        # Analysis requests
        if any(word in user_lower for word in ['analyze', 'analysis', 'correlation', 'relationship']):
            if full_dataset is not None:
                analysis_result = self.perform_custom_analysis(user_input, full_dataset)
                return f"Here's the analysis: {analysis_result}"
            else:
                return "I can perform various analyses including correlations, group comparisons, and statistical summaries. Load some data and I'll help you explore it!"
        
        # Default response
        return "I'm here to help analyze student performance data. You can ask about exam scores, attendance, parental involvement, or request custom analysis. What would you like to explore?"
    
    def render_streamlit_interface(self, dataset, dashboard_context):
        """Render the AI assistant chat interface in Streamlit"""
        import streamlit as st
        
        # Update the instance variables with current data
        self.dataset = dataset
        self.dashboard_context = dashboard_context
        
        st.subheader("AI Assistant")
        st.write("Ask me anything about the student performance data!")
        
        # Chat container
        chat_container = st.container()
        
        # Display chat history
        with chat_container:
            for message in self.conversation_history:
                if message["role"] == "user":
                    st.chat_message("user").write(message["content"])
                else:
                    st.chat_message("assistant").write(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Type your question here..."):
            # Display user message
            st.chat_message("user").write(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = self.get_response(prompt)
                st.write(response)
