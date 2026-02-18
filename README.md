# X Topic Search and Analysis App

A powerful Python application for searching and analyzing topics on X (formerly Twitter) using AI-powered summarization!.

## 📋 Project Overview

This application allows you to:
- **Search X posts** by keywords using the Twitter API v2
- **Generate AI summaries** of posts using DeepSeek LLM
- **Analyze engagement metrics** (likes, retweets, replies)
- **Export results** to beautifully formatted Excel files
- **Test functionality** with mock data (no API keys required)

## 🚀 Features

- 🔍 **Real-time X Search**: Search recent posts with advanced filtering
- 🤖 **AI-Powered Summaries**: Generate concise, objective summaries using DeepSeek
- 📊 **Engagement Analysis**: Track likes, retweets, and replies
- 📈 **Excel Export**: Professional formatting with auto-adjusted columns
- 🧪 **Mock Testing**: Test all features without API credentials
- ⚡ **Rate Limiting**: Built-in delays to respect API limits
- 🔒 **Secure Credentials**: Environment variable support for API keys

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Virtual environment (recommended)

### Setup Steps

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd x-topic-search-analysis
   ```

2. **Create virtual environment**
   ```bash
   python -m venv Xtwe
   # On Windows:
   Xtwe\Scripts\activate
   # On macOS/Linux:
   source Xtwe/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API credentials** (see Configuration section below)

## ⚙️ Configuration

### API Credentials Required

You need two API keys to use the full functionality:

1. **X (Twitter) API Bearer Token**
   - Get from [Twitter Developer Portal](https://developer.twitter.com/)
   - Create a project and app to get Bearer Token

2. **DeepSeek API Key**
   - Get from [DeepSeek Platform](https://platform.deepseek.com/)
   - Sign up for an account and generate API key

### Setting Credentials

**Option 1: Environment Variables (Recommended)**
```bash
# Create .env file in project root
echo "X_BEARER_TOKEN=your_x_bearer_token_here" > .env
echo "DEEPSEEK_API_KEY=your_deepseek_key_here" >> .env
```

**Option 2: Command Line Arguments**
```bash
python x_topic_analyzer.py --x-bearer-token YOUR_TOKEN --deepseek-key YOUR_KEY
```

## 📖 Usage Guide

### Testing with Mock Data (No API Keys Needed)

Run the test version to verify installation:
```bash
python test_analyzer.py
```

This will:
- Use simulated X post data
- Generate mock summaries
- Export to Excel/CSV file
- Display sample results

### Full Analysis with Real APIs

1. **Basic Usage**
   ```bash
   python x_topic_analyzer.py
   ```
   Follow prompts to enter topic and credentials.

2. **Command Line Usage**
   ```bash
   python x_topic_analyzer.py --keyword "artificial intelligence" --max-posts 25
   ```

3. **With Credentials as Arguments**
   ```bash
   python x_topic_analyzer.py \
     --keyword "machine learning" \
     --max-posts 50 \
     --x-bearer-token YOUR_X_TOKEN \
     --deepseek-key YOUR_DEEPSEEK_KEY
   ```

### Command Line Options

- `--keyword`: Topic to search for (can be omitted for interactive input)
- `--max-posts`: Maximum posts to analyze (default: 50, max: 100)
- `--x-bearer-token`: X API Bearer Token
- `--deepseek-key`: DeepSeek API Key

## 📊 Output Format

Results are saved to Excel files with the following columns:

- **Topic**: Search keyword
- **Author**: Author name and username
- **Author Verified**: Verification status
- **Post Date**: Date and time of post
- **Post Link**: Direct link to the post
- **Short Summary**: AI-generated summary
- **Original Text**: Truncated post content
- **Engagement**: Likes, retweets, replies

## 🔧 How It Works

1. **Search Phase**: Queries X API for recent posts matching the keyword
2. **Filtering**: Excludes retweets, focuses on English posts
3. **Analysis Phase**: For each post, generates AI summary using DeepSeek
4. **Processing**: Compiles metadata (author, engagement, timestamps)
5. **Export Phase**: Saves formatted results to Excel with professional styling

## 🧪 Testing

The `test_analyzer.py` provides comprehensive testing:

- ✅ No API credentials required
- ✅ Tests data processing pipeline
- ✅ Verifies Excel export functionality
- ✅ Validates mock data structure
- ✅ Checks formatting and column adjustments

Run tests regularly to ensure functionality.

## 📝 Dependencies

- `tweepy`: X API client
- `pandas`: Data manipulation
- `openpyxl`: Excel file handling
- `openai`: DeepSeek API client
- `python-dotenv`: Environment variable management
- `requests`: HTTP requests

## ⚠️ Important Notes

- **API Limits**: X API has rate limits (300 requests/15min for search)
- **Rate Limiting**: Built-in delays prevent API throttling
- **Cost**: DeepSeek API calls may incur costs based on usage
- **Data Privacy**: Respect X's terms of service and data usage policies
- **Testing First**: Always test with `test_analyzer.py` before using real APIs

## 🐛 Troubleshooting

### Common Issues

1. **"Missing API credentials"**
   - Ensure `.env` file exists with correct keys
   - Or pass credentials as command arguments

2. **"No tweets found"**
   - Try different keywords
   - Check if topic has recent activity
   - X API only returns recent posts (last 7 days)

3. **Excel export fails**
   - Ensure `openpyxl` is installed
   - Falls back to CSV if Excel unavailable

4. **API rate limits**
   - Wait 15 minutes between searches
   - Reduce `--max-posts` value

### Debug Mode

Uncomment debug prints in `x_topic_analyzer.py` to see API details:
```python
print(f"DEBUG: X_BEARER_TOKEN={os.getenv('X_BEARER_TOKEN')}")
print(f"DEBUG: DEEPSEEK_API_KEY={os.getenv('DEEPSEEK_API_KEY')}")
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Test with `test_analyzer.py`
4. Submit a pull request

## 📄 License

[Add your license information here]

## 📞 Support

For issues or questions:
- Check the troubleshooting section
- Test with mock data first
- Ensure all dependencies are installed
- Verify API credentials are correct

---

**Happy Analyzing! 🚀**
