# 🎮 GHUNTER FORECASTING – Game Metrics Prediction App

This project uses machine learning to predict important commercial game metrics — including **Wishlists**, **Bayesian Score**, and **Copies Sold** — based on structured Steam metadata. It features a trained CatBoost model and a Streamlit app for user-friendly predictions.

## 🚀 Project Overview

Using Steam data and a custom-labeled dataset of game attributes (tags, genres, categories, pricing, etc.), this project builds CatBoost regression models to forecast three key indicators:

- 🎯 **Wishlists**: Early player interest
- 📈 **Bayesian Score**: Smoothed sentiment measure from reviews
- 🛒 **Copies Sold**: Estimated sales volume

## 📁 Project Structure

```bash
.
├── app.py                      # Streamlit app interface
├── Proyecto_ML.csv            # Training dataset
├── catboost_model_Wishlists.pkl
├── catboost_model_bayesian_score.pkl
├── catboost_model_Copies Sold.pkl
├── feature_columns.csv        # Feature columns used in the models
├── tag_list.csv
├── genre_list.csv
├── category_list.csv
├── publisher_list.csv
└── README.md
