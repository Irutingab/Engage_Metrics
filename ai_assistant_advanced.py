import requests
import pandas as pd
import streamlit as st
from openai import OpenAI
import json
import numpy as np
from typing import Dict, List, Any

class AdvancedRAGAssistant:
    def __init__(self):
        # Ollama setup - optimized for speed
        self.ollama_url = "http://localhost:11434"
        self.model = "mistral"  # You could also try "llama3.2:1b" for faster responses
        
        # OpenAI client for local Ollama
        self.client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"  # Required but not used by Ollama
        )
        
        # Document store for RAG
        self.knowledge_base = {}
        
    def is_ollama_available(self):
        """Quick check if Ollama is running - optimized for speed"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=1)  # Faster timeout
            return response.status_code == 200
        except:
            return False
    
    def create_knowledge_base(self, dataset: pd.DataFrame) -> Dict[str, Any]:
        """Create comprehensive knowledge base from dataset - Advanced RAG pattern"""
        if dataset is None or dataset.empty:
            return {}
        
        knowledge = {
            "metadata": {
                "total_students": len(dataset),
                "columns": list(dataset.columns),
                "data_types": dataset.dtypes.to_dict()
            },
            "statistics": {},
            "insights": {},
            "relationships": {}
        }
        
        # Statistical summaries for each column
        for col in dataset.columns:
            if dataset[col].dtype in ['int64', 'float64']:
                knowledge["statistics"][col] = {
                    "mean": dataset[col].mean(),
                    "median": dataset[col].median(),
                    "std": dataset[col].std(),
                    "min": dataset[col].min(),
                    "max": dataset[col].max(),
                    "distribution": "numerical"
                }
            else:
                knowledge["statistics"][col] = {
                    "unique_values": dataset[col].unique().tolist(),
                    "value_counts": dataset[col].value_counts().to_dict(),
                    "distribution": "categorical"
                }
        
        # Key insights
        if 'Exam_Score' in dataset.columns:
            # Performance insights
            high_performers = dataset[dataset['Exam_Score'] >= 90]
            low_performers = dataset[dataset['Exam_Score'] < 60]
            
            knowledge["insights"]["performance"] = {
                "high_performers_count": len(high_performers),
                "high_performers_percentage": len(high_performers) / len(dataset) * 100,
                "low_performers_count": len(low_performers),
                "low_performers_percentage": len(low_performers) / len(dataset) * 100,
                "average_score": dataset['Exam_Score'].mean()
            }
            
            # Correlations
            if len(dataset.select_dtypes(include=[np.number]).columns) > 1:
                numeric_cols = dataset.select_dtypes(include=[np.number])
                correlations = numeric_cols.corr()['Exam_Score'].to_dict()
                knowledge["relationships"]["score_correlations"] = correlations
        
        # Parental involvement analysis
        if 'Parental_Involvement' in dataset.columns and 'Exam_Score' in dataset.columns:
            involvement_analysis = dataset.groupby('Parental_Involvement')['Exam_Score'].agg([
                'mean', 'count', 'std'
            ]).to_dict()
            knowledge["insights"]["parental_impact"] = involvement_analysis
        
        # Attendance analysis
        if 'Attendance' in dataset.columns and 'Exam_Score' in dataset.columns:
            attendance_correlation = dataset['Attendance'].corr(dataset['Exam_Score'])
            knowledge["relationships"]["attendance_performance"] = attendance_correlation
        
        self.knowledge_base = knowledge
        return knowledge
    
    def retrieve_relevant_context(self, user_question: str, dataset: pd.DataFrame) -> str:
        """Advanced retrieval based on question content - Key RAG improvement"""
        if not self.knowledge_base:
            self.create_knowledge_base(dataset)
        
        question_lower = user_question.lower()
        context_parts = []
        
        # Always include basic project info
        context_parts.append(f"""PROJECT: Engage Metrics - Student Success Analytics
