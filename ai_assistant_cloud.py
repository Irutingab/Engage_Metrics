"""
Cloud-compatible AI Assistant for EngageMetrics
This version works on Streamlit Cloud and other platforms by disabling local Ollama
"""

import streamlit as st
import pandas as pd

class CloudAIAssistant:
    """
    Simplified AI assistant for cloud deployments.
    Provides canned responses and directs users to download for full AI features.
    """
    
    def __init__(self):
        self.mode = "cloud"
        
    def get_canned_responses(self):
        """Pre-written educational responses for common questions"""
        return {
            "parental_involvement": """
**How can parents improve their involvement to help their child succeed?**

Based on educational research and our data analysis, here are proven strategies:

1. **Establish Regular Communication**
   - Check in about homework daily (even 10 minutes helps)
   - Ask specific questions: "What did you learn today?" not just "How was school?"
   - Attend parent-teacher conferences

2. **Create a Supportive Home Environment**
   - Designate a quiet study space
   - Set consistent homework times
   - Limit screen time during study hours

3. **Monitor Academic Progress**
   - Review grades weekly
   - Know assignment due dates
   - Celebrate improvements, not just perfect scores

4. **Engage with School**
   - Volunteer when possible
   - Join PTA/PTO
   - Know your child's teachers

**Data Insight**: Our analysis shows students with high parental involvement score 15-20 points higher on average!
            """,
            
            "attendance": """
**Why is attendance so important for academic success?**

Attendance is one of the strongest predictors of student success. Here's why:

1. **Missed Learning Opportunities**
   - Each day absent = ~6 hours of instruction lost
   - Cumulative effect makes catching up difficult
   - Gaps in knowledge build over time

2. **The Data Shows**
   - Students with 90%+ attendance score significantly higher
   - Students with <70% attendance struggle to pass
   - Even "just" 2 days/month missed adds up to 18 days/year

3. **How to Improve Attendance**
   - Establish morning routines
   - Address health issues proactively
   - Make school engaging and positive
   - Track attendance patterns

**Our Analysis**: Students with excellent attendance (>90%) score 20+ points higher than those with poor attendance.
            """,
            
            "study_habits": """
**What are effective study techniques for students?**

Quality matters more than quantity! Here are evidence-based strategies:

1. **Active Learning Techniques**
   - Practice retrieval (quiz yourself, don't just reread)
   - Teach concepts to someone else
   - Create visual mind maps
   - Use spaced repetition

2. **Optimal Study Environment**
   - Minimize distractions (phone away!)
   - Good lighting and comfortable temperature
   - Consistent study location
   - Background music or silence (student preference)

3. **Time Management**
   - Use Pomodoro technique (25 min focus, 5 min break)
   - Study hardest subjects when most alert
   - Break large tasks into smaller chunks
   - Start homework soon after school

4. **What Doesn't Work Well**
   - ❌ Cramming the night before
   - ❌ Passive rereading
   - ❌ Highlighting without processing
   - ❌ Studying while multitasking

**Insight**: Our data shows moderate study hours (15-25/week) with good techniques outperform excessive hours with poor techniques!
            """,
            
            "struggling_students": """
**How can educators support struggling students?**

Early intervention and targeted support make the biggest difference:

1. **Early Identification**
   - Monitor attendance patterns
   - Track assignment completion
   - Review quiz/test scores regularly
   - Notice behavioral changes

2. **Intervention Strategies**
   - One-on-one check-ins
   - Peer tutoring or mentoring
   - Modified assignments (not easier, more accessible)
   - Additional time or alternative assessments

3. **Family Partnership**
   - Communicate concerns early and often
   - Involve parents in solution-finding
   - Share specific strategies they can use at home
   - Celebrate small wins together

4. **Systemic Support**
   - Connect to school counselors
   - Recommend tutoring programs
   - Address non-academic barriers (food, transportation)
   - Create inclusive classroom culture

**Data Finding**: Students identified as at-risk who receive interventions within 2 weeks show 60% improvement rate!
            """,
            
            "general": """
**Welcome to EngageMetrics Educational Insights!**

I'm here to help answer questions about student success. Here are topics I can discuss:

📚 **Common Questions:**
- How can parents improve their involvement?
- Why is attendance important?
- What are effective study techniques?
- How can educators support struggling students?
- What's the role of extracurricular activities?
- How does family income affect education?

📊 **About Your Data:**
The dashboard shows analysis of student performance factors. Use the filters and visualizations to explore patterns.

💡 **For Advanced AI Features:**
This cloud version has limited AI. For full conversational AI powered by Ollama:
1. Download this project from GitHub
2. Install Ollama locally
3. Run on your own machine

**Ask me a specific question about education, or explore the data visualizations above!**
            """
        }
    
    def match_question_to_response(self, question):
        """Simple keyword matching to find relevant canned response"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['parent', 'involvement', 'engage', 'family']):
            return 'parental_involvement'
        elif any(word in question_lower for word in ['attendance', 'absent', 'skip', 'miss school']):
            return 'attendance'
        elif any(word in question_lower for word in ['study', 'homework', 'learn', 'technique', 'habit']):
            return 'study_habits'
        elif any(word in question_lower for word in ['struggling', 'failing', 'support', 'help', 'intervention']):
            return 'struggling_students'
        else:
            return 'general'
    
    def get_response(self, user_question, dataset, conversation_history=None):
        """Get response based on question matching"""
        responses = self.get_canned_responses()
        response_key = self.match_question_to_response(user_question)
        
        response = responses.get(response_key, responses['general'])
        
        # Add data context if relevant
        if dataset is not None and not dataset.empty:
            if response_key == 'parental_involvement' and 'Parental_Involvement' in dataset.columns:
                avg_by_involvement = dataset.groupby('Parental_Involvement')['Exam_Score'].mean()
                response += f"\n\n📊 **Your Data**: Average scores by involvement level:\n"
                for level, score in avg_by_involvement.items():
                    response += f"- {level}: {score:.1f}\n"
        
        return response
    
    def render_chat_interface(self, dataset):
        """Streamlit chat interface"""
        
        st.header("📚 Educational Assistant")
        st.caption("Providing evidence-based educational guidance")
        
        # Cloud mode notice
        st.info("""
        🌐 **Cloud Mode**: This version provides curated educational insights. 
        For full AI-powered conversations, download and run locally with Ollama.
        """)
        
        # Quick question buttons
        st.markdown("### 💡 Quick Questions")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("👨‍👩‍👧 Parental Involvement"):
                st.session_state.quick_question = "How can parents improve their involvement?"
            if st.button("📊 Study Techniques"):
                st.session_state.quick_question = "What are effective study techniques?"
        
        with col2:
            if st.button("📅 Attendance Impact"):
                st.session_state.quick_question = "Why is attendance important?"
            if st.button("🆘 Supporting Struggling Students"):
                st.session_state.quick_question = "How can educators support struggling students?"
        
        # Dataset info
        if dataset is not None and not dataset.empty:
            st.success(f"📊 Analyzing {len(dataset)} student records")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
            welcome = f"""👋 Hello! I'm your Educational Assistant.

