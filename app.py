import streamlit as st
import pandas as pd
import numpy as np
import joblib


model_wishlists = joblib.load("catboost_model_Wishlists.pkl")
model_bayesian = joblib.load("catboost_model_bayesian_score.pkl")
model_copies = joblib.load("catboost_model_Copies Sold.pkl")
feature_columns = pd.read_csv("feature_columns.csv").squeeze().tolist()


tags = pd.read_csv("tags_list.csv").squeeze().tolist()
genres = pd.read_csv("genres_list.csv").squeeze().tolist()
categories = pd.read_csv("categories_list.csv").squeeze().tolist()
publishers = pd.read_csv("publisher_list.csv").squeeze().tolist()


st.title("🎮 Game Metrics Predictor")
st.markdown("Enter your game's features below to predict **Wishlists**, **Bayesian Score**, and **Copies Sold**.")


st.sidebar.header("🕹️ Input Game Features")
time_to_beat = st.sidebar.number_input("Time to Beat (minutes)", min_value=1.0, value=60.0)
price = st.sidebar.number_input("Price ($)", min_value=0.0, value=19.99)
followers = st.sidebar.number_input("Followers", min_value=0, value=100000)
engagement_ratio = st.sidebar.number_input("Engagement Ratio", min_value=0.0, value=1.5)

selected_tags = st.sidebar.multiselect("Select Tags", tags)
selected_genres = st.sidebar.multiselect("Select Genres", genres)
selected_categories = st.sidebar.multiselect("Select Categories", categories)
selected_publisher = st.sidebar.selectbox("Select Publisher Class", publishers)


input_data = pd.DataFrame(np.zeros((1, len(feature_columns))), columns=feature_columns)
input_data["time_to_beat"] = time_to_beat
input_data["Price"] = price
input_data["Followers"] = followers
input_data["engagement_ratio"] = engagement_ratio


col = f"Publishers Class_{selected_publisher}"
if col in input_data.columns:
    input_data.at[0, col] = 1

for tag in selected_tags:
    col = f"Tags_{tag}"
    if col in input_data.columns:
        input_data.at[0, col] = 1

for genre in selected_genres:
    col = f"genres_{genre}"
    if col in input_data.columns:
        input_data.at[0, col] = 1

for category in selected_categories:
    col = f"categories_{category}"
    if col in input_data.columns:
        input_data.at[0, col] = 1


st.write("Missing columns:", set(model_wishlists.feature_names_) - set(input_data.columns))
st.write("Unexpected extra columns:", set(input_data.columns) - set(model_wishlists.feature_names_))
st.write("Input dtypes:", input_data.dtypes)



if st.button("Predict"):
    
    input_data = input_data[feature_columns]    
    input_data = input_data.astype(float)  

    missing_cols = set(feature_columns) - set(input_data.columns)
    extra_cols = set(input_data.columns) - set(feature_columns)
    st.write("Missing columns:", missing_cols)
    st.write("Unexpected extra columns:", extra_cols)

  
    st.write("Input dtypes:", input_data.dtypes)
    st.write("Final input shape:", input_data.shape)

    
    input_data = input_data.astype(float)

   
    pred_wishlists = model_wishlists.predict(input_data)[0]
    pred_bayesian = model_bayesian.predict(input_data)[0]
    pred_copies = model_copies.predict(input_data)[0]

    st.write("### 🎯 Predicted Results")
    st.metric("Estimated Wishlists", int(pred_wishlists))
    st.metric("Bayesian Score", round(pred_bayesian, 2))
    st.metric("Estimated Copies Sold", int(pred_copies))