MISSION: Analyze factors contributing to student academic success
DATASET: {self.knowledge_base['metadata']['total_students']} students""")
        
        # Smart context retrieval based on question keywords
        if any(word in question_lower for word in ['score', 'grade', 'performance', 'exam']):
            if 'performance' in self.knowledge_base.get('insights', {}):
                perf = self.knowledge_base['insights']['performance']
                context_parts.append(f"""PERFORMANCE DATA:
- Average Score: {perf['average_score']:.1f}
- High Performers (90+): {perf['high_performers_count']} ({perf['high_performers_percentage']:.1f}%)
- Students Needing Support (<60): {perf['low_performers_count']} ({perf['low_performers_percentage']:.1f}%)""")
        
        if any(word in question_lower for word in ['parent', 'involvement', 'family']):
            if 'parental_impact' in self.knowledge_base.get('insights', {}):
                parent_data = self.knowledge_base['insights']['parental_impact']
                context_parts.append(f"""PARENTAL INVOLVEMENT IMPACT:
- High Involvement: Avg Score {parent_data['mean'].get('High', 0):.1f}
- Medium Involvement: Avg Score {parent_data['mean'].get('Medium', 0):.1f}  
- Low Involvement: Avg Score {parent_data['mean'].get('Low', 0):.1f}""")
        
        if any(word in question_lower for word in ['attendance', 'absent', 'present']):
            if 'attendance_performance' in self.knowledge_base.get('relationships', {}):
                corr = self.knowledge_base['relationships']['attendance_performance']
                context_parts.append(f"""ATTENDANCE ANALYSIS:
- Attendance-Performance Correlation: {corr:.3f}
- Interpretation: {'Strong positive' if corr > 0.7 else 'Moderate positive' if corr > 0.4 else 'Weak'} relationship""")
        
        if any(word in question_lower for word in ['correlation', 'relationship', 'factor']):
            if 'score_correlations' in self.knowledge_base.get('relationships', {}):
                corrs = self.knowledge_base['relationships']['score_correlations']
                top_factors = sorted(corrs.items(), key=lambda x: abs(x[1]), reverse=True)[:3]
                context_parts.append(f"""TOP CORRELATED FACTORS:
{chr(10).join([f'- {factor}: {corr:.3f}' for factor, corr in top_factors if factor != 'Exam_Score'])}""")
        
        return "\n\n".join(context_parts)
    
    def generate_response(self, user_question: str, dataset: pd.DataFrame) -> str:
        """Enhanced response generation with smart context retrieval"""
        # Get relevant context using advanced retrieval
        context = self.retrieve_relevant_context(user_question, dataset)
        
        # Check for fast mode
        fast_mode = hasattr(st.session_state, 'fast_mode') and st.session_state.fast_mode
        max_tokens = 150 if fast_mode else 200
        
        # Create enhanced prompt - optimized for speed
        prompt = f"""DATA CONTEXT: {context}

QUESTION: {user_question}

