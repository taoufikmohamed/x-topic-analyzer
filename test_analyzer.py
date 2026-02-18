"""
Mock X Topic Analyzer - Test without API credentials
This version uses simulated data for testing Excel export and formatting

This module provides a mock implementation of the X Topic Analyzer that:
- Uses pre-defined mock data instead of calling real APIs
- Allows testing of data processing and export functionality
- Works without requiring X API or DeepSeek API credentials
- Useful for development, testing, and demonstration purposes

Author: [Your Name]
Date: 2025
"""

import pandas as pd
from datetime import datetime, timedelta

# Sample mock data to simulate X API results
# This data represents typical tweet information for testing
MOCK_POSTS = [
    {
        'Topic': 'artificial intelligence',
        'Author': 'John Tech (@johntech)',
        'Author Verified': True,
        'Post Date': '2025-02-15 10:30',
        'Post Link': 'https://twitter.com/johntech/status/1234567890',
        'Short Summary': 'AI continues to reshape industries with breakthrough innovation.',
        'Original Text': 'Latest AI models show promising results in healthcare applications. Researchers report 95% accuracy in medical imaging...',
        'Engagement': '❤️ 1250 | 🔄 345 | 💬 89'
    },
    # ... (other mock posts remain the same)
    {
        'Topic': 'artificial intelligence',
        'Author': 'John Tech (@johntech)',
        'Author Verified': True,
        'Post Date': '2025-02-15 10:30',
        'Post Link': 'https://twitter.com/johntech/status/1234567890',
        'Short Summary': 'AI continues to reshape industries with breakthrough innovation.',
        'Original Text': 'Latest AI models show promising results in healthcare applications. Researchers report 95% accuracy in medical imaging...',
        'Engagement': '❤️ 1250 | 🔄 345 | 💬 89'
    },
    {
        'Topic': 'artificial intelligence',
        'Author': 'Tech News Daily (@technewstoday)',
        'Author Verified': True,
        'Post Date': '2025-02-15 09:15',
        'Post Link': 'https://twitter.com/technewstoday/status/5678901234',
        'Short Summary': 'Major tech companies announce significant investments in AI research.',
        'Original Text': 'Fortune 500 companies announce $50B investment in AI infrastructure. This marks the largest single investment in artificial...',
        'Engagement': '❤️ 2100 | 🔄 567 | 💬 234'
    },
    {
        'Topic': 'artificial intelligence',
        'Author': 'AI Research Lab (@airesearchlab)',
        'Author Verified': True,
        'Post Date': '2025-02-15 08:45',
        'Post Link': 'https://twitter.com/airesearchlab/status/2345678901',
        'Short Summary': 'New study reveals ethical considerations in AI model development.',
        'Original Text': 'Our latest research explores the ethical implications of large language models. Key findings include bias detection and mitigation...',
        'Engagement': '❤️ 3400 | 🔄 892 | 💬 567'
    },
    {
        'Topic': 'artificial intelligence',
        'Author': 'StartUp AI (@aistartupers)',
        'Author Verified': False,
        'Post Date': '2025-02-15 07:20',
        'Post Link': 'https://twitter.com/aistartupers/status/3456789012',
        'Short Summary': 'Emerging AI startups disrupting traditional business models.',
        'Original Text': 'New AI startup raises $100M Series B funding focused on autonomous systems. The company plans to expand to 5 new markets...',
        'Engagement': '❤️ 856 | 🔄 234 | 💬 178'
    },
    {
        'Topic': 'artificial intelligence',
        'Author': 'ML Engineer (@mlengineers)',
        'Author Verified': False,
        'Post Date': '2025-02-14 22:10',
        'Post Link': 'https://twitter.com/mlengineers/status/4567890123',
        'Short Summary': 'Technical tutorial on implementing transformer models in production.',
        'Original Text': 'Tutorial: Building production-ready transformer models. Today we cover model optimization, quantization, and deployment best practices...',
        'Engagement': '❤️ 645 | 🔄 289 | 💬 145'
    }
]

