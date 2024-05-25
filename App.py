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
    
    # Perform any necessary data preprocessing (e.g., encoding categorical variables)
    # Assuming all categorical variables need to be encoded
    input_data_encoded = pd.get_dummies(input_data)
    
    # Ensure the input data matches the model's expected features
    model_features = model.feature_names_in_
    for feature in model_features:
        if feature not in input_data_encoded.columns:
            input_data_encoded[feature] = 0  # Add missing features with default value 0

    input_data_encoded = input_data_encoded[model_features]

    return input_data_encoded

# Create the web interface
def main():
    st.title('Space Prediction Model')

    SUBCOUNTY = st.selectbox('SUBCOUNTY',  ['KIHARU', 'GATANGA', 'KANDARA', 'KANGEMA', 'KIGUMO', 'MURANG’A SOUTH', 'MATHIOYA'])
    YEAR_2011 = st.number_input('YEAR2011', min_value=0, max_value=82450)
    YEAR_2012 = st.number_input('YEAR2012', min_value=0, max_value=82450)
    YEAR_2013 = st.number_input('YEAR2013', min_value=0, max_value=82450)
    AGENCY = st.selectbox('AGENCY', ['County Government', 'CBO'])
    LEVEL = st.selectbox('LEVEL', ['Dispensary', 'Health Centre', 'Sub-district'])
    FUNCTIONALITY2 = st.selectbox('FUNCTIONALITY2', ['Fair', 'Below', 'Average', 'Good'])
    STATUS3 = st.selectbox('STATUS3', ['Fair', 'Good'])
    Land_elevation = st.selectbox('Land_elevation', ['1<1200 meters asl', '<1200 meters asl'])
    Capacity_coded = st.selectbox('Capacity_coded', ['Minimum capacity', 'No capacity', 'Sufficient installed capacity'])

    if st.button('Predict'):
        input_data = preprocess_input(SUBCOUNTY, YEAR_2011, YEAR_2012, YEAR_2013, AGENCY, LEVEL, FUNCTIONALITY2,
                                      STATUS3, Land_elevation, Capacity_coded)
        try:
            prediction = model.predict(input_data)[0]
            if prediction == 0:
                st.write('Prediction: No Space Available')
            else:
                st.write('Prediction: Space Available')
        except Exception as e:
            st.write(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
