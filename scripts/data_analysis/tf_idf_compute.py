#!/usr/bin/env python3
"""
TF-IDF Analysis Script
Computes the top 10 words with highest TF-IDF scores for each topic
from articles_by_topic.json and visualizes them in a matplotlib bar chart.
Uses the 'Text' and 'Title' fields from the JSON data.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Directory configuration
ROOT_DIR = Path(__file__).parent.parent.parent
DATA_DIR = ROOT_DIR / 'data'
DATA_ANALYSIS_DIR = DATA_DIR / 'data_analysis'
DATA_ANNOTATION_DIR = DATA_DIR / 'data_annotation'
ANNOTATED_DATA_PATH = DATA_ANNOTATION_DIR / 'articles_by_topic.json'
OUTPUT_PATH = DATA_ANALYSIS_DIR / 'tf_idf.png'

# Common English stopwords
STOPWORDS = set([
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
    'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i',
    'you', 'he', 'she', 'it', 'we', 'they', 'them', 'their', 'what', 'which',
    'who', 'when', 'where', 'why', 'how', 'all', 'each', 'every', 'both',
    'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'just',
    'don', 'now', 'if', 'after', 'over', 'his', 'her', 'its', 'my', 'our',
    'your', 'up', 'out', 'about', 'into', 'through', 'during', 'before',
    'after', 'above', 'below', 'between', 'under', 'again', 'further',
    'then', 'once', 'here', 'there', 'all', 'any', 'because', 'am', 'been',
    'being', 'down', 'off', 'against', 'etc', 'us', 'him', 'new', 'york',
    'city', 'nyc', 'mamdani', 'zohran', 'mayor', 'elect', 'said', 'says'
])


def clean_text(text: str) -> str:
    """
    Clean and normalize text.
    
    Args:
        text: The text to clean
        
    Returns:
        Cleaned text
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)
    
    # Remove special characters but keep spaces
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def extract_topic_documents(data: Dict[str, List[Dict]]) -> Dict[str, str]:
    """
    Extract and combine text from articles for each topic.
    
    Args:
        data: Dictionary mapping topic names to lists of article dictionaries
        
    Returns:
        Dictionary mapping topic names to concatenated cleaned text
    """
    topic_documents = {}
    
    for topic, articles in data.items():
        print(f"Processing topic: {topic} ({len(articles)} articles)")
        
        all_text = []
        for article in articles:
            # Extract Title and Text fields
            title = article.get('Title', '')
            text = article.get('Text', '')
            
            # Combine title and text
            combined = f"{title} {text}"
            
            # Clean the text
            cleaned = clean_text(combined)
            all_text.append(cleaned)
        
        # Combine all articles for this topic into one document
        topic_documents[topic] = ' '.join(all_text)
        print(f"  Total characters: {len(topic_documents[topic])}")
    
    return topic_documents


def compute_tfidf(topic_documents: Dict[str, str]) -> Dict[str, List[Tuple[str, float]]]:
    """
    Compute TF-IDF scores for each topic.
    
    Args:
        topic_documents: Dictionary mapping topic names to concatenated text documents
        
    Returns:
        Dictionary mapping topic names to list of (word, score) tuples
    """
    # Get topics and documents in order
    topics = list(topic_documents.keys())
    documents = [topic_documents[topic] for topic in topics]
    
    # Create TF-IDF vectorizer with custom stopwords
    vectorizer = TfidfVectorizer(
        max_features=None,
        stop_words=list(STOPWORDS),
        lowercase=True,
        token_pattern=r'\b[a-z]{3,}\b',  # Only words with 3+ letters
        min_df=1,  # Must appear in at least 1 document
        max_df=0.95  # Ignore words appearing in >95% of documents
    )
    
    # Fit and transform
    tfidf_matrix = vectorizer.fit_transform(documents)
    feature_names = vectorizer.get_feature_names_out()
    
    # Extract top words for each topic
    topic_top_words = {}
    
    for i, topic in enumerate(topics):
        # Get TF-IDF scores for this topic
        scores = tfidf_matrix[i].toarray()[0]
        
        # Get top 10 words
        top_indices = np.argsort(scores)[-10:][::-1]
        top_words = [(feature_names[idx], scores[idx]) for idx in top_indices]
        
        topic_top_words[topic] = top_words
    
    return topic_top_words


def visualize_tfidf(topic_top_words: Dict[str, List[Tuple[str, float]]], output_file: Path):
    """
    Create a visualization of top TF-IDF words per topic.
    
    Args:
        topic_top_words: Dictionary mapping topics to list of (word, score) tuples
        output_file: Path to save the visualization
    """
    num_topics = len(topic_top_words)
    
    # Determine grid layout
    if num_topics <= 4:
        nrows, ncols = 1, num_topics
        figsize = (5 * num_topics, 5)
    elif num_topics <= 8:
        nrows, ncols = 2, 4
        figsize = (20, 10)
    else:
        nrows = (num_topics + 3) // 4
        ncols = 4
        figsize = (20, 5 * nrows)
    
    # Create subplots
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
    fig.suptitle('Top 10 TF-IDF Words by Topic', fontsize=16, fontweight='bold', y=0.995)
    
    # Flatten axes for easier iteration
    if num_topics == 1:
        axes = [axes]
    else:
        axes = axes.flatten() if isinstance(axes, np.ndarray) else [axes]
    
    # Plot each topic
    for idx, (topic, top_words) in enumerate(topic_top_words.items()):
        ax = axes[idx]
        
        # Extract words and scores
        words = [word for word, score in top_words]
        scores = [score for word, score in top_words]
        
        # Create horizontal bar chart
        y_pos = np.arange(len(words))
        ax.barh(y_pos, scores, align='center', color='steelblue', alpha=0.8)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(words, fontsize=9)
        ax.invert_yaxis()  # Top word at the top
        ax.set_xlabel('TF-IDF Score', fontsize=9)
        ax.set_title(topic, fontsize=10, fontweight='bold', pad=10)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        # Add value labels on bars
        for i, (y, score) in enumerate(zip(y_pos, scores)):
            ax.text(score, y, f' {score:.3f}', va='center', fontsize=7, color='black')
    
    # Hide extra subplots
    for idx in range(num_topics, len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nVisualization saved to {output_file}")
    plt.close()


def main():
    """Main function to run the TF-IDF analysis."""
    print("="*80)
    print("TF-IDF Analysis for Articles by Topic")
    print("="*80)
    
    # Ensure output directory exists
    DATA_ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load the JSON data
    print(f"\nLoading data from: {ANNOTATED_DATA_PATH}")
    with open(ANNOTATED_DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Found {len(data)} topics\n")
    
    # Extract text for each topic
    topic_documents = extract_topic_documents(data)
    
    # Compute TF-IDF scores
    print("\nComputing TF-IDF scores...")
    topic_top_words = compute_tfidf(topic_documents)
    
    # Print results
    print("\n" + "="*80)
    print("TOP 10 TF-IDF WORDS PER TOPIC")
    print("="*80)
    
    for topic, top_words in topic_top_words.items():
        print(f"\n{topic}:")
        for i, (word, score) in enumerate(top_words, 1):
            print(f"  {i:2d}. {word:20s} {score:.4f}")
    
    # Create visualization
    print("\n" + "="*80)
    print("Creating visualization...")
    visualize_tfidf(topic_top_words, OUTPUT_PATH)
    
    print("="*80)
    print("Analysis complete!")
    print("="*80)


if __name__ == '__main__':
    main()
