#!/usr/bin/env python3
"""
Script to clean and standardize topics in the annotated_articles.json file.
Maps various topic variations to the 8 main standardized topics.
"""

import json
import os

# Define the 8 main topics
MAIN_TOPICS = {
    "Election Victory/Results",
    "Trump Conflicts",
    "Israel/Palestine/Antisemitism",
    "Personal Background/Family",
    "Controversies/Personal Attacks",
    "Policy Positions",
    "Campaign/Endorsements",
    "India/Hindu Relations"
}

# Define mapping from various topic variations to the main topics
TOPIC_MAPPING = {
    # Election related
    "Election Victory/Results": "Election Victory/Results",
    "Election results / official reporting": "Election Victory/Results",
    "Election results / victory speech": "Election Victory/Results",
    "Election results / policy coverage": "Election Victory/Results",
    "Electoral coverage / horse race": "Election Victory/Results",
    
    # Trump related
    "Trump Conflicts": "Trump Conflicts",
    "Trump / GOP reactions": "Trump Conflicts",
    
    # Israel/Palestine
    "Israel/Palestine/Antisemitism": "Israel/Palestine/Antisemitism",
    
    # Personal Background
    "Personal Background/Family": "Personal Background/Family",
    "Personal background / identity": "Personal Background/Family",
    
    # Controversies
    "Controversies/Personal Attacks": "Controversies/Personal Attacks",
    "Criticism / scandal / accusations": "Controversies/Personal Attacks",
    "Public backlash / mockery": "Controversies/Personal Attacks",
    "Political attacks / debate coverage": "Controversies/Personal Attacks",
    
    # Policy
    "Policy Positions": "Policy Positions",
    "Policing / NYPD controversy": "Policy Positions",
    "Crime & public safety narratives": "Policy Positions",
    "Crime / economic anxiety": "Policy Positions",
    "Fearmongering / crime / public reaction": "Policy Positions",
    "Right-wing fear narratives": "Policy Positions",
    
    # Campaign
    "Campaign/Endorsements": "Campaign/Endorsements",
    "Support & voter appeal": "Campaign/Endorsements",
    
    # India related
    "India/Hindu Relations": "India/Hindu Relations",
}


def standardize_topic(topic):
    """
    Standardize a topic string to one of the 8 main topics.
    
    Args:
        topic: The topic string to standardize
        
    Returns:
        The standardized topic string
    """
    # Handle None or empty string
    if not topic:
        return "Controversies/Personal Attacks"  # Default fallback
    
    # If topic contains "OR" or "/", take the first option
    if " OR " in topic:
        topic = topic.split(" OR ")[0].strip()
    
    # Check if the topic is already standardized
    if topic in MAIN_TOPICS:
        return topic
    
    # Try to find a mapping
    if topic in TOPIC_MAPPING:
        return TOPIC_MAPPING[topic]
    
    # If no exact match, try to find the best match based on keywords
    topic_lower = topic.lower()
    
    # Election related keywords
    if any(keyword in topic_lower for keyword in ["election", "victory", "results", "win", "electoral"]):
        return "Election Victory/Results"
    
    # Trump related keywords
    if any(keyword in topic_lower for keyword in ["trump", "gop", "republican"]):
        return "Trump Conflicts"
    
    # Israel/Palestine keywords
    if any(keyword in topic_lower for keyword in ["israel", "palestine", "antisemitism", "antisemite", "jewish", "jihadist", "hamas", "bds"]):
        return "Israel/Palestine/Antisemitism"
    
    # Personal Background keywords
    if any(keyword in topic_lower for keyword in ["personal", "background", "family", "identity", "net worth", "biography"]):
        return "Personal Background/Family"
    
    # Policy keywords
    if any(keyword in topic_lower for keyword in ["policy", "policing", "crime", "safety", "nypd", "tax", "billionaire", "economic"]):
        return "Policy Positions"
    
    # Campaign keywords
    if any(keyword in topic_lower for keyword in ["campaign", "endorsement", "support", "voter", "appeal", "pac"]):
        return "Campaign/Endorsements"
    
    # India/Hindu keywords
    if any(keyword in topic_lower for keyword in ["india", "hindu", "modi", "kangana", "bollywood"]):
        return "India/Hindu Relations"
    
    # Controversies keywords (catch-all for attacks, scandals, etc.)
    if any(keyword in topic_lower for keyword in ["controversy", "attack", "scandal", "criticism", "backlash", "mockery"]):
        return "Controversies/Personal Attacks"
    
    # Default fallback
    print(f"Warning: Could not categorize topic '{topic}', defaulting to 'Controversies/Personal Attacks'")
    return "Controversies/Personal Attacks"


def clean_annotated_articles(input_file, output_file):
    """
    Clean the annotated articles by standardizing topic values.
    
    Args:
        input_file: Path to the input JSON file
        output_file: Path to the output JSON file
    """
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    # Track statistics
    topic_changes = {}
    
    # Process each article
    for article in articles:
        original_topic = article.get("Topic", "")
        standardized_topic = standardize_topic(original_topic)
        
        # Track changes
        if original_topic != standardized_topic:
            if original_topic not in topic_changes:
                topic_changes[original_topic] = {"count": 0, "mapped_to": standardized_topic}
            topic_changes[original_topic]["count"] += 1
        
        # Update the topic
        article["Topic"] = standardized_topic
    
    # Write the cleaned data to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    
    # Print statistics
    print(f"\nCleaning complete!")
    print(f"Total articles processed: {len(articles)}")
    print(f"\nTopic changes made:")
    for original, info in sorted(topic_changes.items()):
        print(f"  '{original}' -> '{info['mapped_to']}' ({info['count']} articles)")
    
    # Count final distribution
    topic_distribution = {}
    for article in articles:
        topic = article["Topic"]
        topic_distribution[topic] = topic_distribution.get(topic, 0) + 1
    
    print(f"\nFinal topic distribution:")
    for topic in sorted(MAIN_TOPICS):
        count = topic_distribution.get(topic, 0)
        print(f"  {topic}: {count} articles")


if __name__ == "__main__":
    # Define file paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, "data", "annotated_articles.json")
    output_file = os.path.join(base_dir, "data", "clean_annotated_articles.json")
    
    # Run the cleaning
    clean_annotated_articles(input_file, output_file)
