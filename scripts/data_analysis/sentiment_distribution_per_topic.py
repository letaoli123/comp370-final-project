#!/usr/bin/env python3
"""
Sentiment Distribution Analysis Script
Analyzes and visualizes the sentiment distribution for each topic
from articles_by_topic.json using a 2x4 grid of pie charts.
"""

import json
from pathlib import Path
from typing import Dict, List
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np

# Directory configuration
ROOT_DIR = Path(__file__).parent.parent.parent
DATA_DIR = ROOT_DIR / 'data'
DATA_ANALYSIS_DIR = DATA_DIR / 'data_analysis'
DATA_ANNOTATION_DIR = DATA_DIR / 'data_annotation'
ANNOTATED_DATA_PATH = DATA_ANNOTATION_DIR / 'articles_by_topic.json'
OUTPUT_PATH = DATA_ANALYSIS_DIR / 'sentiment_distribution.png'

# Sentiment colors
SENTIMENT_COLORS = {
    'Positive': '#2ecc71',  # Green
    'Neutral': '#95a5a6',   # Gray
    'Negative': '#e74c3c'   # Red
}


def analyze_sentiment_distribution(data: Dict[str, List[Dict]]) -> Dict[str, Dict[str, int]]:
    """
    Analyze sentiment distribution for each topic.
    
    Args:
        data: Dictionary mapping topic names to lists of article dictionaries
        
    Returns:
        Dictionary mapping topic names to sentiment counts
    """
    topic_sentiments = {}
    
    for topic, articles in data.items():
        # Count sentiments for this topic
        sentiments = [article.get('Sentiment', 'Unknown') for article in articles]
        sentiment_counts = Counter(sentiments)
        topic_sentiments[topic] = dict(sentiment_counts)
        
        print(f"{topic}: {len(articles)} articles")
        for sentiment, count in sorted(sentiment_counts.items()):
            percentage = (count / len(articles)) * 100
            print(f"  {sentiment}: {count} ({percentage:.1f}%)")
    
    return topic_sentiments


def visualize_sentiment_distribution(topic_sentiments: Dict[str, Dict[str, int]], output_file: Path):
    """
    Create a 2x4 grid visualization of sentiment distribution per topic.
    
    Args:
        topic_sentiments: Dictionary mapping topics to sentiment counts
        output_file: Path to save the visualization
    """
    num_topics = len(topic_sentiments)
    
    # Create a 2x4 grid
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    fig.suptitle('Sentiment Distribution by Topic', fontsize=16, fontweight='bold', y=0.995)
    
    # Flatten axes for easier iteration
    axes = axes.flatten()
    
    # Plot each topic
    for idx, (topic, sentiments) in enumerate(topic_sentiments.items()):
        ax = axes[idx]
        
        # Prepare data for pie chart
        # Ensure consistent order: Positive, Neutral, Negative
        sentiment_order = ['Positive', 'Neutral', 'Negative']
        counts = [sentiments.get(sentiment, 0) for sentiment in sentiment_order]
        colors = [SENTIMENT_COLORS[sentiment] for sentiment in sentiment_order]
        
        # Filter out zero counts
        filtered_sentiments = []
        filtered_counts = []
        filtered_colors = []
        for sentiment, count, color in zip(sentiment_order, counts, colors):
            if count > 0:
                filtered_sentiments.append(sentiment)
                filtered_counts.append(count)
                filtered_colors.append(color)
        
        # Create pie chart
        total = sum(filtered_counts)
        percentages = [(count / total) * 100 for count in filtered_counts]
        
        wedges, texts, autotexts = ax.pie(
            filtered_counts,
            labels=filtered_sentiments,
            colors=filtered_colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 9}
        )
        
        # Make percentage text bold and white
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        # Set title with total count
        ax.set_title(f"{topic}\n({total} articles)", fontsize=10, fontweight='bold', pad=10)
    
    # Hide extra subplots
    for idx in range(num_topics, len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nVisualization saved to {output_file}")
    plt.close()


def print_overall_statistics(topic_sentiments: Dict[str, Dict[str, int]]):
    """
    Print overall sentiment statistics across all topics.
    
    Args:
        topic_sentiments: Dictionary mapping topics to sentiment counts
    """
    # Aggregate all sentiments
    total_sentiments = Counter()
    total_articles = 0
    
    for sentiments in topic_sentiments.values():
        for sentiment, count in sentiments.items():
            total_sentiments[sentiment] += count
            total_articles += count
    
    print("\n" + "="*80)
    print("OVERALL SENTIMENT STATISTICS")
    print("="*80)
    print(f"\nTotal articles: {total_articles}")
    print(f"\nSentiment breakdown:")
    
    for sentiment in ['Positive', 'Neutral', 'Negative']:
        count = total_sentiments.get(sentiment, 0)
        percentage = (count / total_articles) * 100 if total_articles > 0 else 0
        print(f"  {sentiment:10s}: {count:4d} ({percentage:5.1f}%)")
    
    print("="*80)


def main():
    """Main function to run the sentiment distribution analysis."""
    print("="*80)
    print("Sentiment Distribution Analysis")
    print("="*80)
    
    # Ensure output directory exists
    DATA_ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load the JSON data
    print(f"\nLoading data from: {ANNOTATED_DATA_PATH}")
    with open(ANNOTATED_DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Found {len(data)} topics\n")
    
    # Analyze sentiment distribution
    print("Analyzing sentiment distribution...\n")
    topic_sentiments = analyze_sentiment_distribution(data)
    
    # Print overall statistics
    print_overall_statistics(topic_sentiments)
    
    # Create visualization
    print("\nCreating visualization...")
    visualize_sentiment_distribution(topic_sentiments, OUTPUT_PATH)
    
    print("\nAnalysis complete!")
    print("="*80)


if __name__ == '__main__':
    main()
