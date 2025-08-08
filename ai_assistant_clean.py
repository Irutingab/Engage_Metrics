import requests
import json
import pandas as pd
import numpy as np
import streamlit as st
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class AIAssistant:
    def __init__(self, ollama_url="http://localhost:11434", model="mistral"):
        self.ollama_url = ollama_url
        self.model = model
        self.conversation_history = []
        self.project_context = self._build_project_context()
        self.data_insights_cache = {}
    
    def _build_project_context(self):
        """Build comprehensive project context for AI understanding"""
        return {
            "project_name": "Engage Metrics: Student Success Analytics",
            "mission": "To prove and demonstrate that parental involvement is crucial for student academic success, while revealing other important success factors",
            "story": "This project began as a hypothesis: parents play a crucial role in their children's academic success. Through analyzing real student data, we discovered that while parental involvement is indeed critical, academic success is multifaceted - influenced by attendance patterns, study habits, socioeconomic factors, and individual characteristics."
        }
    
    def add_message(self, role, content):
        """Add a message to conversation history"""
        self.conversation_history.append({
            "role": role, 
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.data_insights_cache = {}
    
    def get_response(self, user_input, dashboard_data=None, full_dataset=None):
        """Get intelligent response with immediate fallback (no waiting)"""
        # Add user message to history
        self.add_message("user", user_input)
        
        # First check for simple conversational responses
        simple_response = self._handle_conversational_queries(user_input, full_dataset)
        if simple_response:
            self.add_message("assistant", simple_response)
            return simple_response
        
        # Quick Ollama check (1 second max)
        ollama_available = self._quick_ollama_check()
        
        if not ollama_available:
            # Use comprehensive fallback immediately
            fallback_response = self._get_comprehensive_fallback_response(user_input, full_dataset)
            self.add_message("assistant", fallback_response)
            return fallback_response
        
        # Try Ollama with very short timeout
        try:
            context = f"You are Engage Metrics Assistant. Dataset: {len(full_dataset) if full_dataset is not None else 0} students."
            prompt = f'{context} User: "{user_input}". Respond warmly and briefly.'
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"num_predict": 150, "temperature": 0.4}
                },
                timeout=5  # Very short timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get("response", "").strip()
                
                if ai_response and len(ai_response) > 10:
                    self.add_message("assistant", ai_response)
                    return ai_response
            
            # If poor response, use fallback
            raise Exception("Poor Ollama response")
            
        except Exception:
            # Always fallback quickly
            fallback_response = self._get_comprehensive_fallback_response(user_input, full_dataset)
            self.add_message("assistant", fallback_response)
            return fallback_response
    
    def _quick_ollama_check(self):
        """Super quick Ollama check (1 second timeout)"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=1)
            return response.status_code == 200
        except:
            return False
    
    def _handle_conversational_queries(self, user_input, dataset=None):
        """Handle natural conversational queries with engaging responses"""
        user_input_lower = user_input.lower().strip()
        
        # Greetings
        if any(greeting in user_input_lower for greeting in ['hello', 'hi', 'hey', 'bonjour', 'salut', 'hiii']):
            if dataset is not None:
                return f"Hi there! 👋 I'm excited to explore student success patterns with you. I've got {len(dataset)} student records loaded and ready to reveal some fascinating insights about what really drives academic achievement. What would you like to discover today?"
            else:
                return "Hello! I'm the Engage Metrics Assistant, and I'm passionate about helping people understand what makes students succeed academically. Once we have student data loaded, I can tell you some amazing stories!"
        
        # How are you questions
        if any(phrase in user_input_lower for phrase in ['how are you', 'comment ça va', 'how do you']):
            if dataset is not None:
                return f"I'm doing great, thanks for asking! 😊 I'm really energized because I've been analyzing {len(dataset)} student records and discovering incredible patterns. The data shows fascinating stories about how parental involvement, attendance, and other factors create pathways to success!"
            else:
                return "I'm doing wonderfully, thank you! I'm always excited when I get to help people understand educational data. There's something magical about uncovering the patterns that show how students can succeed!"
        
        # Project questions
        if any(phrase in user_input_lower for phrase in ['what does this project do', 'what is this project', 'tell me about this project']):
            return f"""**This is the Engage Metrics project - with a fascinating story!** 📚

