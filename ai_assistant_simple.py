import requests
import pandas as pd
import streamlit as st
from openai import OpenAI
import json

class SimpleAIAssistant:
    def __init__(self):
        # Ollama setup
        self.ollama_url = "http://localhost:11434"
        self.model = "mistral"
        self.dataset = "student_performance_cleaned.csv"
        
        # OpenAI client for local Ollama
        self.client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"  # Required but not used by Ollama
        )
        
    def is_ollama_available(self):
        """Quick check if Ollama is running"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def build_context(self, dataset):
        """Build RAG context from the dataset"""
        if dataset is None or dataset.empty:
            return "No dataset available."
        
        # Project context
        context = f"""PROJECT: Engage Metrics - Student Success Analytics
MISSION: Analyze factors that contribute to student academic success
FOCUS: Understanding how parental involvement, attendance, and other factors impact performance

CURRENT DATASET:
- Total Students: {len(dataset)}
- Columns Available: {list(dataset.columns)}
"""
        
        # Add basic statistics
        try:
            if 'Exam_Score' in dataset.columns:
                avg_score = dataset['Exam_Score'].mean()
                context += f"- Average Exam Score: {avg_score:.1f}\n"
            
            if 'Attendance' in dataset.columns:
                avg_attendance = dataset['Attendance'].mean()
                context += f"- Average Attendance: {avg_attendance:.1f}%\n"
                
            if 'Parental_Involvement' in dataset.columns:
                involvement_counts = dataset['Parental_Involvement'].value_counts().to_dict()
                context += f"- Parental Involvement Distribution: {involvement_counts}\n"
        except:
            pass
            
        return context
    
    def get_response(self, user_question, dataset):
        """Get AI response using RAG approach"""
        # Build context from dataset
        context = self.build_context(dataset)
        
        # Create prompt with context + question
        prompt = f"""You are an AI assistant for the Engage Metrics student analytics project.

CONTEXT:
{context}

USER QUESTION: {user_question}

Please answer the question based on the dataset context above. If the question is about data analysis, use the specific numbers provided. Be helpful and conversational."""

        # Try Ollama with OpenAI client
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message.content
            
        except Exception as e:
            # Simple fallback
            if not self.is_ollama_available():
                return "AI Assistant is currently unavailable. Please make sure Ollama is running with the Mistral model."
            else:
                return f"Sorry, I encountered an error: {str(e)[:100]}..."
    
    def render_chat_interface(self, dataset):
        """Simple Streamlit chat interface"""
        st.header("Engage Metrics AI Assistant")
        
        # Status check
        if self.is_ollama_available():
            st.success("AI Ready - Ollama + Mistral connected")
        else:
            st.error("AI Unavailable - Start Ollama with: `ollama run mistral`")
        
        # Dataset info
        if dataset is not None and not dataset.empty:
            st.info(f"Dataset loaded: {len(dataset)} students with {len(dataset.columns)} features")
        else:
            st.warning("No dataset loaded")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
            if dataset is not None and not dataset.empty:
                welcome = f"Hello! I'm ready to analyze your {len(dataset)} student records. What would you like to know?"
                st.session_state.messages.append({"role": "assistant", "content": welcome})
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about the student data..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    response = self.get_response(prompt, dataset)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Simple controls
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
