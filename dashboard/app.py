"""
Streamlit Dashboard for Churn Prediction
"""
import streamlit as st
import requests
import json
import pandas as pd
import plotly.graph_objects as go

# API URL
API_URL = "https://churn-prediction-api-r70r.onrender.com"

# Page config
st.set_page_config(
    page_title="Churn Prediction System",
    page_icon="🎯",
    layout="wide"
)

# Title
st.title("🎯 Customer Churn Prediction System")
st.markdown("### Predict customer churn risk with ML")

# Sidebar
st.sidebar.header("📊 About")
st.sidebar.info(
    """
    This system uses machine learning to predict 
    customer churn with **84% accuracy**.
    
    **How it works:**
    1. Enter customer information
    2. Click 'Predict'
    3. Get instant churn risk assessment
    """
)

# Main form
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Customer Information")
    
    gender = st.selectbox("Gender", ["Male", "Female"])
    senior_citizen = st.selectbox("Senior Citizen", [0, 1], 
                                  format_func=lambda x: "Yes" if x else "No")
    partner = st.selectbox("Has Partner", ["Yes", "No"])
    dependents = st.selectbox("Has Dependents", ["Yes", "No"])
    
    st.subheader("📞 Services")
    phone_service = st.selectbox("Phone Service", ["Yes", "No"])
    multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
    internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    online_security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
    online_backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])

with col2:
    st.subheader("📺 Additional Services")
    device_protection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
    tech_support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
    streaming_tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
    streaming_movies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])
    
    st.subheader("💳 Account Information")
    contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
    payment_method = st.selectbox(
        "Payment Method", 
        ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
    )
    tenure = st.slider("Tenure (months)", 0, 72, 12)
    monthly_charges = st.number_input("Monthly Charges ($)", 0.0, 200.0, 50.0)
    total_charges = st.number_input("Total Charges ($)", 0.0, 10000.0, 600.0)

# Predict button
if st.button("🔮 Predict Churn Risk", type="primary"):
    # Prepare data
    customer_data = {
        "gender": gender,
        "SeniorCitizen": senior_citizen,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": int(tenure),
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method,
        "MonthlyCharges": float(monthly_charges),
        "TotalCharges": float(total_charges)
    }
    
    # Make prediction
    with st.spinner("Analyzing customer..."):
        try:
            response = requests.post(
                f"{API_URL}/predict",
                json=customer_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Display results
                st.success("✅ Prediction Complete!")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Churn Prediction",
                        "Will Churn" if result['churn_prediction'] == 1 else "Will Stay",
                        delta=None
                    )
                
                with col2:
                    st.metric(
                        "Churn Probability",
                        f"{result['churn_probability']*100:.1f}%",
                        delta=None
                    )
                
                with col3:
                    risk_color = {
                        "low": "🟢",
                        "medium": "🟡",
                        "high": "🟠",
                        "very_high": "🔴"
                    }
                    st.metric(
                        "Risk Level",
                        f"{risk_color.get(result['risk_level'], '')} {result['risk_level'].upper()}",
                        delta=None
                    )
                
                # Gauge chart for probability
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=result['churn_probability'] * 100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Churn Risk"},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 30], 'color': "lightgreen"},
                            {'range': [30, 60], 'color': "yellow"},
                            {'range': [60, 80], 'color': "orange"},
                            {'range': [80, 100], 'color': "red"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 80
                        }
                    }
                ))
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Recommendations
                st.subheader("💡 Recommendations")
                if result['churn_prediction'] == 1:
                    st.warning("""
                    **High Churn Risk Detected!**
                    
                    Recommended Actions:
                    - 🎁 Offer retention discount or upgrade
                    - 📞 Schedule customer success call
                    - 📧 Send personalized retention email
                    - 🎯 Provide additional services trial
                    """)
                else:
                    st.info("""
                    **Low Churn Risk - Customer Likely to Stay**
                    
                    Recommendations:
                    - ⭐ Consider for upsell opportunities
                    - 📊 Monitor for any changes in behavior
                    - 💬 Request feedback/testimonial
                    """)
                
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        
        except Exception as e:
            st.error(f"Error connecting to API: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Built with ❤️ using FastAPI, MLflow, and Streamlit</p>
        <p>Model Accuracy: 84% ROC-AUC | API Status: 
        <a href='https://churn-prediction-api-r70r.onrender.com/health'>Check Health</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
