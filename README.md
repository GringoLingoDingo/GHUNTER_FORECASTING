markdown# Game Success Analytics: Predicting Performance Metrics for Steam Games

## Project Overview
This machine learning project predicts key performance metrics for Steam games using CatBoost regression models. By analyzing a dataset of over 98,000 games and identifying patterns in successful titles, the project provides valuable insights for game developers and publishers to forecast commercial performance.

## Key Metrics Predicted
- **Copies Sold**: Number of game copies purchased
- **Wishlists**: Number of users who added the game to their wishlists
- **Bayesian Score**: Weighted review score metric

## Dataset
- Original dataset: 98,350 Steam games
- Filtered dataset: 7,029 games with complete engagement metrics
- Features include: game tags, genres, categories, publisher class, and engagement metrics

## Key Findings
- **Dataset Selection Bias**: The filtered dataset represents only the top 7.15% of market performers
- The median game in our filtered dataset sells 84.6x more copies than the median game in the overall market
- Even the lowest-performing games in our dataset significantly outperform average market titles

## Model Performance
| Target Variable | R² Score | MAE     |
|-----------------|----------|---------|
| Copies Sold     | 0.83     | 171,311 |
| Wishlists       | 0.75     | 34,115  |
| Bayesian Score  | 0.39     | 6.59    |

## Most Important Features
- Followers
- time_to_beat
- engagement_ratio
- Publisher Class (AAA, Indie)
- Game tags (Open World, Co-op)

## Technical Approach
- Data preprocessing with feature engineering and one-hot encoding
- CatBoost implementation for handling categorical features
- Log transformation for skewed target variables
- Cross-validation with 5 folds and hyperparameter tuning

## Limitations & Future Improvements
- Models trained exclusively on successful games (top 7% of market)
- Limited applicability to newer or less established games
- **Proposed Solution**: Two-stage model combining classification and regression:
 1. Predict if a game will be in top ~7% of market (classification)
 2. For "successful" games, predict precise metrics (regression)

## Future Development
- NLP analysis of user reviews for keyword extraction
- Time-series analysis to track growth patterns
- Integration with social media APIs (Twitch, YouTube)
- Implementation of recurrent neural networks (RNNs)

## Repository Structure
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
