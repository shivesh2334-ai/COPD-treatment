import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="COPD Assessment & Treatment System",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-top: 1rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid #ffc107;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'patient_data' not in st.session_state:
    st.session_state.patient_data = {}
if 'assessment_complete' not in st.session_state:
    st.session_state.assessment_complete = False

# Load COPD knowledge base
@st.cache_data
def load_knowledge_base():
    """Load COPD treatment guidelines from the knowledge base"""
    knowledge_base = {
        "groups": {
            "A": {
                "name": "Less symptomatic, low risk",
                "criteria": {
                    "mMRC": "0-1",
                    "CAT": "<10",
                    "exacerbations": "0"
                },
                "treatment": "Long-acting bronchodilator (LAMA or LABA)",
                "medications": [
                    "Tiotropium (LAMA) 18 mcg once daily",
                    "Salmeterol (LABA) 50 mcg twice daily",
                    "Formoterol (LABA) 20 mcg twice daily",
                    "Indacaterol (LABA) 75-150 mcg once daily"
                ]
            },
            "B": {
                "name": "More symptomatic, low risk",
                "criteria": {
                    "mMRC": "≥2",
                    "CAT": "≥10",
                    "exacerbations": "0"
                },
                "treatment": "Dual bronchodilator therapy (LAMA-LABA)",
                "medications": [
                    "Tiotropium-Olodaterol (2.5/2.5 mcg, 2 inhalations once daily)",
                    "Umeclidinium-Vilanterol (62.5/25 mcg, 1 inhalation daily)",
                    "Glycopyrronium-Indacaterol (50/110 mcg once daily)",
                    "Glycopyrrolate-Formoterol (9/4.8 mcg, 2 inhalations twice daily)",
                    "Aclidinium-Formoterol (400/12 mcg once daily)"
                ]
            },
            "E": {
                "name": "High risk of exacerbations",
                "criteria": {
                    "exacerbations": "≥1 moderate or severe"
                },
                "treatment": "LAMA-LABA (may add ICS based on eosinophils)",
                "medications": [
                    "LAMA-LABA combinations (same as Group B)",
                    "If eosinophils ≥300 cells/μL: Triple therapy (LAMA-LABA-ICS)",
                    "Umeclidinium-Vilanterol-Fluticasone",
                    "Glycopyrronium-Indacaterol-Mometasone",
                    "Tiotropium + Budesonide-Formoterol"
                ]
            }
        },
        "rescue_therapy": [
            "Albuterol (SABA) 90 mcg, 2 puffs as needed",
            "Levalbuterol (SABA) 45 mcg, 2 puffs as needed",
            "Ipratropium-Albuterol (20/100 mcg) 1 inhalation every 4-6 hours as needed"
        ],
        "spirometry_classification": {
            "GOLD 1": {"FEV1": "≥80%", "severity": "Mild"},
            "GOLD 2": {"FEV1": "50-79%", "severity": "Moderate"},
            "GOLD 3": {"FEV1": "30-49%", "severity": "Severe"},
            "GOLD 4": {"FEV1": "<30%", "severity": "Very Severe"}
        }
    }
    return knowledge_base

def calculate_mMRC_score(dyspnea_level):
    """Calculate mMRC dyspnea scale score"""
    mMRC_scale = {
        "No breathlessness except with strenuous exercise": 0,
        "Breathless when hurrying or walking up a slight hill": 1,
        "Walks slower than people of same age due to breathlessness or has to stop for breath when walking at own pace": 2,
        "Stops for breath after walking about 100 meters or after a few minutes": 3,
        "Too breathless to leave house or breathless when dressing": 4
    }
    return mMRC_scale.get(dyspnea_level, 0)

def calculate_CAT_score(responses):
    """Calculate COPD Assessment Test (CAT) score"""
    return sum(responses.values())

