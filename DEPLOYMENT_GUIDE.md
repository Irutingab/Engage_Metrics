# 🚀 EngageMetrics Deployment Guide

## Overview: Making Your App Publicly Available

There are several ways to deploy EngageMetrics, each with different trade-offs:

| Method | Difficulty | Cost | Best For | Time to Deploy |
|--------|-----------|------|----------|----------------|
| **Streamlit Cloud** | ⭐ Easy | Free | Quick demos, MVP | 10 minutes |
| **Hugging Face Spaces** | ⭐ Easy | Free | AI/ML projects | 15 minutes |
| **Railway** | ⭐⭐ Medium | $5-20/mo | Small scale | 30 minutes |
| **Render** | ⭐⭐ Medium | Free-$25/mo | Production-lite | 30 minutes |
| **AWS/Azure/GCP** | ⭐⭐⭐⭐ Hard | $20-100/mo | Large scale | 2-4 hours |
| **Docker + VPS** | ⭐⭐⭐ Medium | $5-15/mo | Full control | 1-2 hours |

---

## 🎯 RECOMMENDED: Streamlit Cloud (Easiest & Free!)

### Why Start Here:
- ✅ **100% Free** for public apps
- ✅ **No DevOps knowledge needed**
- ✅ **Auto-deploys from GitHub**
- ✅ **Built-in HTTPS & custom domains**
- ✅ **Perfect for Streamlit apps**

### ⚠️ Limitations:
- ❌ **Ollama won't work** (requires local installation)
- ❌ Limited to 1GB RAM on free tier
- ❌ Public apps only (unless you pay)
- ❌ Sleep after 7 days of inactivity

### **Step-by-Step Deployment:**

#### **1. Prepare Your Repository**

**a) Create `.streamlit/config.toml` (for better UI):**
```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
enableCORS = false
port = 8501
```

**b) Update `requirements.txt`** (remove Ollama dependencies for now):
```txt
streamlit==1.45.1
pandas==2.2.3
numpy==2.1.3
matplotlib==3.10.0
seaborn==0.13.2
plotly==5.24.1
requests==2.32.3
```

**c) Create `.gitignore`:**
```gitignore
__pycache__/
*.py[cod]
*$py.class
*.so
.env
.venv
venv/
*.csv
*.ipynb_checkpoints/
.DS_Store
```

**d) Create `README.md` with live demo link** (update after deployment):
```markdown
# EngageMetrics - Student Success Analytics Dashboard

🔗 **Live Demo**: https://your-app-name.streamlit.app

[Rest of your README...]
```

#### **2. Push to GitHub**

```bash
# Initialize git (if not already)
git init
git add .
git commit -m "Prepare for Streamlit Cloud deployment"

# Create GitHub repo and push
git remote add origin https://github.com/Irutingab/Engage_Metrics.git
git branch -M main
git push -u origin main
```

#### **3. Deploy on Streamlit Cloud**

1. Go to **https://share.streamlit.io/**
2. Click **"New app"**
3. Connect your GitHub account
4. Select:
   - Repository: `Irutingab/Engage_Metrics`
   - Branch: `main`
   - Main file path: `main.py`
5. Click **"Deploy!"**

**Your app will be live at**: `https://engage-metrics.streamlit.app/`

⏱️ **Total time: 10 minutes!**

---

## 🤖 Option 2: Streamlit Cloud + AI Workaround

Since Ollama won't work on Streamlit Cloud, here are alternatives:

### **Option A: Use OpenAI API (Recommended)**

**Pros**: 
- ✅ Works on any cloud platform
- ✅ Better AI quality
- ✅ Reliable and fast

**Cons**:
- ❌ Costs money (~$0.01-0.05 per conversation)
- ❌ Data sent to OpenAI

**Implementation:**

```python
# ai_assistant_cloud.py
import openai
import streamlit as st
import os

class CloudAIAssistant:
    def __init__(self):
        # Get API key from Streamlit secrets
        self.api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
        openai.api_key = self.api_key
        
    def get_response(self, user_question, dataset, conversation_history=None):
        # Same logic as EducationalAIAssistant, but uses OpenAI
        prompt = self.create_educational_prompt(user_question, dataset, conversation_history)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Or gpt-4
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI temporarily unavailable: {str(e)}"
```

**Add to Streamlit secrets** (on streamlit.io dashboard):
```toml
OPENAI_API_KEY = "sk-your-api-key-here"
```

**Cost estimate**: ~$1-5/month for 1000 users

---

### **Option B: Use Free Hugging Face Models**

```python
# ai_assistant_huggingface.py
from transformers import pipeline
import streamlit as st

class HuggingFaceAIAssistant:
    def __init__(self):
        # Load a free model (runs on your server)
        self.model = pipeline("text-generation", model="facebook/opt-350m")
    
    def get_response(self, user_question, dataset):
        prompt = self.create_educational_prompt(user_question, dataset)
        response = self.model(prompt, max_length=200)
        return response[0]['generated_text']
```

