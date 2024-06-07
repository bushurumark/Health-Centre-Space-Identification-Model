#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip install streamlit


# In[2]:


import streamlit as st
import pandas as pd
import joblib


# In[3]:


# Load the trained model
model = joblib.load("model.pkl")


# In[4]:


# Define function to preprocess input data
def preprocess_input(SUBCOUNTY, YEAR_2011, YEAR_2012, YEAR_2013, AGENCY,
                     LEVEL, FUNCTIONALITY2, STATUS3, Land_elevation,
                     Capacity_coded):
    # Create a DataFrame with the input data
    input_data = pd.DataFrame({
        'SUBCOUNTY': [SUBCOUNTY],
        'YEAR2011': [YEAR_2011],
        'YEAR2012': [YEAR_2012],  
        'YEAR2013': [YEAR_2013],
        'AGENCY': [AGENCY],
        'LEVEL': [LEVEL],
        'FUNCTIONALITY2': [FUNCTIONALITY2],
        'STATUS3': [STATUS3],
        'Land_elevation': [Land_elevation],
        'Capacity_coded': [Capacity_coded]
    })
    
    # Encoding of all categorical variables 
    input_data_encoded = pd.get_dummies(input_data)
    
    # Ensure the input data matches the model's expected features
    model_features = model.feature_names_in_
    for feature in model_features:
        if feature not in input_data_encoded.columns:
            input_data_encoded[feature] = 0  # Add missing features with default value 0

    input_data_encoded = input_data_encoded[model_features]

    return input_data_encoded

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: purple;
    }
    .title {
        color: green;
        text-align: center;
        font-size: 40px;
    }
    .widget-label {
        color: #ff6347;
        font-weight: bold;
    }
    .prediction-result {
        color: red;
        font-size: 30px;
        text-align: center;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Create the web interface
def main():
    st.markdown('<div class="title">Space Prediction Model</div>', unsafe_allow_html=True)

    SUBCOUNTY = st.selectbox('SUB-COUNTY',  ['KIHARU', 'GATANGA', 'KANDARA', 'KANGEMA', 'KIGUMO', 'MURANG’A SOUTH', 'MATHIOYA'])
    YEAR_2011 = st.number_input('NUMBER OF PATIENTS IN THE YEAR 2011', min_value=0, max_value=82450)
    YEAR_2012 = st.number_input('NUMBER OF PATIENTS IN THE YEAR 2012', min_value=0, max_value=82450)
    YEAR_2013 = st.number_input('NUMBER OF PATIENTS IN THE YEAR 2013', min_value=0, max_value=82450)
    AGENCY = st.selectbox('AGENCY', ['County Government', 'CBO'])
    LEVEL = st.selectbox('LEVEL', ['Dispensary', 'Health Centre', 'Sub-district'])
    FUNCTIONALITY2 = st.selectbox('FUNCTIONALITY2', ['Fair', 'Below', 'Average', 'Good'])
    STATUS3 = st.selectbox('STATUS', ['Fair', 'Good'])
    Land_elevation = st.selectbox('LAND ELEVATION', ['1<1200 meters asl', '<1200 meters asl'])
    Capacity_coded = st.selectbox('CAPACITY', ['Minimum capacity', 'No capacity', 'Sufficient installed capacity'])

    if st.button('Predict'):
        input_data = preprocess_input(SUBCOUNTY, YEAR_2011, YEAR_2012, YEAR_2013, AGENCY, LEVEL, FUNCTIONALITY2,
                                      STATUS3, Land_elevation, Capacity_coded)
        try:
            prediction = model.predict(input_data)[0]
            if prediction == 0:
                st.markdown('<div class="prediction-result">Prediction: No Space Available</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="prediction-result">Prediction: Space Available</div>', unsafe_allow_html=True)
        except Exception as e:
            st.write(f"An error occurred: {e}")

if __name__ == '__main__':
    main()

