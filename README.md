# 🫁 COPD Assessment & Treatment System

A comprehensive web application for COPD (Chronic Obstructive Pulmonary Disease) assessment, diagnosis, and treatment recommendations based on GOLD 2026 guidelines.

## 📋 Features

### 1. **Patient Information Management**
- Complete patient demographics
- Smoking history and pack-years calculation
- Comorbidity tracking
- Current medication documentation

### 2. **Clinical Assessment**
- **mMRC Dyspnea Scale** - Modified Medical Research Council dyspnea assessment
- **CAT Score** - COPD Assessment Test (8-item questionnaire)
- **Exacerbation History** - Track moderate and severe exacerbations
- **Spirometry Results** - FEV1, FVC, and airflow limitation classification
- **Laboratory Results** - Blood eosinophil counts and other relevant tests
- **Chest X-ray Findings** - Radiographic findings documentation

### 3. **Automated Diagnosis**
- **GOLD ABE Classification** - Automatic assignment to Groups A, B, or E
- **Spirometry-based Staging** - GOLD 1-4 classification based on FEV1
- **Risk Stratification** - Based on symptoms and exacerbation history

### 4. **Treatment Recommendations**
- Evidence-based medication recommendations by GOLD group
- Eosinophil-guided ICS therapy decisions
- Rescue therapy recommendations for all patients
- Special considerations based on comorbidities
- Non-pharmacologic management guidelines

### 5. **Knowledge Base**
- Comprehensive GOLD 2026 guidelines
- Medication reference with dosing information
- Spirometry classification tables
- Treatment algorithms and decision support

### 6. **Data Management**
- Save patient assessments as JSON files
- Download assessment reports
- Session-based data persistence
- Export functionality for records

## 🚀 Quick Start

### Local Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/copd-assessment-system.git
cd copd-assessment-system
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
streamlit run app.py
```

4. **Access the application:**
Open your browser and navigate to `http://localhost:8501`

## 📦 Deployment on Streamlit Cloud

### Step 1: Prepare Your GitHub Repository

1. Create a new repository on GitHub
2. Upload these files:
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - `knowledge_base/` (folder containing COPD guidelines)
   - `.gitignore` (see below)

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository, branch (main), and main file path (app.py)
5. Click "Deploy"

Your app will be live at: `https://yourappname.streamlit.app`

### Step 3: Configure Secrets (Optional)

If you need to store sensitive configuration:

1. Go to your app settings on Streamlit Cloud
2. Navigate to "Secrets"
3. Add your secrets in TOML format:

```toml
[database]
host = "your-host"
port = 5432
```

## 📁 Project Structure

```
copd-assessment-system/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .gitignore                      # Git ignore file
│
├── knowledge_base/                 # COPD treatment guidelines
│   ├── guidelines.json             # Structured treatment protocols
│   └── medications.json            # Medication database
│
├── patient_data/                   # Saved patient assessments
│   └── .gitkeep                    # Keep directory in Git
│
└── docs/                           # Additional documentation
    ├── GOLD_2026_Summary.md        # GOLD guidelines summary
    └── Clinical_Workflow.md        # Clinical usage guide
```

## 🎯 Usage Guide

### For Healthcare Providers

#### Step 1: Patient Information
1. Navigate to "Patient Information" tab
2. Enter patient demographics
3. Document smoking history and comorbidities
4. Save patient information

#### Step 2: Clinical Assessment
1. Navigate to "Clinical Assessment" tab
2. Complete mMRC Dyspnea Scale assessment
3. Administer CAT questionnaire (8 items)
4. Record exacerbation history
5. Enter spirometry results
6. Document blood eosinophil count
7. Record chest X-ray findings
8. Click "Complete Assessment"

#### Step 3: Review Diagnosis & Treatment
1. Navigate to "Diagnosis & Treatment" tab
2. Review automated GOLD group classification
3. Review treatment recommendations
4. Note special considerations (eosinophils, comorbidities)
5. Review rescue therapy options
6. Note non-pharmacologic recommendations
7. Save and download assessment report

#### Step 4: Access Knowledge Base
1. Navigate to "Knowledge Base" tab
2. Review GOLD classification criteria
3. Access medication reference
4. Review spirometry tables
5. Check treatment guidelines

## 🔧 Configuration

### Customization Options

You can customize the application by modifying `app.py`:

#### 1. Add Custom Assessment Tools
```python
# Add custom scoring systems in the load_knowledge_base() function
knowledge_base["custom_scores"] = {
    "BODE_index": {...},
    "6MWT": {...}
}
```

#### 2. Modify Treatment Protocols
```python
# Update treatment recommendations in knowledge_base dictionary
knowledge_base["groups"]["A"]["medications"] = [
    "Your custom medication list"
]
```

#### 3. Add Additional Pages
```python
# Add new navigation options in the sidebar
page = st.radio("Select Section:", 
               ["Patient Information", "Clinical Assessment", 
                "Diagnosis & Treatment", "Knowledge Base", 
                "Your New Page"])
```