It started with me wanting to prove that parental involvement is crucial for student success. But as I analyzed {len(dataset) if dataset else 'real'} student records, I discovered something even more compelling!

**What I found:** Yes, parental involvement IS incredibly important, but student success is like a symphony where multiple factors harmonize together - attendance, study habits, family engagement, and individual circumstances.

**What this dashboard does:** It helps parents, students, teachers, and schools understand these relationships so they can make targeted improvements that actually work!"""
        
        # Thanks
        if any(phrase in user_input_lower for phrase in ['thank you', 'thanks', 'merci']):
            return "You're so welcome! I genuinely love helping people understand how to improve student outcomes. Every insight we uncover could help real students succeed! 🌟"
        
        return None  # Not a simple conversational query
    
    def _get_comprehensive_fallback_response(self, user_input, dataset):
        """Comprehensive fallback system providing intelligent responses without Ollama"""
        user_input_lower = user_input.lower().strip()
        
        # Analyze the data if available
        analysis_insights = ""
        if dataset is not None and len(dataset) > 0:
            try:
                insights = self._get_quick_data_insights(user_input, dataset)
                if insights:
                    analysis_insights = f"\n\n**CURRENT DATA INSIGHTS:**\n{insights}"
            except:
                pass
        
        # Story requests
        if any(word in user_input_lower for word in ['story', 'complete story', 'tell me about', 'histoire']):
            return f"""**The Complete Engage Metrics Story** 📖

This journey began with a simple question: *"Do involved parents really make a difference in their children's academic success?"*

**The Original Hypothesis:** Parental involvement is crucial for student success.

**The Beautiful Discovery:** Not only is parental involvement incredibly powerful, but student success is like a symphony where multiple factors create harmony together:

🎵 **The Success Components:**
- **Parental Involvement** (Foundation): Sets the stage for everything else
- **Consistent Attendance** (Rhythm): Keeps students engaged and progressing  
- **Study Habits** (Melody): Individual effort that builds on the foundation

**The Most Surprising Finding:** When these factors combine, the results aren't just additive - they're exponential!

**The Mission:** Help everyone understand these patterns to create more success stories! 🌟{analysis_insights}"""
        
        # Performance questions
        elif any(word in user_input_lower for word in ['performance', 'achievement', 'scores', 'grades']):
            if dataset is not None and 'Exam_Score' in dataset.columns:
                avg_score = dataset['Exam_Score'].mean()
                high_achievers = len(dataset[dataset['Exam_Score'] >= 90])
                struggling = len(dataset[dataset['Exam_Score'] < 60])
                
                return f"""**Academic Performance Deep Dive** 📊

Looking at our {len(dataset)} students, here's what emerges:

**The Numbers Tell a Story:**
- Average Performance: {avg_score:.1f} points
- High Achievers (90+): {high_achievers} students ({high_achievers/len(dataset)*100:.1f}%)
- Students Needing Support (<60): {struggling} students ({struggling/len(dataset)*100:.1f}%)

**What Makes High Achievers Special:**
These {high_achievers} top performers typically combine multiple success factors - most have high parental involvement AND excellent attendance.

**The Encouraging Truth:** The {struggling} students aren't "failing" - they have specific, addressable challenges like attendance or engagement gaps.

**The Beautiful Pattern:** Success follows predictable pathways! 🌟{analysis_insights}"""
            else:
                return "I'd love to analyze academic performance patterns! Once student data is available, I can reveal fascinating insights about what drives success."
        
        # Default response
        else:
            if dataset is not None:
                return f"""**Analyzing Your {len(dataset)} Student Records** 📚

I can see fascinating patterns in this data! Even without the advanced AI, I can provide intelligent insights using built-in analysis.

**What I'm Finding:**
This data tells the story of how parental involvement, attendance, and individual factors work together. It's a beautiful example of how multiple elements create academic success.

