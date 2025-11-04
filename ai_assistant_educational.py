import requests
import pandas as pd
import streamlit as st
from openai import OpenAI
import json

class EducationalAIAssistant:
    """
    Educational AI Assistant using Ollama for conversational support.
    Combines dataset insights with general educational expertise.
    """
    
    def __init__(self):
        # Ollama setup
        self.ollama_url = "http://localhost:11434"
        self.model = "gpt-oss:20b"  # Using your available model
        
        # OpenAI-compatible client for Ollama
        self.client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"  # Required but not used
        )
        
        # System context for educational expertise
        self.system_context = """You are an expert educational consultant and data analyst specializing in student success.

Your expertise includes:
- Student performance analysis and academic improvement strategies
- Parental involvement and family support techniques
- Effective teaching methods and educator support
- Study habits, time management, and learning strategies
- Understanding factors that impact academic achievement
- Evidence-based educational interventions

Your role:
- Provide thoughtful, evidence-based educational guidance
- Answer questions about how to improve student outcomes
- Offer practical advice for parents, educators, and students
- Use data insights when available, but also draw on general educational knowledge
- Be conversational, supportive, and actionable in your responses
- Give specific, practical recommendations

Communication style:
- Warm and supportive, like a knowledgeable mentor
- Provide concrete examples and actionable steps
- Balance data-driven insights with empathetic understanding
- Keep responses focused and practical (2-3 paragraphs typically)
"""
        
    def is_ollama_available(self):
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=3)
            return response.status_code == 200
        except:
            return False
    
    def check_model_availability(self):
        """Check if the specific model is available"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=3)
            if response.status_code == 200:
                models = response.json().get('models', [])
                available_models = [model['name'] for model in models]
                return self.model in available_models, available_models
            return False, []
        except:
            return False, []
    
    def get_data_insights(self, dataset):
        """Extract key insights from the dataset to inform AI responses"""
        if dataset is None or dataset.empty:
            return "No dataset currently loaded."
        
        insights = []
        insights.append(f"Analysis of {len(dataset)} student records:")
        
        try:
            # Exam performance insights
            if 'Exam_Score' in dataset.columns:
                avg_score = dataset['Exam_Score'].mean()
                top_performers = len(dataset[dataset['Exam_Score'] >= 80])
                struggling = len(dataset[dataset['Exam_Score'] < 60])
                insights.append(f"- Average exam score: {avg_score:.1f}/100")
                insights.append(f"- {top_performers} students scoring 80+, {struggling} students below 60")
            
            # Attendance patterns
            if 'Attendance' in dataset.columns:
                avg_attendance = dataset['Attendance'].mean()
                high_attendance = len(dataset[dataset['Attendance'] >= 90])
                insights.append(f"- Average attendance: {avg_attendance:.1f}%")
                insights.append(f"- {high_attendance} students with 90%+ attendance")
            
            # Parental involvement impact
            if 'Parental_Involvement' in dataset.columns and 'Exam_Score' in dataset.columns:
                involvement_impact = dataset.groupby('Parental_Involvement')['Exam_Score'].mean().to_dict()
                insights.append(f"- Parental involvement correlation with scores: {involvement_impact}")
            
            # Study hours impact
            if 'Hours_Studied' in dataset.columns and 'Exam_Score' in dataset.columns:
                correlation = dataset[['Hours_Studied', 'Exam_Score']].corr().iloc[0, 1]
                insights.append(f"- Study hours correlation with performance: {correlation:.2f}")
            
            # Extracurricular activities
            if 'Extracurricular_Activities' in dataset.columns:
                activities_dist = dataset['Extracurricular_Activities'].value_counts().to_dict()
                insights.append(f"- Extracurricular participation: {activities_dist}")
            
        except Exception as e:
            insights.append(f"- Some data analysis features unavailable")
        
        return "\n".join(insights)
    
    def create_educational_prompt(self, user_question, dataset, conversation_history=None):
        """Create a rich prompt that combines data insights with educational expertise"""
        
        # Get data insights if available
        data_context = self.get_data_insights(dataset)
        
        # Build conversation history context
        history_context = ""
        if conversation_history and len(conversation_history) > 1:
            recent_history = conversation_history[-6:]  # Last 3 exchanges
            history_context = "\n\nRecent conversation:\n"
            for msg in recent_history:
                role = msg['role'].upper()
                history_context += f"{role}: {msg['content']}\n"
        
        # Create the full prompt
        prompt = f"""{self.system_context}