## 📊 Data Storage

### Local Storage
Patient data is saved in JSON format in the `patient_data/` directory:

```json
{
    "assessment_date": "2026-02-07T10:30:00",
    "patient_data": {
        "patient_id": "12345",
        "age": 65,
        "mMRC_score": 2,
        "CAT_score": 18,
        ...
    },
    "diagnosis": {
        "GOLD_group": "B",
        "treatment_strategy": "Dual bronchodilator therapy"
    }
}
```

### GitHub Integration
The knowledge base files are stored in the GitHub repository:
- `knowledge_base/guidelines.json` - Treatment protocols
- `knowledge_base/medications.json` - Medication database

## 🔒 Security & Privacy

### Important Considerations

1. **HIPAA Compliance**: This application does not include encryption or access controls suitable for production medical use
2. **PHI Protection**: Do not store actual patient identifiable information without proper security measures
3. **Local Use**: For clinical use, deploy on secure, compliant infrastructure
4. **Educational Purpose**: This application is designed for educational and demonstration purposes

### Recommendations for Production Use

1. Implement user authentication (e.g., OAuth, SAML)
2. Add encryption for data at rest and in transit
3. Implement audit logging
4. Use secure database instead of JSON files
5. Add role-based access controls
6. Conduct security audit and penetration testing
7. Ensure HIPAA compliance if handling real patient data

## 📚 Clinical Guidelines Reference

This application is based on:

- **GOLD 2026 Report** - Global Initiative for Chronic Obstructive Lung Disease
- **UpToDate Guidelines** - Stable COPD: Initial Pharmacologic Management (January 2026)

### Key Updates in GOLD 2026

1. **ABE Classification**: Simplified from ABCD to ABE system
2. **Eosinophil-Guided Therapy**: Enhanced role in ICS decisions
3. **Triple Therapy**: Refined indications for LAMA-LABA-ICS
4. **Exacerbation Risk**: Stronger emphasis on exacerbation history

## 🛠️ Troubleshooting

### Common Issues

**Issue: "ModuleNotFoundError"**
```bash
# Solution: Install all dependencies
pip install -r requirements.txt
```

**Issue: "Permission denied" when saving files**
```bash
# Solution: Create patient_data directory
mkdir patient_data
chmod 755 patient_data
```

**Issue: Application won't start**
```bash
# Solution: Check Python version (requires 3.8+)
python --version

# Update Streamlit
pip install --upgrade streamlit
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Contribution

- Additional assessment tools (BODE index, 6-minute walk test)
- Integration with EHR systems
- Multi-language support
- Advanced analytics and reporting
- Mobile-responsive improvements
- Database backend implementation

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

**FOR EDUCATIONAL AND INFORMATIONAL PURPOSES ONLY**

This application is designed to assist healthcare providers in implementing GOLD guidelines for COPD management. It should not replace clinical judgment or serve as the sole basis for medical decisions. Always verify recommendations against current clinical guidelines and patient-specific factors.

- Not FDA approved
- Not a substitute for professional medical advice
- Not validated for clinical diagnosis or treatment
- Users assume all responsibility for clinical decisions

## 👥 Authors

- **Medical Content**: Based on GOLD 2026 guidelines and UpToDate references
- **Application Development**: [Your Name]
- **Clinical Review**: [Reviewers]

## 📧 Support

For issues, questions, or suggestions:
- Create an issue on GitHub
- Email: support@yourproject.com
- Documentation: [Link to docs]

## 🔄 Version History

### Version 1.0.0 (February 2026)
- Initial release
- GOLD ABE classification system
- Automated treatment recommendations
- Eosinophil-guided therapy
- Knowledge base integration
- Patient data export

### Planned Features (Version 1.1.0)
- [ ] BODE index calculator
- [ ] 6-minute walk test integration
- [ ] Exacerbation prediction model
- [ ] Database backend
- [ ] User authentication
- [ ] Multi-user support
- [ ] Advanced analytics dashboard
- [ ] PDF report generation

## 🌟 Acknowledgments

- Global Initiative for Chronic Obstructive Lung Disease (GOLD)
- UpToDate Clinical Decision Support
- Streamlit development team
- COPD clinical research community

## 📖 Additional Resources

### Clinical Guidelines
- [GOLD 2026 Report](https://goldcopd.org)
- [ATS/ERS Standards](https://www.thoracic.org)
- [NICE Guidelines](https://www.nice.org.uk)

### Patient Education
- [American Lung Association](https://www.lung.org)
- [COPD Foundation](https://www.copdfoundation.org)

### Research
- [ClinicalTrials.gov](https://clinicaltrials.gov)
- [PubMed COPD Research](https://pubmed.ncbi.nlm.nih.gov)

---

**Made with ❤️ for better COPD care**

*Last Updated: February 2026*