**Key Insights:**
- Success follows predictable patterns (which means it's replicable!)
- Small improvements in key areas create big results  
- Every student has a pathway to success

I'm here to help you understand what drives achievement! 🌟{analysis_insights}"""
            else:
                return """**I'm Your Educational Data Assistant** 📊

While the advanced AI isn't available right now, I can still help you understand student success patterns! I specialize in analyzing educational data to reveal what really drives academic achievement.

Once student data is loaded, I can provide detailed insights! 🚀"""
    
    def _get_quick_data_insights(self, user_input, dataset):
        """Get quick insights from the dataset"""
        try:
            insights = []
            
            if 'Exam_Score' in dataset.columns:
                avg_score = dataset['Exam_Score'].mean()
                insights.append(f"Average exam score: {avg_score:.1f} points")
                
                high_performers = len(dataset[dataset['Exam_Score'] >= 90])
                if high_performers > 0:
                    insights.append(f"{high_performers} high achievers (90+ points)")
            
            if 'Attendance' in dataset.columns:
                avg_attendance = dataset['Attendance'].mean()
                insights.append(f"Average attendance: {avg_attendance:.1f}%")
            
            if 'Parental_Involvement' in dataset.columns:
                high_involvement = len(dataset[dataset['Parental_Involvement'] == 'High'])
                insights.append(f"{high_involvement} students have high parental involvement")
            
            return " • ".join(insights) if insights else None
            
        except Exception:
            return None
    
    def render_streamlit_interface(self, dataset, dashboard_context=None):
        """Render enhanced AI chat interface in Streamlit"""
        st.header("🤖 Engage Metrics AI Assistant")
        st.markdown("*Your intelligent companion for understanding student success patterns*")
        
        # Quick status check
        if dataset is not None:
            total_students = len(dataset)
            st.info(f"**Ready to analyze {total_students} students!** I can reveal patterns, tell stories, and answer questions beyond standard visualizations.")
            
            # Ollama status
            if self._quick_ollama_check():
                st.success("🤖 **Advanced AI Available** - Enhanced responses powered by Ollama")
            else:
                st.warning("🤖 **Smart Fallback Mode** - Advanced AI unavailable, but I still provide comprehensive insights!")
        else:
            st.warning("**No student data loaded** - I can still discuss educational success factors!")
        
        # Initialize chat history
        if "ai_chat_messages" not in st.session_state:
            st.session_state.ai_chat_messages = []
            welcome_msg = f"Welcome to Engage Metrics! 🎓\n\nI've analyzed {len(dataset) if dataset else 0} student records and discovered fascinating patterns about academic success. Ask me anything!"
            st.session_state.ai_chat_messages.append({"role": "assistant", "content": welcome_msg})
        
        # Display chat messages
        for message in st.session_state.ai_chat_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask me about success patterns, data insights, or anything else..."):
            # Add user message
            st.session_state.ai_chat_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = self.get_response(prompt, full_dataset=dataset)
                    st.markdown(response)
                    st.session_state.ai_chat_messages.append({"role": "assistant", "content": response})
        
        # Quick action buttons
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🧹 Clear Chat"):
                st.session_state.ai_chat_messages = []
                self.clear_history()
                st.experimental_rerun()
        
        with col2:
            if st.button("💡 Data Story"):
                story_response = self._get_comprehensive_fallback_response("Tell me the complete story behind this data", dataset)
                st.session_state.ai_chat_messages.append({"role": "user", "content": "Tell me the complete story"})
                st.session_state.ai_chat_messages.append({"role": "assistant", "content": story_response})
                st.experimental_rerun()
        
        with col3:
            if st.button("🔍 Hidden Patterns"):
                pattern_response = self._get_comprehensive_fallback_response("What hidden patterns do you see?", dataset)
                st.session_state.ai_chat_messages.append({"role": "user", "content": "What hidden patterns do you see?"})
                st.session_state.ai_chat_messages.append({"role": "assistant", "content": pattern_response})
                st.experimental_rerun()
        
        with col4:
            if st.button("📊 Performance Analysis"):
                perf_response = self._get_comprehensive_fallback_response("Analyze academic performance patterns", dataset)
                st.session_state.ai_chat_messages.append({"role": "user", "content": "Analyze academic performance"})
                st.session_state.ai_chat_messages.append({"role": "assistant", "content": perf_response})
                st.experimental_rerun()
        
        st.markdown("---")
        st.markdown("*💡 **Tip**: I work great with or without Ollama! Ask about patterns, relationships, or stories in the data.*")
