# 🚀 EngageMetrics Deployment Checklist

## ✅ Pre-Deployment Checklist

### Code Preparation
- [ ] All code is committed to Git
- [ ] `requirements.txt` is up to date
- [ ] `.gitignore` excludes sensitive files
- [ ] Data files are included (or have instructions to download)
- [ ] README.md has deployment instructions
- [ ] All features work locally

### Configuration Files
- [ ] `.streamlit/config.toml` created
- [ ] `Procfile` created (for Railway/Heroku)
- [ ] `runtime.txt` created (for Railway/Heroku)
- [ ] `Dockerfile` created (for Docker deployment)
- [ ] `docker-compose.yml` created

### Repository Setup
- [ ] GitHub repository is public (or have permissions set)
- [ ] Repository has good README
- [ ] Repository has LICENSE file
- [ ] Repository has proper description and topics

---

## 🎯 OPTION 1: Streamlit Cloud (Recommended for Start)

### Time: ~10 minutes | Cost: FREE

#### Step 1: Prepare Repository
```bash
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

#### Step 2: Deploy
- [ ] Go to https://share.streamlit.io/
- [ ] Click "New app"
- [ ] Connect GitHub account
- [ ] Select repository: `Irutingab/Engage_Metrics`
- [ ] Branch: `main`
- [ ] Main file: `main.py`
- [ ] Click "Deploy!"

#### Step 3: Configure (Optional)
- [ ] Add custom domain (Settings → Custom domain)
- [ ] Set up secrets if using AI (Settings → Secrets)
- [ ] Monitor app status

#### Notes:
- ⚠️ Ollama AI won't work (local-only)
- ⚠️ Free tier: 1GB RAM, public apps only
- ✅ Auto-deploys on git push
- ✅ Free SSL certificate

**Your app URL**: `https://engage-metrics.streamlit.app/`

---

## 🚂 OPTION 2: Railway

### Time: ~20 minutes | Cost: $5/month free credit

#### Step 1: Setup Railway
- [ ] Go to https://railway.app/
- [ ] Sign up with GitHub
- [ ] Click "New Project"
- [ ] Select "Deploy from GitHub repo"
- [ ] Choose `Engage_Metrics`

#### Step 2: Configure
- [ ] Railway auto-detects configuration
- [ ] Set environment variables if needed
- [ ] Domain is auto-generated

#### Step 3: Monitor
- [ ] Check deployment logs
- [ ] Test the deployed app
- [ ] Set up custom domain (optional)

**Your app URL**: `https://engage-metrics.up.railway.app/`

---

## 🎨 OPTION 3: Hugging Face Spaces

### Time: ~15 minutes | Cost: FREE (with GPU option!)

#### Step 1: Create Space
```bash
# Install HF CLI
pip install huggingface_hub

# Login
huggingface-cli login

# Create Space
huggingface-cli repo create engage-metrics --type space --space_sdk streamlit
```

#### Step 2: Push Code
```bash
git remote add hf https://huggingface.co/spaces/YOUR-USERNAME/engage-metrics
git push hf main
```

#### Step 3: Configure
- [ ] Go to your Space settings
- [ ] Set Space SDK to "Streamlit"
- [ ] Choose hardware (CPU is free)
- [ ] Space auto-builds

**Your app URL**: `https://huggingface.co/spaces/YOUR-USERNAME/engage-metrics`

---

## 🐳 OPTION 4: Docker + DigitalOcean/VPS

### Time: ~1-2 hours | Cost: $6/month

#### Step 1: Create VPS
- [ ] Sign up at DigitalOcean/Linode/Vultr
- [ ] Create Droplet (Ubuntu 22.04, $6/month)
- [ ] Note the IP address

#### Step 2: SSH and Deploy
```bash
# SSH into server
ssh root@YOUR-SERVER-IP

# Download and run deploy script
wget https://raw.githubusercontent.com/Irutingab/Engage_Metrics/main/deploy.sh
chmod +x deploy.sh
./deploy.sh
```

#### Step 3: Configure Domain (Optional)
```bash
# Point domain to server IP
# Then run:
apt install certbot python3-certbot-nginx -y
certbot --nginx -d yourdomain.com
```

**Your app URL**: `http://YOUR-SERVER-IP` or `https://yourdomain.com`

---

## 🔧 Post-Deployment Tasks

### Testing
- [ ] Visit deployed URL
- [ ] Test all features
- [ ] Check visualizations load
- [ ] Test data filtering
- [ ] Test AI assistant (if available)
- [ ] Test on mobile devices
- [ ] Test on different browsers

### Monitoring
- [ ] Set up Google Analytics (optional)
- [ ] Monitor error logs
- [ ] Check performance metrics
- [ ] Monitor uptime

### Documentation
- [ ] Update README with live demo link
- [ ] Add deployment badge
- [ ] Document any known issues
- [ ] Create user guide

### Marketing
- [ ] Share on LinkedIn
- [ ] Post on Twitter/X
- [ ] Share in education communities
- [ ] Add to portfolio
- [ ] Submit to Streamlit gallery

---

## 🐛 Troubleshooting

### App Won't Start
- [ ] Check requirements.txt has all dependencies
- [ ] Check Python version compatibility
- [ ] Review deployment logs
- [ ] Verify data files are included

### Slow Loading
- [ ] Check data file size
- [ ] Add caching decorators
- [ ] Optimize computations
- [ ] Use pagination for large datasets

### AI Not Working
- [ ] Verify API keys are set (if using OpenAI)
- [ ] Check Ollama is running (local only)
- [ ] Review AI assistant error messages
- [ ] Consider disabling AI for cloud deployment

### Data Not Loading
- [ ] Check file paths are relative (not absolute)
- [ ] Verify CSV files are in repository
- [ ] Check file encoding (UTF-8)
- [ ] Review data loading error messages

---

## 🎯 Quick Commands Reference

### Git Commands
```bash
# Commit changes
git add .
git commit -m "Your message"
git push origin main

# Check status
git status

# View history
git log --oneline
```

### Docker Commands
```bash
# Build image
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

### Streamlit Commands
```bash
# Run locally
streamlit run main.py

# Run with specific port
streamlit run main.py --server.port 8501

# Clear cache
streamlit cache clear
```

---

## 📊 Deployment Status

| Platform | Status | URL | Notes |
|----------|--------|-----|-------|
| Streamlit Cloud | ⬜ Not deployed | - | Easy, free |
| Railway | ⬜ Not deployed | - | $5/month |
| Hugging Face | ⬜ Not deployed | - | Free, ML-focused |
| DigitalOcean | ⬜ Not deployed | - | Full control |
| Local | ✅ Running | http://localhost:8501 | Development |

---

## 🎉 Success Criteria

Your deployment is successful when:
- ✅ App loads without errors
- ✅ All visualizations render correctly
- ✅ Data filtering works
- ✅ Downloads function properly
- ✅ Responsive on mobile
- ✅ HTTPS enabled (for production)
- ✅ Under 3-second load time
- ✅ Accessible to target users

---

## 📞 Need Help?

- **Streamlit Docs**: https://docs.streamlit.io/
- **Railway Docs**: https://docs.railway.app/
- **Streamlit Community**: https://discuss.streamlit.io/
- **GitHub Issues**: Create issue in your repo

---

**Ready to deploy? Pick your option and follow the checklist! 🚀**

**Recommended first deployment**: Streamlit Cloud (easiest, free, 10 minutes)
