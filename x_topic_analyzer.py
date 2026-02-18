"""
X Topic Analyzer - A tool for searching and analyzing topics on X (formerly Twitter)

This module provides functionality to:
- Search for recent posts on X using keywords
- Generate AI-powered summaries of posts using DeepSeek LLM
- Analyze topic sentiment and engagement
- Export results to formatted Excel files

Author: [Your Name]
Date: 2025
"""

import os
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time
import tweepy
from openai import OpenAI
import argparse
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Debug prints (commented out for production)
# print(f"DEBUG: X_BEARER_TOKEN={os.getenv('X_BEARER_TOKEN')}")
# print(f"DEBUG: DEEPSEEK_API_KEY={os.getenv('DEEPSEEK_API_KEY')}")

class XTopicAnalyzer:
    """
    Main class for analyzing topics on X (Twitter) platform.
    
    This class handles:
    - Authentication with X API and DeepSeek AI
    - Searching for posts based on keywords
    - Generating summaries using AI
    - Formatting and exporting results
    """
    
    def __init__(self, bearer_token: str, deepseek_api_key: str):
        """
        Initialize the X Topic Analyzer with API credentials
        
        Args:
            bearer_token: X API Bearer Token for authentication
            deepseek_api_key: DeepSeek API Key for AI summarization
        """
        # Initialize X API client with rate limiting enabled
        self.client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)
        
        # Initialize DeepSeek client for AI-powered summarization
        self.deepseek_client = OpenAI(
            api_key=deepseek_api_key,
            base_url="https://api.deepseek.com"
        )
        
    def search_x_posts(self, keyword: str, max_results: int = 100) -> List[Dict]:
        """
        Search for posts on X based on keyword
        
        Args:
            keyword: Search term to query X API
            max_results: Maximum number of results to return (capped at 100 by API)
            
        Returns:
            List of post data dictionaries containing tweet information
        """
        try:
            # Construct search query: keyword, exclude retweets, English language only
            query = f"{keyword} -is:retweet lang:en"
            
            # Call X API to search for recent tweets
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=min(max_results, 100),  # API limit is 100
                tweet_fields=['created_at', 'public_metrics', 'author_id', 'text'],
                user_fields=['username', 'name', 'verified'],
                expansions='author_id'  # Include author information
            )
            
            # Handle case where no tweets are found
            if not tweets.data:
                print(f"No tweets found for keyword: {keyword}")
                return []
            
            # Create user dictionary for quick author lookup
            users = {}
            if tweets.includes and 'users' in tweets.includes:
                for user in tweets.includes['users']:
                    users[user.id] = user
            
            # Process each tweet and extract relevant information
            posts_data = []
            for tweet in tweets.data:
                author = users.get(tweet.author_id)
                
                # Compile post information into dictionary
                post_info = {
                    'tweet_id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at,
                    'author_id': tweet.author_id,
                    'author_username': author.username if author else 'unknown',
                    'author_name': author.name if author else 'unknown',
                    'author_verified': author.verified if author else False,
                    'retweet_count': tweet.public_metrics['retweet_count'],
                    'like_count': tweet.public_metrics['like_count'],
                    'reply_count': tweet.public_metrics['reply_count'],
                    'url': f"https://twitter.com/{author.username if author else 'unknown'}/status/{tweet.id}"
                }
                posts_data.append(post_info)
            
            return posts_data
            
        except Exception as e:
            # Handle API errors gracefully
            print(f"Error searching X: {str(e)}")
            return []
    
    def generate_summary_with_deepseek(self, text: str, keyword: str) -> str:
        """
        Generate a concise summary using DeepSeek LLM
        
        Args:
            text: Original post text to summarize
            keyword: Search keyword for context in the prompt
            
        Returns:
            Generated summary string, or error message if failed
        """
        try:
            # Create a focused prompt for summarization
            prompt = f"""Analyze this social media post about '{keyword}' and provide a brief, objective summary (max 2-3 sentences):

Post: {text}

Focus on:
1. Main point or claim
2. Key context
3. Relevance to topic

Summary:"""

            # Call DeepSeek API for summarization
            response = self.deepseek_client.chat.completions.create(
                model="deepseek-chat",  # Use DeepSeek's chat model
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates concise, objective summaries of social media posts."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,  # Limit response length
                temperature=0.3  # Lower temperature for more consistent summaries
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # Handle API errors gracefully
            print(f"Error generating summary: {str(e)}")
            return "Summary generation failed"
    
    def analyze_topic(self, keyword: str, max_posts: int = 50) -> pd.DataFrame:
        """
        Main method to search and analyze a topic
        
        Args:
            keyword: Topic to search for on X
            max_posts: Maximum number of posts to analyze
            
        Returns:
            DataFrame with analyzed results including summaries and metadata
        """
        print(f"🔍 Searching X for: '{keyword}'")
        posts = self.search_x_posts(keyword, max_results=max_posts)
        
        if not posts:
            return pd.DataFrame()
        
        print(f"📊 Found {len(posts)} posts. Generating summaries...")
        
        # Generate AI summaries for each post
        analyzed_posts = []
        for i, post in enumerate(posts, 1):
            print(f"  Processing post {i}/{len(posts)}...")
            
            # Generate summary using DeepSeek
            summary = self.generate_summary_with_deepseek(post['text'], keyword)
            
            # Compile analyzed post data
            analyzed_post = {
                'Topic': keyword,
                'Author': f"{post['author_name']} (@{post['author_username']})",
                'Author Verified': post['author_verified'],
                'Post Date': post['created_at'].strftime('%Y-%m-%d %H:%M'),
                'Post Link': post['url'],
                'Short Summary': summary,
                'Original Text': post['text'][:200] + '...' if len(post['text']) > 200 else post['text'],
                'Engagement': f"❤️ {post['like_count']} | 🔄 {post['retweet_count']} | 💬 {post['reply_count']}"
            }
            analyzed_posts.append(analyzed_post)
            
            # Rate limiting to avoid API throttling
            time.sleep(0.5)
        
        return pd.DataFrame(analyzed_posts)
    
    def save_to_excel(self, df: pd.DataFrame, filename: str = None):
        """
        Save results to Excel file with formatting
        
        Args:
            df: DataFrame to save
            filename: Output filename (optional, auto-generated if not provided)
        """
        if df.empty:
            print("No data to save")
            return
        
        # Generate timestamped filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"x_analysis_{timestamp}.xlsx"
        
        # Create Excel writer with formatting
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='X Analysis', index=False)
            
            # Get workbook and worksheet for formatting
            workbook = writer.book
            worksheet = writer.sheets['X Analysis']
            
            # Auto-adjust column widths for better readability
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                
                adjusted_width = min(max_length + 2, 50)  # Cap at 50 for readability
                worksheet.column_dimensions[column_letter].width = adjusted_width
            
            # Format header row with bold font and blue background
            from openpyxl.styles import Font, PatternFill
            header_font = Font(bold=True)
            header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
            
            for cell in worksheet[1]:
                cell.font = header_font
                cell.fill = header_fill
        
        print(f"✅ Results saved to: {filename}")
        print(f"📈 Total posts analyzed: {len(df)}")