Give a {'brief' if fast_mode else 'concise'}, data-driven answer using the numbers provided:"""

        # Try Ollama with performance optimizations
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert educational data analyst. Give concise, practical insights using the provided data."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,  # Adaptive based on mode
                temperature=0.4,  # Lower for more focused responses
                timeout=10  # 10 second timeout
            )
            return response.choices[0].message.content
            
        except Exception as e:
            # Intelligent fallback using knowledge base
            return self.intelligent_fallback(user_question)
    
    def intelligent_fallback(self, user_question: str) -> str:
        """Smart fallback using knowledge base instead of generic message"""
        question_lower = user_question.lower()
        
        if not self.knowledge_base:
            return "AI is currently unavailable, and I don't have dataset context loaded. Please ensure Ollama is running."
        
        # Use knowledge base for basic responses
        metadata = self.knowledge_base.get('metadata', {})
        insights = self.knowledge_base.get('insights', {})
        
        if any(word in question_lower for word in ['score', 'performance']):
            if 'performance' in insights:
                perf = insights['performance']
                return f"Based on the data: Average score is {perf['average_score']:.1f}. {perf['high_performers_count']} students (({perf['high_performers_percentage']:.1f}%)) are high performers, while {perf['low_performers_count']} students need additional support."
        
        if any(word in question_lower for word in ['parent', 'involvement']):
            if 'parental_impact' in insights:
                return "Parental involvement shows clear impact on student performance. High involvement correlates with better academic outcomes."
        
        return f"AI is temporarily unavailable. I have {metadata.get('total_students', 0)} student records ready for analysis once the AI connection is restored."
    
    def render_advanced_chat(self, dataset: pd.DataFrame):
        """Enhanced Streamlit interface with better UX"""
        st.header("🎓 Engage Metrics - Advanced AI Analyst")
        st.markdown("*Powered by Advanced RAG + Ollama*")
        
        # Enhanced status display
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if self.is_ollama_available():
                st.success("🤖 AI Online")
            else:
                st.error("🤖 AI Offline")
        
        with col2:
            if dataset is not None and not dataset.empty:
                st.info(f"📊 {len(dataset)} Students")
            else:
                st.warning("📊 No Data")
        
        with col3:
            if not self.knowledge_base:
                self.create_knowledge_base(dataset)
                st.success("🧠 Knowledge Ready")
            else:
                st.success("🧠 Knowledge Ready")
        
        # Quick insights panel
        if dataset is not None and not dataset.empty:
            with st.expander("🔍 Quick Dataset Insights", expanded=False):
                if 'performance' in self.knowledge_base.get('insights', {}):
                    perf = self.knowledge_base['insights']['performance']
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Avg Score", f"{perf['average_score']:.1f}")
                    with col_b:
                        st.metric("High Performers", f"{perf['high_performers_count']}")
                    with col_c:
                        st.metric("Need Support", f"{perf['low_performers_count']}")
        
        # Chat interface
        if "advanced_messages" not in st.session_state:
            st.session_state.advanced_messages = []
            if dataset is not None and not dataset.empty:
                welcome = f"👋 Ready to analyze {len(dataset)} student records with advanced RAG! Ask me about performance patterns, correlations, or specific insights."
                st.session_state.advanced_messages.append({"role": "assistant", "content": welcome})
        
        # Display messages
        for message in st.session_state.advanced_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Enhanced input with suggestions and performance note
        st.markdown("**💡 Try asking:** *'What factors correlate most with exam scores?'* or *'How does parental involvement affect performance?'*")
        st.caption("⚡ **Performance Tip:** For faster responses, try shorter, specific questions!")
        
        # Chat input
        if prompt := st.chat_input("Ask about patterns, correlations, insights..."):
            # Add user message
            st.session_state.advanced_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate response with timing
            with st.chat_message("assistant"):
                start_time = st.empty()
                start_time.caption("⏳ Analyzing...")
                
                import time
                response_start = time.time()
                response = self.generate_response(prompt, dataset)
                response_time = time.time() - response_start
                
                start_time.empty()  # Clear the loading message
                st.markdown(response)
                st.caption(f"⚡ Response generated in {response_time:.1f}s")
                st.session_state.advanced_messages.append({"role": "assistant", "content": response})
        
        # Enhanced controls with performance options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🧹 Clear Chat"):
                st.session_state.advanced_messages = []
                st.rerun()
        
        with col2:
            if st.button("🔄 Refresh Knowledge"):
                self.create_knowledge_base(dataset)
                st.success("Knowledge base updated!")
                st.rerun()
        
        with col3:
            # Model speed toggle
            use_fast_mode = st.toggle("⚡ Fast Mode", help="Use shorter responses for faster performance")
            if use_fast_mode:
                st.session_state.fast_mode = True
            else:
                st.session_state.fast_mode = False