**Pros**: Free, no API keys
**Cons**: Lower quality than GPT, slower

---

### **Option C: Disable AI for Cloud, Keep Local**

**Smart approach**: 

```python
# dashboard.py
import os

class StudentDashboard:
    def __init__(self):
        # ... other code ...
        
        # Only use AI if running locally
        if os.getenv("STREAMLIT_RUNTIME_ENV") != "cloud":
            from ai_assistant_educational import EducationalAIAssistant
            self.ai_assistant = EducationalAIAssistant()
        else:
            self.ai_assistant = None
    
    def run(self):
        # ... other code ...
        
        # Conditionally show AI
        if self.ai_assistant:
            st.header("🤖 AI Assistant")
            self.ai_assistant.render_chat_interface(filtered_df)
        else:
            st.info("🔒 AI Assistant available in downloadable version only (privacy-first)")
            st.markdown("""
            **Want AI-powered insights?**
            1. Download this project from GitHub
            2. Install Ollama locally
            3. Run on your own machine
            
            This keeps your data private and AI costs $0!
            """)
```

**Best of both worlds**: Cloud for visibility, local for AI features

---

## 🎨 Option 3: Hugging Face Spaces (Great for AI Projects!)

### Why Choose This:
- ✅ Free GPU support (for AI models)
- ✅ Great for ML/AI projects
- ✅ Active ML community
- ✅ Easy Docker deployment

### **Deployment Steps:**

#### **1. Create `app.py`** (Hugging Face uses this name):
```python
# app.py (just imports your main)
from main import main

if __name__ == "__main__":
    main()
```

#### **2. Create `Dockerfile`** (optional but recommended):
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### **3. Push to Hugging Face:**

```bash
# Install Hugging Face CLI
pip install huggingface_hub

# Login
huggingface-cli login

# Create new Space
huggingface-cli repo create engage-metrics --type space --space_sdk streamlit

# Push your code
git remote add hf https://huggingface.co/spaces/YOUR-USERNAME/engage-metrics
git push hf main
```

**Your app will be live at**: `https://huggingface.co/spaces/YOUR-USERNAME/engage-metrics`

---

## 🚂 Option 4: Railway (Good Balance)

### Why Railway:
- ✅ Easy deployment from GitHub
- ✅ $5/month free credit
- ✅ Auto-scaling
- ✅ Custom domains
- ✅ Database support

### **Deployment Steps:**

#### **1. Create `Procfile`:**
```
web: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
```

#### **2. Create `runtime.txt`:**
```
python-3.11.5
```

#### **3. Deploy:**

1. Go to **https://railway.app/**
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose `Engage_Metrics`
5. Railway auto-detects and deploys!

**Cost**: Free for hobby projects, ~$5-20/month for production

---

## 🎯 Option 5: Render (Free Tier Available)

### Why Render:
- ✅ Free tier (with limitations)
- ✅ Auto-deploy from GitHub
- ✅ PostgreSQL databases
- ✅ No credit card needed

### **Deployment Steps:**

#### **1. Create `render.yaml`:**
```yaml
services:
  - type: web
    name: engage-metrics
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.5
```

#### **2. Deploy:**

1. Go to **https://render.com/**
2. Click **"New Web Service"**
3. Connect GitHub repo
4. Render auto-deploys!

**Your app**: `https://engage-metrics.onrender.com`

**Limitation**: Free tier sleeps after 15 minutes of inactivity (wakes up in ~30 seconds)

---

## 🐳 Option 6: Docker + DigitalOcean/Linode (Most Control)

### Why This:
- ✅ Full control over server
- ✅ Can run Ollama!
- ✅ Cheapest long-term ($5-10/month)
- ✅ Best performance

### **Complete Setup:**

#### **1. Create Production Dockerfile:**

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Expose Ollama port
EXPOSE 11434

# Start both Ollama and Streamlit
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]
```

#### **2. Create `start.sh`:**

```bash
#!/bin/bash

# Start Ollama in background
ollama serve &

# Wait for Ollama to start
sleep 5

# Pull the AI model
ollama pull gpt-oss:20b

# Start Streamlit
streamlit run main.py --server.port=8501 --server.address=0.0.0.0
```

#### **3. Create `docker-compose.yml`:**

```yaml
version: '3.8'

services:
  engage-metrics:
    build: .
    ports:
      - "8501:8501"
      - "11434:11434"
    volumes:
      - ./student_performance_cleaned.csv:/app/student_performance_cleaned.csv
      - ollama-data:/root/.ollama
    restart: unless-stopped

volumes:
  ollama-data:
```

#### **4. Deploy to DigitalOcean:**

```bash
# 1. Create droplet on DigitalOcean ($6/month)
# Choose: Ubuntu 22.04, Basic plan, $6/month