def main():
    """
    Main entry point for the X Topic Analyzer CLI application
    
    Handles command-line arguments, environment variables, and orchestrates the analysis workflow.
    """
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description='X Topic Search and Analysis')
    parser.add_argument('--keyword', type=str, help='Topic to search for')
    parser.add_argument('--max-posts', type=int, default=50, help='Maximum posts to analyze')
    parser.add_argument('--x-bearer-token', type=str, help='X API Bearer Token')
    parser.add_argument('--deepseek-key', type=str, help='DeepSeek API Key')
    
    args = parser.parse_args()
    
    # Get API credentials from arguments or environment variables
    X_BEARER_TOKEN = args.x_bearer_token or os.getenv('X_BEARER_TOKEN')
    DEEPSEEK_API_KEY = args.deepseek_key or os.getenv('DEEPSEEK_API_KEY')
    
    # Validate that required credentials are available
    if not X_BEARER_TOKEN or not DEEPSEEK_API_KEY:
        print("❌ Error: Missing API credentials")
        print("Please provide X Bearer Token and DeepSeek API Key")
        print("You can set them as environment variables or pass as arguments")
        return
    
    # Get search keyword from arguments or user input
    keyword = args.keyword
    if not keyword:
        keyword = input("Enter topic to search for: ")
    
    # Create analyzer instance with credentials
    analyzer = XTopicAnalyzer(X_BEARER_TOKEN, DEEPSEEK_API_KEY)
    
    # Perform topic analysis
    results_df = analyzer.analyze_topic(keyword, max_posts=args.max_posts)
    
    # Save and display results
    if not results_df.empty:
        analyzer.save_to_excel(results_df)
        print("\n📊 Sample Results:")
        print(results_df[['Author', 'Short Summary', 'Post Link']].head().to_string())
    else:
        print("No results found.")

if __name__ == "__main__":
    main()