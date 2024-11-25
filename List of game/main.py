import pandas as pd
import numpy as np


# Create sample game data
def create_sample_game_data():
    """Create a sample DataFrame with game data"""
    data = {
        'game_title': ['The Witcher 3', 'Red Dead Redemption 2', 'God of War', 'Cyberpunk 2077',
                       'GTA V', 'Elden Ring', 'Horizon Zero Dawn', 'Spider-Man'],
        'genre': ['RPG', 'Action-Adventure', 'Action', 'RPG',
                  'Action-Adventure', 'RPG', 'Action-RPG', 'Action-Adventure'],
        'release_year': [2015, 2018, 2018, 2020, 2013, 2022, 2017, 2018],
        'rating': [9.8, 9.7, 9.5, 7.8, 9.6, 9.4, 9.2, 9.3],
        'sales_millions': [40.2, 50.5, 23.0, 18.2, 170.0, 20.5, 20.0, 33.2],
        'playtime_hours': [100, 80, 30, 60, 50, 70, 40, 25],
        'price': [39.99, 59.99, 49.99, 59.99, 29.99, 59.99, 49.99, 39.99]
    }
    return pd.DataFrame(data)


def analyze_games(df):
    """Perform various analyses on the game dataset"""

    # Basic statistics
    stats = {
        'total_games': len(df),
        'avg_rating': df['rating'].mean(),
        'avg_price': df['price'].mean(),
        'total_sales': df['sales_millions'].sum(),
        'avg_playtime': df['playtime_hours'].mean()
    }

    # Genre analysis
    genre_stats = df.groupby('genre').agg({
        'game_title': 'count',
        'rating': 'mean',
        'sales_millions': 'sum',
        'price': 'mean'
    }).round(2)
    genre_stats.columns = ['game_count', 'avg_rating', 'total_sales_millions', 'avg_price']

    # Year analysis
    year_stats = df.groupby('release_year').agg({
        'game_title': 'count',
        'sales_millions': 'sum'
    }).round(2)
    year_stats.columns = ['games_released', 'total_sales_millions']

    # Top games by different metrics
    top_rated = df.nlargest(3, 'rating')[['game_title', 'rating', 'genre']]
    top_selling = df.nlargest(3, 'sales_millions')[['game_title', 'sales_millions', 'genre']]
    best_value = df.assign(hours_per_dollar=df['playtime_hours'] / df['price']) \
        .nlargest(3, 'hours_per_dollar')[['game_title', 'hours_per_dollar', 'price']]

    return {
        'basic_stats': stats,
        'genre_analysis': genre_stats,
        'yearly_analysis': year_stats,
        'top_rated_games': top_rated,
        'top_selling_games': top_selling,
        'best_value_games': best_value
    }


def print_analysis(analysis_results):
    """Print the analysis results in a formatted way"""
    print("\n=== GAME ANALYSIS RESULTS ===\n")

    print("Basic Statistics:")
    for key, value in analysis_results['basic_stats'].items():
        print(f"{key.replace('_', ' ').title()}: {value:.2f}")

    print("\nGenre Analysis:")
    print(analysis_results['genre_analysis'])

    print("\nYearly Analysis:")
    print(analysis_results['yearly_analysis'])

    print("\nTop Rated Games:")
    print(analysis_results['top_rated_games'])

    print("\nTop Selling Games:")
    print(analysis_results['top_selling_games'])

    print("\nBest Value Games:")
    print(analysis_results['best_value_games'])


# Example usage
if __name__ == "__main__":
    # Create sample data
    games_df = create_sample_game_data()

    # Perform analysis
    results = analyze_games(games_df)

    # Print results
    print_analysis(results)

    # Additional analysis examples

    # Filter games by rating threshold
    high_rated = games_df[games_df['rating'] > 9.0]
    print("\nGames rated above 9.0:")
    print(high_rated[['game_title', 'rating']])

    # Calculate correlation between price and playtime
    correlation = games_df['price'].corr(games_df['playtime_hours'])
    print(f"\nCorrelation between price and playtime: {correlation:.2f}")

    # Average sales by genre
    avg_sales_by_genre = games_df.groupby('genre')['sales_millions'].mean()
    print("\nAverage sales by genre:")
    print(avg_sales_by_genre)