# 2. SSH into server
ssh root@your-droplet-ip

# 3. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 4. Install Docker Compose
apt install docker-compose -y

# 5. Clone your repo
git clone https://github.com/Irutingab/Engage_Metrics.git
cd Engage_Metrics

# 6. Build and run
docker-compose up -d

# 7. Setup domain (optional)
# Point your domain to droplet IP
# Install Nginx as reverse proxy
apt install nginx -y

# Create Nginx config
cat > /etc/nginx/sites-available/engage-metrics << EOF
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
    }
}
EOF

ln -s /etc/nginx/sites-available/engage-metrics /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# 8. Add HTTPS (free SSL)
apt install certbot python3-certbot-nginx -y
certbot --nginx -d yourdomain.com
```

**Your app is now live at**: `https://yourdomain.com`

**Cost**: $6/month DigitalOcean + $12/year domain = ~$7/month total

---

## 📊 Deployment Comparison Table

| Feature | Streamlit Cloud | Railway | Render | DigitalOcean |
|---------|----------------|---------|--------|--------------|
| **Cost (monthly)** | Free | $5-20 | Free-$25 | $6 |
| **Setup Time** | 10 min | 20 min | 20 min | 1-2 hours |
| **Ollama Support** | ❌ No | ❌ No | ❌ No | ✅ Yes |
| **Custom Domain** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Auto-Deploy** | ✅ Yes | ✅ Yes | ✅ Yes | Manual |
| **Database** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| **Scaling** | Limited | Auto | Auto | Manual |
| **Best For** | MVP/Demo | Small prod | Free tier | Full control |

---

## 🎯 RECOMMENDED STRATEGY

### **Phase 1: MVP (Week 1)**
- ✅ Deploy on **Streamlit Cloud** (free, fast)
- ✅ Disable AI or use OpenAI API
- ✅ Get feedback from users
- ✅ Share with educators/parents

### **Phase 2: Beta (Month 1-2)**
- ✅ Migrate to **Railway** or **Render**
- ✅ Add PostgreSQL database
- ✅ Implement user authentication
- ✅ Use OpenAI API for AI features

### **Phase 3: Production (Month 3+)**
- ✅ Move to **DigitalOcean/AWS**
- ✅ Add Ollama for privacy-focused AI
- ✅ Implement caching and optimization
- ✅ Add monitoring and analytics

---

## 🚀 QUICK START: Deploy in 10 Minutes

**Right now, let's get you live on Streamlit Cloud:**

### **Step 1: Prepare Files**

I'll help you create the necessary deployment files:

1. `.streamlit/config.toml` ← Better UI
2. `.gitignore` ← Don't commit junk
3. Update `requirements.txt` ← Cloud-compatible

### **Step 2: Push to GitHub**

```bash
git add .
git commit -m "Ready for deployment"
git push
```

### **Step 3: Deploy**

1. Visit: https://share.streamlit.io/
2. Connect GitHub
3. Select your repo
4. Click Deploy
5. **Done!** 🎉

---

## 🔒 Security Best Practices

### **Environment Variables** (never commit secrets):

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')
```

### **Streamlit Secrets** (for Streamlit Cloud):

Create `.streamlit/secrets.toml` (DON'T commit this):
```toml
OPENAI_API_KEY = "sk-..."
DATABASE_URL = "postgresql://..."
```

Add to `.gitignore`:
```
.streamlit/secrets.toml
.env
```

Then access in code:
```python
import streamlit as st
api_key = st.secrets["OPENAI_API_KEY"]
```

---

## 📈 Monitoring & Analytics

### **Add Google Analytics:**

```python
# In dashboard.py
def add_analytics():
    st.markdown("""
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-XXXXXXXXXX');
    </script>
    """, unsafe_allow_html=True)
```

### **Add Usage Tracking:**

```python
import streamlit as st
from datetime import datetime

# Track page views
if 'page_views' not in st.session_state:
    st.session_state.page_views = 0
st.session_state.page_views += 1

# Log to file or database
with open('analytics.log', 'a') as f:
    f.write(f"{datetime.now()}, Page View: {st.session_state.page_views}\n")
```

---

## 🎯 NEXT STEPS

**Want me to help you deploy right now?** I can:

1. ✅ Create all deployment configuration files
2. ✅ Modify code for cloud compatibility
3. ✅ Set up GitHub repo properly
4. ✅ Guide you through Streamlit Cloud setup
5. ✅ Add OpenAI integration (if you want AI)

**Just let me know which deployment method you prefer, and I'll set it up for you!**

---

## 📚 Resources

- **Streamlit Cloud Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **Railway Docs**: https://docs.railway.app/
- **Render Docs**: https://render.com/docs
- **DigitalOcean Tutorial**: https://www.digitalocean.com/community/tutorials
- **Docker Tutorial**: https://docs.docker.com/get-started/

---

**Ready to go live? Let's deploy EngageMetrics! 🚀**