def classify_spirometry(fev1_percent):
    """Classify airflow limitation based on FEV1"""
    if fev1_percent >= 80:
        return "GOLD 1", "Mild"
    elif fev1_percent >= 50:
        return "GOLD 2", "Moderate"
    elif fev1_percent >= 30:
        return "GOLD 3", "Severe"
    else:
        return "GOLD 4", "Very Severe"

def determine_GOLD_group(mMRC, CAT, exacerbations_count, hospitalization):
    """Determine GOLD ABE group based on symptoms and exacerbation history"""
    
    # Group E: High risk (≥1 exacerbation)
    if exacerbations_count >= 1 or hospitalization:
        return "E"
    
    # Group B: More symptomatic, low risk
    if mMRC >= 2 or CAT >= 10:
        return "B"
    
    # Group A: Less symptomatic, low risk
    return "A"

def save_patient_data(data):
    """Save patient data to JSON file"""
    data_dir = Path("patient_data")
    data_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"patient_data/patient_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    
    return filename

# Main application
def main():
    st.markdown('<h1 class="main-header">🫁 COPD Assessment & Treatment System</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/lungs.png", width=100)
        st.markdown("### Navigation")
        page = st.radio("Select Section:", 
                       ["Patient Information", "Clinical Assessment", "Diagnosis & Treatment", "Knowledge Base"])
        
        st.markdown("---")
        st.markdown("### About")
        st.info("This system provides COPD assessment and treatment recommendations based on GOLD 2026 guidelines.")
    
    knowledge_base = load_knowledge_base()
    
    # Page 1: Patient Information
    if page == "Patient Information":
        st.markdown('<div class="section-header">Patient Information</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            patient_id = st.text_input("Patient ID/MRN", key="patient_id")
            age = st.number_input("Age", min_value=18, max_value=120, value=60, key="age")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="gender")
            
        with col2:
            smoking_status = st.selectbox("Smoking Status", 
                                         ["Current Smoker", "Former Smoker", "Never Smoked"], 
                                         key="smoking")
            pack_years = st.number_input("Pack Years (if applicable)", 
                                        min_value=0, max_value=200, value=0, key="pack_years")
            bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=25.0, key="bmi")
        
        st.markdown("### Medical History")
        comorbidities = st.multiselect("Comorbidities", 
                                      ["Cardiovascular Disease", "Diabetes", "Asthma", 
                                       "Hypertension", "Gastroesophageal Reflux", "Osteoporosis"],
                                      key="comorbidities")
        
        current_medications = st.text_area("Current Medications", 
                                          placeholder="List current medications...",
                                          key="current_meds")
        
        if st.button("Save Patient Information", key="save_patient_info"):
            st.session_state.patient_data.update({
                "patient_id": patient_id,
                "age": age,
                "gender": gender,
                "smoking_status": smoking_status,
                "pack_years": pack_years,
                "bmi": bmi,
                "comorbidities": comorbidities,
                "current_medications": current_medications
            })
            st.success("✅ Patient information saved!")
    
    # Page 2: Clinical Assessment
    elif page == "Clinical Assessment":
        st.markdown('<div class="section-header">Clinical Assessment</div>', unsafe_allow_html=True)
        
        # Symptom Assessment
        st.markdown("### 1. Dyspnea Assessment (mMRC Scale)")
        dyspnea_level = st.selectbox(
            "Select the statement that best describes breathlessness:",
            [
                "No breathlessness except with strenuous exercise",
                "Breathless when hurrying or walking up a slight hill",
                "Walks slower than people of same age due to breathlessness or has to stop for breath when walking at own pace",
                "Stops for breath after walking about 100 meters or after a few minutes",
                "Too breathless to leave house or breathless when dressing"
            ],
            key="dyspnea"
        )
        mMRC_score = calculate_mMRC_score(dyspnea_level)
        st.info(f"**mMRC Score: {mMRC_score}**")
        
        # CAT Score
        st.markdown("### 2. COPD Assessment Test (CAT)")
        st.write("Rate each item from 0 (best) to 5 (worst):")
        
        col1, col2 = st.columns(2)
        
        cat_responses = {}
        with col1:
            cat_responses['cough'] = st.slider("Cough frequency", 0, 5, 0, 
                                              help="0=Never cough, 5=Cough all the time")
            cat_responses['phlegm'] = st.slider("Phlegm in chest", 0, 5, 0,
                                               help="0=No phlegm, 5=Chest completely full")
            cat_responses['chest_tight'] = st.slider("Chest tightness", 0, 5, 0,
                                                    help="0=Not tight, 5=Very tight")
            cat_responses['breathless'] = st.slider("Breathlessness going up hills/stairs", 0, 5, 0,
                                                   help="0=Not breathless, 5=Very breathless")
        
        with col2:
            cat_responses['activities'] = st.slider("Limited doing activities at home", 0, 5, 0,
                                                   help="0=Not limited, 5=Very limited")
            cat_responses['confidence'] = st.slider("Confidence leaving home", 0, 5, 0,
                                                   help="0=Very confident, 5=Not confident at all")
            cat_responses['sleep'] = st.slider("Sleep quality", 0, 5, 0,
                                              help="0=Sleep soundly, 5=Don't sleep soundly")
            cat_responses['energy'] = st.slider("Energy level", 0, 5, 0,
                                               help="0=Lots of energy, 5=No energy at all")
        
        CAT_score = calculate_CAT_score(cat_responses)
        st.info(f"**CAT Score: {CAT_score}** (0-9: Low, 10-20: Medium, 21-30: High, 31-40: Very High)")
        
        # Exacerbation History
        st.markdown("### 3. Exacerbation History")
        col1, col2 = st.columns(2)
        
        with col1:
            exacerbations = st.number_input(
                "Number of exacerbations in past year requiring antibiotics/steroids:",
                min_value=0, max_value=20, value=0, key="exacerbations"
            )
        
        with col2:
            hospitalization = st.checkbox("Any hospitalization for COPD exacerbation in past year?",
                                        key="hospitalization")
        
        # Spirometry
        st.markdown("### 4. Spirometry Results")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fev1_actual = st.number_input("FEV1 (Liters)", min_value=0.0, max_value=10.0, 
                                         value=2.0, step=0.1, key="fev1_actual")
        with col2:
            fev1_predicted = st.number_input("FEV1 Predicted (Liters)", min_value=0.0, max_value=10.0,
                                            value=3.0, step=0.1, key="fev1_predicted")
        with col3:
            fev1_fvc = st.number_input("FEV1/FVC Ratio", min_value=0.0, max_value=1.0,
                                      value=0.65, step=0.01, key="fev1_fvc")
        
        if fev1_predicted > 0:
            fev1_percent = (fev1_actual / fev1_predicted) * 100
            gold_stage, severity = classify_spirometry(fev1_percent)
            st.info(f"**FEV1: {fev1_percent:.1f}% predicted | {gold_stage} ({severity})**")
        
        # Blood Tests
        st.markdown("### 5. Laboratory Results")
        col1, col2 = st.columns(2)
        
        with col1:
            eosinophils = st.number_input("Blood Eosinophils (cells/μL)", 
                                         min_value=0, max_value=2000, value=150, key="eosinophils")
            st.caption("Reference: <100 (low), 100-300 (intermediate), ≥300 (high)")
        
        with col2:
            other_labs = st.text_area("Other Lab Results", 
                                     placeholder="Hemoglobin, Alpha-1 antitrypsin, etc.",
                                     key="other_labs")
        
        # Chest X-ray Findings
        st.markdown("### 6. Chest X-ray Findings")
        cxr_findings = st.multiselect("Select CXR Findings:",
                                     ["Hyperinflation", "Flattened diaphragm", "Bullae",
                                      "Increased retrosternal airspace", "Narrow cardiac silhouette",
                                      "Bronchial wall thickening", "No significant findings"],
                                     key="cxr_findings")
        
        cxr_notes = st.text_area("Additional CXR Notes", key="cxr_notes")
        
        if st.button("Complete Assessment", key="complete_assessment"):
            st.session_state.patient_data.update({
                "mMRC_score": mMRC_score,
                "CAT_score": CAT_score,
                "exacerbations": exacerbations,
                "hospitalization": hospitalization,
                "fev1_percent": fev1_percent if fev1_predicted > 0 else None,
                "fev1_fvc": fev1_fvc,
                "gold_stage": gold_stage if fev1_predicted > 0 else None,
                "eosinophils": eosinophils,
                "cxr_findings": cxr_findings,
                "cxr_notes": cxr_notes,
                "other_labs": other_labs
            })
            st.session_state.assessment_complete = True
            st.success("✅ Clinical assessment completed! Go to 'Diagnosis & Treatment' for recommendations.")
    
    # Page 3: Diagnosis & Treatment
    elif page == "Diagnosis & Treatment":
        st.markdown('<div class="section-header">Diagnosis & Treatment Recommendations</div>', unsafe_allow_html=True)
        
        if not st.session_state.assessment_complete:
            st.warning("⚠️ Please complete the Clinical Assessment first.")
            return
        
        data = st.session_state.patient_data
        
        # Determine GOLD Group
        GOLD_group = determine_GOLD_group(
            data.get('mMRC_score', 0),
            data.get('CAT_score', 0),
            data.get('exacerbations', 0),
            data.get('hospitalization', False)
        )
        
        group_info = knowledge_base['groups'][GOLD_group]
        
        # Display Diagnosis
        st.markdown("### Diagnosis Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("GOLD Group", GOLD_group)
            st.caption(group_info['name'])
        
        with col2:
            if data.get('gold_stage'):
                st.metric("Airflow Limitation", data['gold_stage'])
                st.caption(f"FEV1: {data.get('fev1_percent', 0):.1f}%")
        
        with col3:
            st.metric("Symptom Burden", 
                     "High" if data.get('CAT_score', 0) >= 10 else "Low")
            st.caption(f"CAT: {data.get('CAT_score', 0)}, mMRC: {data.get('mMRC_score', 0)}")
        
        # Treatment Recommendations
        st.markdown("### Treatment Recommendations")
        
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown(f"**Primary Treatment Strategy:** {group_info['treatment']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Medication Options
        st.markdown("#### Recommended Medications")
        
        for i, med in enumerate(group_info['medications'], 1):
            st.write(f"{i}. {med}")
        
        # Special Considerations
        st.markdown("#### Special Considerations")
        
        considerations = []
        
        # Eosinophil-based recommendations
        if GOLD_group == "E":
            eosinophils = data.get('eosinophils', 0)
            if eosinophils >= 300:
                considerations.append(
                    "🔴 **High Eosinophils (≥300 cells/μL):** Consider triple therapy (LAMA-LABA-ICS) upfront"
                )
            elif eosinophils < 100:
                considerations.append(
                    "🟢 **Low Eosinophils (<100 cells/μL):** Avoid ICS if possible due to increased pneumonia risk"
                )
            else:
                considerations.append(
                    "🟡 **Intermediate Eosinophils (100-300 cells/μL):** ICS may provide moderate benefit"
                )
        
        # Comorbidity considerations
        comorbidities = data.get('comorbidities', [])
        if 'Asthma' in comorbidities:
            considerations.append(
                "🔵 **Asthma-COPD Overlap:** Consider adding ICS to bronchodilator therapy"
            )
        
        if 'Cardiovascular Disease' in comorbidities:
            considerations.append(
                "⚠️ **Cardiovascular Disease:** Monitor for cardiovascular effects of bronchodilators"
            )
        
        if data.get('hospitalization'):
            considerations.append(
                "🔴 **Recent Hospitalization:** Consider triple therapy (LAMA-LABA-ICS) due to high risk"
            )
        
        for consideration in considerations:
            st.markdown(f"- {consideration}")
        
        # Rescue Therapy
        st.markdown("#### Rescue Therapy (All Patients)")
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.write("**All patients should have a short-acting bronchodilator for symptom relief:**")
        for rescue in knowledge_base['rescue_therapy']:
            st.write(f"- {rescue}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Non-Pharmacologic Management
        st.markdown("### Non-Pharmacologic Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Essential Interventions")
            st.write("✅ Smoking cessation (if applicable)")
            st.write("✅ Pulmonary rehabilitation")
            st.write("✅ Influenza vaccination (annual)")
            st.write("✅ Pneumococcal vaccination")
            st.write("✅ COVID-19 vaccination")
        
        with col2:
            st.markdown("#### Additional Recommendations")
            st.write("• Regular exercise as tolerated")
            st.write("• Nutritional optimization")
            st.write("• Oxygen therapy if hypoxemic")
            st.write("• Education on inhaler technique")
            st.write("• Self-management education")
        
        # Follow-up Plan
        st.markdown("### Follow-up Plan")
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.write("**Recommended Follow-up:**")
        st.write("- Initial follow-up: 2-4 weeks after starting new therapy")
        st.write("- Routine follow-up: Every 3-6 months for stable patients")
        st.write("- Monitor for: Symptom control, exacerbation frequency, side effects")
        st.write("- Adjust therapy based on response (see GOLD guidelines)")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Save Report
        if st.button("💾 Save Assessment Report", key="save_report"):
            report_data = {
                "assessment_date": datetime.now().isoformat(),
                "patient_data": data,
                "diagnosis": {
                    "GOLD_group": GOLD_group,
                    "group_description": group_info['name'],
                    "treatment_strategy": group_info['treatment']
                },
                "recommendations": {
                    "medications": group_info['medications'],
                    "rescue_therapy": knowledge_base['rescue_therapy'],
                    "special_considerations": considerations
                }
            }
            
            filename = save_patient_data(report_data)
            st.success(f"✅ Report saved: {filename}")
            
            # Offer download
            st.download_button(
                label="📥 Download Report (JSON)",
                data=json.dumps(report_data, indent=4),
                file_name=f"COPD_Assessment_{data.get('patient_id', 'unknown')}_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
    
    # Page 4: Knowledge Base
    elif page == "Knowledge Base":
        st.markdown('<div class="section-header">COPD Knowledge Base (GOLD 2026)</div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["GOLD Groups", "Medications", "Spirometry", "Guidelines"])
        
        with tab1:
            st.markdown("### GOLD ABE Classification System")
            
            for group_key, group_data in knowledge_base['groups'].items():
                with st.expander(f"**Group {group_key}: {group_data['name']}**", expanded=True):
                    st.write("**Criteria:**")
                    for criterion, value in group_data['criteria'].items():
                        st.write(f"- {criterion}: {value}")
                    
                    st.write(f"\n**Treatment:** {group_data['treatment']}")
                    
                    st.write("\n**Medication Options:**")
                    for med in group_data['medications']:
                        st.write(f"- {med}")
        
        with tab2:
            st.markdown("### Medication Classes")
            
            st.markdown("#### Long-Acting Beta-Agonists (LABA)")
            laba_data = {
                "Medication": ["Salmeterol", "Formoterol", "Indacaterol", "Olodaterol", "Vilanterol"],
                "Dosing": ["50 mcg BID", "20 mcg BID", "75-150 mcg QD", "2.5 mcg (2 inh) QD", "25 mcg QD"],
                "Onset": ["Slow (120 min)", "Rapid (3 min)", "Rapid", "Rapid", "Intermediate (15 min)"],
                "Duration": ["12 hours", "12 hours", "24 hours", "24 hours", "24 hours"]
            }
            st.table(pd.DataFrame(laba_data))
            
            st.markdown("#### Long-Acting Muscarinic Antagonists (LAMA)")
            lama_data = {
                "Medication": ["Tiotropium", "Aclidinium", "Umeclidinium", "Glycopyrrolate"],
                "Dosing": ["18 mcg QD or 2.5 mcg (2 inh) QD", "400 mcg BID", "62.5 mcg QD", "50 mcg QD"],
                "Device": ["DPI or SMI", "DPI", "DPI", "DPI"],
                "Features": ["Most studied", "Low bioavailability", "Once daily", "Once or twice daily"]
            }
            st.table(pd.DataFrame(lama_data))
            
            st.markdown("#### Combination Therapies")
            st.write("**LAMA-LABA Combinations:**")
            st.write("- Tiotropium-Olodaterol")
            st.write("- Umeclidinium-Vilanterol")
            st.write("- Glycopyrronium-Indacaterol")
            st.write("- Glycopyrrolate-Formoterol")
            st.write("- Aclidinium-Formoterol")
            
            st.write("\n**Triple Therapy (LAMA-LABA-ICS):**")
            st.write("- Reserved for patients with frequent exacerbations and/or high eosinophils")
            st.write("- Various combinations available")
        
        with tab3:
            st.markdown("### Spirometry Classification")
            
            spirometry_df = pd.DataFrame([
                {"GOLD Stage": "GOLD 1", "Severity": "Mild", "FEV1 % Predicted": "≥80%"},
                {"GOLD Stage": "GOLD 2", "Severity": "Moderate", "FEV1 % Predicted": "50-79%"},
                {"GOLD Stage": "GOLD 3", "Severity": "Severe", "FEV1 % Predicted": "30-49%"},
                {"GOLD Stage": "GOLD 4", "Severity": "Very Severe", "FEV1 % Predicted": "<30%"}
            ])
            
            st.table(spirometry_df)
            
            st.info("**Note:** FEV1/FVC <0.70 confirms airflow obstruction (COPD diagnosis)")
        
        with tab4:
            st.markdown("### Key Guidelines Summary")
            
            st.markdown("#### Assessment Tools")
            st.write("- **mMRC Dyspnea Scale:** 0-4 (≥2 indicates more symptomatic)")
            st.write("- **CAT Score:** 0-40 (<10 low impact, ≥10 high impact)")
            st.write("- **Exacerbation History:** ≥1 in past year indicates high risk")
            
            st.markdown("#### Treatment Principles")
            st.write("1. All patients receive rescue bronchodilator (SABA ± SAMA)")
            st.write("2. Regular therapy based on GOLD group (A, B, or E)")
            st.write("3. Consider eosinophils for ICS decisions in Group E")
            st.write("4. Prefer single-inhaler combinations for adherence")
            st.write("5. Always combine with non-pharmacologic management")
            
            st.markdown("#### Eosinophil-Guided Therapy")
            eosinophil_df = pd.DataFrame([
                {"Eosinophil Count": "<100 cells/μL", "ICS Benefit": "Minimal", "Risk": "Higher pneumonia risk"},
                {"Eosinophil Count": "100-300 cells/μL", "ICS Benefit": "Moderate", "Risk": "Intermediate"},
                {"Eosinophil Count": "≥300 cells/μL", "ICS Benefit": "High", "Risk": "Consider triple therapy"}
            ])
            st.table(eosinophil_df)
            
            st.markdown("#### Red Flags")
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.write("**Refer for specialist evaluation if:**")
            st.write("- Diagnostic uncertainty")
            st.write("- Severe COPD (GOLD 3-4)")
            st.write("- Frequent exacerbations despite optimal therapy")
            st.write("- Rapid decline in lung function")
            st.write("- Hemoptysis")
            st.write("- Consideration for oxygen therapy or surgical interventions")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("#### References")
            st.write("- Global Initiative for Chronic Obstructive Lung Disease (GOLD) 2026 Report")
            st.write("- UpToDate: Stable COPD - Initial Pharmacologic Management")
            st.write("- Latest update: January 2026")

if __name__ == "__main__":
    main()