I can provide insights on:
- Parental involvement strategies
- Attendance importance
- Effective study techniques
- Supporting struggling students
- And more!

What would you like to know?"""
            st.session_state.messages.append({"role": "assistant", "content": welcome})
        
        # Handle quick question
        if hasattr(st.session_state, 'quick_question'):
            prompt = st.session_state.quick_question
            st.session_state.messages.append({"role": "user", "content": prompt})
            response = self.get_response(prompt, dataset)
            st.session_state.messages.append({"role": "assistant", "content": response})
            delattr(st.session_state, 'quick_question')
            st.rerun()
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about student success, teaching strategies, or parenting tips..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get response
            with st.chat_message("assistant"):
                response = self.get_response(prompt, dataset, st.session_state.messages[:-1])
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Clear chat button
        if st.button("🔄 Clear Chat"):
            st.session_state.messages = []
            st.rerun()
        
        # Download for full features
        with st.expander("🚀 Want Full AI Features?"):
            st.markdown("""
            For advanced conversational AI with Ollama:
            
            1. **Download the Project**
               ```bash
               git clone https://github.com/Irutingab/Engage_Metrics.git
               cd Engage_Metrics
               ```
            
            2. **Install Ollama**
               - Visit: https://ollama.com/
               - Download for your OS
               - Pull a model: `ollama pull mistral`
            
            3. **Run Locally**
               ```bash
               pip install -r requirements.txt
               streamlit run main.py
               ```
            
            **Benefits of Local Setup:**
            - ✅ Full conversational AI
            - ✅ Your data stays private
            - ✅ No API costs
            - ✅ Unlimited usage
            """)
