#!/usr/bin/env python3
"""
Topic Distribution Visualization Script
Generates a bar chart showing the distribution of articles across different topics.
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
DATA_DIR = ROOT_DIR / 'data'
DATA_ANALYSIS_DIR = DATA_DIR / 'data_analysis'
DATA_ANNOTATION_DIR = DATA_DIR / 'data_annotation'
DATA_ANNOTATED_PATH = DATA_ANNOTATION_DIR / 'articles_by_topic.json'
OUTPUT_PATH = DATA_ANALYSIS_DIR / 'topic_distribution.png'


def load_topic_data(filepath):
    """
    Load topic data from JSON file.
    
    Args:
        filepath: Path to the JSON file containing articles by topic
        
    Returns:
        Dictionary mapping topic names to list of articles
    """
    with open(filepath, 'r') as f:
        return json.load(f)


def count_articles_per_topic(data):
    """
    Count the number of articles for each topic.
    
    Args:
        data: Dictionary mapping topics to articles
        
    Returns:
        Dictionary mapping topics to article counts
    """
    return {topic: len(articles) for topic, articles in data.items()}


def create_bar_chart(topic_counts, output_file=OUTPUT_PATH):
    """
    Create and save a bar chart of topic distribution.
    
    Args:
        topic_counts: Dictionary mapping topics to counts
        output_file: Path to save the chart image
    """
    # Sort topics by count (descending)
    sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
    topics = [item[0] for item in sorted_topics]
    counts = [item[1] for item in sorted_topics]
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create bar chart
    bars = ax.bar(range(len(topics)), counts, color='steelblue', alpha=0.8, edgecolor='black')
    
    # Customize the chart
    ax.set_xlabel('Topic', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Articles', fontsize=12, fontweight='bold')
    ax.set_title('Article Distribution Across Topics', fontsize=14, fontweight='bold', pad=20)
    
    # Set x-axis labels
    ax.set_xticks(range(len(topics)))
    ax.set_xticklabels(topics, rotation=45, ha='right')
    
    # Add value labels on top of bars
    for i, (bar, count) in enumerate(zip(bars, counts)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{count}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Add grid for better readability
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the figure
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Chart saved to {output_file}")
    
    # Close the plot
    plt.close()


def print_statistics(topic_counts):
    """
    Print summary statistics about the topic distribution.
    
    Args:
        topic_counts: Dictionary mapping topics to counts
    """
    total = sum(topic_counts.values())
    counts = list(topic_counts.values())
    
    print("\n" + "="*60)
    print("TOPIC DISTRIBUTION STATISTICS")
    print("="*60)
    print(f"\nTotal articles: {total}")
    print(f"Number of topics: {len(topic_counts)}")
    print(f"Average articles per topic: {total/len(topic_counts):.1f}")
    print(f"Minimum: {min(counts)} articles")
    print(f"Maximum: {max(counts)} articles")
    
    print("\nArticles per topic:")
    for topic, count in sorted(topic_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total) * 100
        print(f"  {topic:35s}: {count:3d} ({percentage:5.1f}%)")
    print("="*60 + "\n")


def main():
    """Main function to run the topic distribution analysis."""
    # Path to the data file
    data_file = DATA_ANNOTATED_PATH
    
    print("Loading topic data...")
    data = load_topic_data(data_file)
    
    print("Counting articles per topic...")
    topic_counts = count_articles_per_topic(data)
    
    print("Generating bar chart...")
    create_bar_chart(topic_counts, OUTPUT_PATH)
    
    print_statistics(topic_counts)
    
    print("Done!")


if __name__ == '__main__':
    main()
