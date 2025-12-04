#!/usr/bin/env python3
"""
TF-IDF Analysis Script
Computes the top 10 words with highest TF-IDF scores for each topic
from articles_by_topic.json and visualizes them in a 2x4 grid of bar charts.
"""

import json
import re
from collections import Counter, defaultdict
from typing import Dict, List, Tuple
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from pathlib import Path

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
    'being', 'down', 'off', 'against', 'etc', 'us', 'him'
])


def extract_title_from_url(url: str) -> str:
    """
    Extract the title from a URL.
    If the URL is an HTTP link, fetch the page and extract the title.
    Otherwise, treat it as plain text.
    
    Args:
        url: The URL or text to process
        
    Returns:
        The extracted title or text
    """
    if url.startswith('http://') or url.startswith('https://'):
        try:
            # Fetch the page with a timeout
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; TF-IDF Analysis Bot)'
            })
            response.raise_for_status()
            
            # Parse the HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to get the title
            title_tag = soup.find('title')
            if title_tag:
                return title_tag.get_text().strip()
            
            # If no title tag, try h1
            h1_tag = soup.find('h1')
            if h1_tag:
                return h1_tag.get_text().strip()
            
            # Fallback to URL
            return url
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            # Return the URL itself as fallback
            return url
    else:
        # It's already text, just return it
        return url


def clean_text(text: str) -> List[str]:
    """
    Clean and tokenize text.
    
    Args:
        text: The text to clean
        
    Returns:
        List of cleaned tokens
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs that might be in the text
    text = re.sub(r'https?://\S+', '', text)
    
    # Keep only alphanumeric characters and spaces
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    
    # Split into words
    words = text.split()
    
    # Filter out stopwords and short words
    words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    
    return words


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
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        max_features=None,
        stop_words=None,  # We already removed stopwords
        lowercase=False,  # Already lowercased
        token_pattern=r'\b\w+\b'
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


def visualize_tfidf(topic_top_words: Dict[str, List[Tuple[str, float]]], output_file: str):
    """
    Create a 2x4 grid visualization of top TF-IDF words per topic.
    
    Args:
        topic_top_words: Dictionary mapping topics to list of (word, score) tuples
        output_file: Path to save the visualization
    """
    # Create a 2x4 grid
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    fig.suptitle('Top 10 TF-IDF Words by Topic', fontsize=16, fontweight='bold')
    
    # Flatten axes for easier iteration
    axes = axes.flatten()
    
    # Plot each topic
    for idx, (topic, top_words) in enumerate(topic_top_words.items()):
        ax = axes[idx]
        
        # Extract words and scores
        words = [word for word, score in top_words]
        scores = [score for word, score in top_words]
        
        # Create bar chart
        y_pos = np.arange(len(words))
        ax.barh(y_pos, scores, align='center', color='steelblue', alpha=0.8)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(words)
        ax.invert_yaxis()  # Top word at the top
        ax.set_xlabel('TF-IDF Score', fontsize=10)
        ax.set_title(topic, fontsize=11, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Visualization saved to {output_file}")
    plt.close()


def main():
    """Main function to run the TF-IDF analysis."""
    print("Loading articles_by_topic.json...")
    
    # Load the JSON data
    with open(ANNOTATED_DATA_PATH, 'r') as f:
        data = json.load(f)
    
    print(f"Found {len(data)} topics")
    
    # Extract text for each topic
    topic_texts = {}
    
    for topic, articles in data.items():
        print(f"\nProcessing topic: {topic} ({len(articles)} articles)")
        all_words = []
        
        for i, article in enumerate(articles):
            url = article.get('URL', '')
            
            # Extract title/text from URL
            text = extract_title_from_url(url)
            
            # Clean and tokenize
            words = clean_text(text)
            all_words.extend(words)
            
            if (i + 1) % 20 == 0:
                print(f"  Processed {i + 1}/{len(articles)} articles...")
        
        # Join all words for this topic into a single document
        topic_texts[topic] = ' '.join(all_words)
        print(f"  Total words for {topic}: {len(all_words)}")
    
    print("\nComputing TF-IDF scores...")
    topic_top_words = compute_tfidf(topic_texts)
    
    # Print results
    print("\n" + "="*80)
    print("TOP 10 TF-IDF WORDS PER TOPIC")
    print("="*80)
    
    for topic, top_words in topic_top_words.items():
        print(f"\n{topic}:")
        for i, (word, score) in enumerate(top_words, 1):
            print(f"  {i:2d}. {word:20s} {score:.4f}")
    
    # Create visualization
    print("\nCreating visualization...")
    visualize_tfidf(topic_top_words, OUTPUT_PATH)
    
    print("\nDone!")


if __name__ == '__main__':
    main()