class MockXTopicAnalyzer:
    """Mock analyzer that uses simulated data instead of real API calls"""
    
    def __init__(self):
        """Initialize with mock data - no API credentials needed"""
        print("✅ Mock analyzer initialized (no API credentials required)")
    
    def analyze_topic(self, keyword: str, max_posts: int = 50) -> pd.DataFrame:
        """
        Return mock analyzed data for testing purposes
        
        Args:
            keyword: Topic keyword (not used in mock, just for compatibility)
            max_posts: Maximum posts to return
            
        Returns:
            DataFrame with mock analyzed results
        """
        print(f"🔍 [MOCK] Searching for: '{keyword}'")
        print(f"📊 [MOCK] Returning {min(len(MOCK_POSTS), max_posts)} mock posts")
        
        # Return limited number of posts based on max_posts parameter
        posts = MOCK_POSTS[:min(len(MOCK_POSTS), max_posts)]
        return pd.DataFrame(posts)
    
    def save_to_excel(self, df: pd.DataFrame, filename: str = None):
        """
        Save results to file (CSV when openpyxl not available, Excel otherwise)
        
        Args:
            df: DataFrame to save
            filename: Output filename (optional, auto-generated with timestamp)
        """
        if df.empty:
            print("No data to save")
            return
        
        # Generate timestamped filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            # Try to use xlsx if openpyxl available, otherwise use csv
            try:
                import openpyxl
                filename = f"x_analysis_mock_{timestamp}.xlsx"
            except ImportError:
                filename = f"x_analysis_mock_{timestamp}.csv"
        
        print(f"💾 Saving results to: {filename}")
        
        try:
            # Try Excel format if openpyxl is available
            if filename.endswith('.xlsx'):
                with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='X Analysis', index=False)
                    
                    # Get workbook and worksheet for formatting
                    workbook = writer.book
                    worksheet = writer.sheets['X Analysis']
                    
                    # Auto-adjust column widths
                    for column in worksheet.columns:
                        max_length = 0
                        column_letter = column[0].column_letter
                        
                        for cell in column:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except:
                                pass
                        
                        adjusted_width = min(max_length + 2, 50)
                        worksheet.column_dimensions[column_letter].width = adjusted_width
                    
                    # Format header with bold white font on blue background
                    try:
                        from openpyxl.styles import Font, PatternFill
                        header_font = Font(bold=True, color='FFFFFF')
                        header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
                        
                        for cell in worksheet[1]:
                            cell.font = header_font
                            cell.fill = header_fill
                    except ImportError:
                        pass  # Skip formatting if openpyxl styles not available
            else:
                # Save as CSV if Excel not supported
                df.to_csv(filename, index=False)
        except ImportError:
            # Fallback to CSV if openpyxl not available
            csv_filename = filename.replace('.xlsx', '.csv')
            df.to_csv(csv_filename, index=False)
            filename = csv_filename
        
        print(f"✅ Results saved to: {filename}")
        print(f"📈 Total posts analyzed: {len(df)}")


def main():
    """Run mock analysis for testing purposes"""
    print("=" * 60)
    print("🧪 X Topic Analyzer - MOCK TEST MODE (No API credentials needed)")
    print("=" * 60)
    print()
    
    # Create mock analyzer instance
    analyzer = MockXTopicAnalyzer()
    
    # Analyze topic with mock data
    keyword = "artificial intelligence"
    results_df = analyzer.analyze_topic(keyword, max_posts=5)
    
    # Save results to file
    if not results_df.empty:
        analyzer.save_to_excel(results_df)
        
        # Display sample results in console
        print("\n📊 Sample Results:")
        print("=" * 60)
        print(results_df[['Author', 'Short Summary', 'Engagement']].to_string(index=False))
        print("\n✨ Full results saved with formatting!")
    else:
        print("No results found.")


if __name__ == "__main__":
    main()