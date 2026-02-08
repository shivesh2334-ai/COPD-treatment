# Quick Deployment Guide

## 🚀 Deploy to Streamlit Cloud in 5 Minutes

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at share.streamlit.io)

### Step 1: Upload to GitHub

1. Create a new repository on GitHub (e.g., `copd-assessment-app`)
2. Upload all files from this folder to your repository:
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - `.gitignore`
   - `knowledge_base/` folder with JSON files
   - `patient_data/` folder with .gitkeep
   - `docs/` folder
   - `.streamlit/` folder with config.toml

### Step 2: Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with your GitHub account
3. Click "New app"
4. Fill in:
   - **Repository:** your-username/copd-assessment-app
   - **Branch:** main (or master)
   - **Main file path:** app.py
5. Click "Deploy!"

Your app will be live in 2-3 minutes at:
`https://your-app-name.streamlit.app`

### Step 3: Test the Application

1. Open your app URL
2. Navigate through all sections:
   - Patient Information
   - Clinical Assessment
   - Diagnosis & Treatment
   - Knowledge Base
3. Complete a test assessment
4. Verify treatment recommendations

## 🏥 Local Testing (Before Deployment)

### Install and Run Locally

```bash
# Clone your repository
git clone https://github.com/your-username/copd-assessment-app.git
cd copd-assessment-app

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Open browser to: http://localhost:8501

## 📦 What's Included

```
copd_assessment_system/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # Full documentation
├── .gitignore                  # Git ignore rules
│
├── .streamlit/
│   └── config.toml            # Streamlit configuration
│
├── knowledge_base/
│   ├── guidelines.json        # GOLD 2026 treatment protocols
│   └── medications.json       # Comprehensive medication database
│
├── patient_data/
│   └── .gitkeep              # Preserves directory in Git
│
└── docs/
    └── Clinical_Workflow.md  # Detailed clinical usage guide
```

## ✅ Post-Deployment Checklist

- [ ] Application loads without errors
- [ ] All four navigation sections work
- [ ] Patient information saves correctly
- [ ] Clinical assessment completes
- [ ] GOLD group classification displays
- [ ] Treatment recommendations generate
- [ ] Knowledge base content accessible
- [ ] Reports can be downloaded

## 🔧 Troubleshooting

### "ModuleNotFoundError"
- Check requirements.txt is in root directory
- Verify all packages are listed

### "Page not found"
- Ensure app.py is in root directory
- Check main file path in Streamlit Cloud settings

### Data not saving
- Patient data saves to session state (not persistent across sessions)
- For production, implement database backend

## 🔒 Security Notes

⚠️ **IMPORTANT:** This demo version:
- Does NOT include authentication
- Stores data in JSON (not secure for PHI)
- Is intended for demonstration/education only

For clinical use:
- Add user authentication
- Implement encrypted database
- Ensure HIPAA compliance
- Conduct security audit

## 📞 Support

Issues? Check:
1. README.md for full documentation
2. docs/Clinical_Workflow.md for usage guide
3. GitHub issues for bug reports

## 🎉 Success!

If you can complete a full patient assessment and see treatment recommendations, your deployment is successful!

---

**Next Steps:**
- Review Clinical_Workflow.md for detailed usage
- Customize knowledge base for your practice
- Consider database integration for production use
- Add your institutional branding

**Made with ❤️ for better COPD care**
