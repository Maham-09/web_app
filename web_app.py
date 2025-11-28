import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Initialize session state for data storage
if 'health_data' not in st.session_state:
    st.session_state.health_data = pd.DataFrame(
        columns=['Date', 'Weight', 'Steps', 'Calories', 'Water'],
        dtype=object
    )

# Page configuration
st.set_page_config(page_title="Personal Health Tracker", layout="wide")
st.title("🩺 Personal Health Tracker")
st.markdown("Track your daily health metrics and visualize your progress!")

# Sidebar for navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Data Input", "Dashboard", "BMI Calculator"])

# Function to add new data
def add_health_data(date, weight, steps, calories, water):
    new_data = pd.DataFrame({
        'Date': [pd.to_datetime(date)],
        'Weight': [float(weight)],
        'Steps': [int(steps)],
        'Calories': [int(calories)],
        'Water': [float(water)]
    })
    st.session_state.health_data = pd.concat(
        [st.session_state.health_data, new_data],
        ignore_index=True
    )

# Data Input Page
if page == "Data Input":
    st.header("Enter Your Daily Health Data")
    
    with st.form("health_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            date = st.date_input("Date", value=datetime.now())
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, step=0.1)
        
        with col2:
            steps = st.number_input("Steps Walked", min_value=0, max_value=50000, step=100)
            calories = st.number_input("Calories Burned", min_value=0, max_value=5000, step=10)
        
        water = st.slider("Water Intake (liters)", min_value=0.0, max_value=5.0, step=0.1)
        
        submitted = st.form_submit_button("Save Data")
        
        if submitted:
            add_health_data(date, weight, steps, calories, water)
            st.success("Data saved successfully!")

# Dashboard Page
elif page == "Dashboard":
    st.header("Health Dashboard")
    
    if not st.session_state.health_data.empty:
        st.session_state.health_data['Date'] = pd.to_datetime(st.session_state.health_data['Date'])
        
        tab1, tab2, tab3 = st.tabs(["Weight & BMI", "Activity", "Water Intake"])
        
        with tab1:
            fig_weight = px.line(
                st.session_state.health_data,
                x='Date',
                y='Weight',
                title="Weight Progress",
                markers=True
            )
            st.plotly_chart(fig_weight, use_container_width=True)
            
        with tab2:
            fig_activity = go.Figure()
            fig_activity.add_trace(
                go.Scatter(
                    x=st.session_state.health_data['Date'],
                    y=st.session_state.health_data['Steps'],
                    name='Steps',
                    mode='lines+markers'
                )
            )
            fig_activity.add_trace(
                go.Scatter(
                    x=st.session_state.health_data['Date'],
                    y=st.session_state.health_data['Calories'],
                    name='Calories',
                    mode='lines+markers',
                    yaxis='y2'
                )
            )
            
            fig_activity.update_layout(
                title="Activity Metrics",
                xaxis=dict(title="Date"),
                yaxis=dict(title="Steps"),
                yaxis2=dict(title="Calories", overlaying="y", side="right")
            )
            st.plotly_chart(fig_activity, use_container_width=True)
            
        with tab3:
            fig_water = px.bar(
                st.session_state.health_data,
                x='Date',
                y='Water',
                title="Daily Water Intake"
            )
            st.plotly_chart(fig_water, use_container_width=True)
            
        st.subheader("Health Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Weight",
                      f"{st.session_state.health_data['Weight'].mean():.1f} kg")
        with col2:
            st.metric("Total Steps",
                      f"{int(st.session_state.health_data['Steps'].sum()):,}")
        with col3:
            st.metric("Avg Water Intake",
                      f"{st.session_state.health_data['Water'].mean():.1f} L")
    
    else:
        st.warning("No data available. Please enter data in the Data Input section.")

# BMI Calculator Page
elif page == "BMI Calculator":
    st.header("BMI Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        weight = st.number_input("Enter Weight (kg)", min_value=30.0, max_value=200.0, step=0.1)
        height = st.number_input("Enter Height (cm)", min_value=100.0, max_value=250.0, step=0.1)
    # feet = st.number_input("Height (Feet)", min_value=3, max_value=8, step=1)
    if st.button("Calculate BMI"):
        if height > 0:
            height_m = height / 100 
            bmi = weight / (height_m ** 2)
            
            if bmi < 18.5:
                category = "Underweight"
            elif 18.5 <= bmi < 25:
                category = "Normal"
            elif 25 <= bmi < 30:
                category = "Overweight"
            else:
                category = "Obese"
                
            st.success(f"Your BMI is {bmi:.1f} ({category})")
            
            fig_bmi = go.Figure()
            fig_bmi.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=bmi,
                    title={'text': "BMI"},
                    gauge={
                        'axis': {'range': [10, 40]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [10, 18.5], 'color': "lightblue"},
                            {'range': [18.5, 25], 'color': "lightgreen"},
                            {'range': [25, 30], 'color': "yellow"},
                            {'range': [30, 40], 'color': "red"}
                        ]
                    }
                )
            )
            st.plotly_chart(fig_bmi, use_container_width=True)
        else:
            st.error("Please enter a valid height.")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit • Track your health journey! 💪")