CURRENT DATASET INSIGHTS:
{data_context}
{history_context}

USER QUESTION: {user_question}

Please provide a helpful, educational response. If the question relates to the data, reference specific insights. For general educational questions (like "how can parents help improve grades" or "what teaching strategies work best"), provide evidence-based advice even if not directly in the data. Be conversational and practical."""

        return prompt
    
    def get_response(self, user_question, dataset, conversation_history=None):
        """Get AI response with educational expertise"""
        
        # Check Ollama availability
        if not self.is_ollama_available():
            return "⚠️ **AI Assistant Unavailable**\n\nOllama is not running. Please start it:\n```\nollama serve\n```"
        
        # Check model availability
        model_available, available_models = self.check_model_availability()
        if not model_available:
            models_list = ", ".join(available_models) if available_models else "none"
            return f"⚠️ **Model Not Found**\n\nThe model '{self.model}' is not available.\n\nAvailable models: {models_list}\n\nTo pull the model:\n```\nollama pull {self.model}\n```"
        
        # Create educational prompt
        prompt = self.create_educational_prompt(user_question, dataset, conversation_history)
        
        # Get AI response
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7,
                stream=False
            )
            return response.choices[0].message.content
            
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg or "not found" in error_msg.lower():
                return f"⚠️ **Model Error**\n\nThe model '{self.model}' could not be loaded. Try:\n```\nollama pull {self.model}\n```\n\nOr check available models with:\n```\nollama list\n```"
            else:
                return f"⚠️ **Error**: {error_msg[:200]}"
    
    def render_chat_interface(self, dataset):
        """Streamlit chat interface with educational focus"""
        
        st.header("📚 Educational AI Assistant")
        st.caption("Powered by Ollama - Ask about student success, parenting strategies, teaching methods, and more!")
        
        # Status indicators
        col1, col2 = st.columns(2)
        with col1:
            if self.is_ollama_available():
                model_ok, models = self.check_model_availability()
                if model_ok:
                    st.success(f"✅ AI Ready - {self.model}")
                else:
                    st.error(f"⚠️ Model '{self.model}' not found")
                    if models:
                        st.info(f"Available: {', '.join(models[:3])}")
            else:
                st.error("⚠️ Ollama not running")
                with st.expander("How to start Ollama"):
                    st.code("ollama serve", language="bash")
        
        with col2:
            if dataset is not None and not dataset.empty:
                st.info(f"📊 {len(dataset)} students | {len(dataset.columns)} features")
            else:
                st.warning("No dataset loaded")
        
        # Example questions
        with st.expander("💡 Example Questions You Can Ask"):
            st.markdown("""
            **About the Data:**
            - What patterns do you see in student performance?
            - How does parental involvement affect exam scores?
            - What's the relationship between study hours and grades?
            
            **General Educational Guidance:**
            - How can parents help improve their child's grades?
            - What are effective study techniques for struggling students?
            - How can educators better support student success?
            - What role does attendance play in academic achievement?
            - How can students balance extracurricular activities and academics?
            """)
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
            # Warm welcome message
            welcome = f"""👋 Hello! I'm your Educational AI Assistant.

I can help you with:
- **Data Insights**: Analyzing the {len(dataset) if dataset is not None and not dataset.empty else '0'} student records
- **Parent Guidance**: Strategies to support your child's education
- **Teaching Methods**: Evidence-based approaches for educators
- **Student Success**: Study techniques, time management, and academic strategies

What would you like to know?"""
            st.session_state.messages.append({"role": "assistant", "content": welcome})
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask anything about student success, education strategies, or the data..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = self.get_response(
                        prompt, 
                        dataset, 
                        conversation_history=st.session_state.messages[:-1]
                    )
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Controls
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🔄 Clear Chat"):
                st.session_state.messages = []
                st.rerun()
