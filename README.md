# browserstack-task
# El País Opinion Scraper & Cross-Browser Validator

A Python-based web scraping and automated testing suite that extracts Spanish opinion articles from **El País**, translates titles to English, analyzes text patterns, and validates content across multiple browsers using BrowserStack.

## 📋 Overview

This project performs a multi-stage workflow:

1. **Scrape** – Extracts opinion articles (titles, body text, images) from [El País Opinion](https://elpais.com/opinion/)
2. **Translate** – Converts Spanish titles to English via RapidAPI's Google Translate
3. **Analyze** – Identifies repeated words and linguistic patterns in translated titles
4. **Report** – Generates timestamped JSON reports with article metadata
5. **Cross-Browser Test** – Validates articles across Chrome, Firefox, Safari, and Edge on BrowserStack

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Chrome WebDriver** (included in `chromedriver-win64/`)
- **RapidAPI Key** (for translation)
- **BrowserStack Credentials** (for cross-browser testing)

### Installation

1. Clone or navigate to the project directory:
   ```bash
   cd browserstack
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables (create `.env` or update `config.py`):
   ```env
   RAPIDAPI_KEY=your_rapidapi_key_here
   RAPIDAPI_HOST=deep-translate1.p.rapidapi.com
   BROWSERSTACK_USERNAME=your_browserstack_username
   BROWSERSTACK_ACCESS_KEY=your_browserstack_access_key
   LOG_FILE=output/output.log
   ```

### Run the Full Pipeline

```bash
python Main.py
```

This executes all stages: scraping, translation, analysis, reporting, and cross-browser testing.

## 📁 Project Structure

```
browserstack/
├── Main.py                    # Main orchestration script
├── scraper.py                 # Web scraping (Selenium + BeautifulSoup)
├── translator.py              # Title translation via RapidAPI
├── analyzer.py                # Text pattern analysis
├── reporter.py                # JSON report generation
├── runner.py                  # BrowserStack cross-browser testing
├── config.py                  # Configuration & environment variables
├── utils.py                   # Logging utilities
├── browser_tests.py           # Individual browser test logic
├── requirements.txt           # Python dependencies
├── chromedriver-win64/        # Chrome WebDriver binary
├── output/
│   ├── images/                # Downloaded article images
│   ├── reports/               # Generated JSON reports (timestamped)
│   └── output.log             # Application logs
└── README.md                  # This file
```


## 📊 Output & Reports

### Images
Downloaded article images are stored in `output/images/` with naming convention `article_N.jpg`.

### Reports
Generated reports are timestamped JSON files in `output/reports/`:
```json
{
  "generated_at": "20260225_223651",
  "repeated_words": {
    "word1": 3,
    "word2": 2
  },
  "articles": [
    {
      "title": "Spanish Title",
      "translated_title": "English Title",
      "body": "Article body text...",
      "image_url": "...",
      "image_path": "output/images/article_1.jpg"
    }
  ]
}

## 🌐 Supported Browsers (BrowserStack)

- **Chrome** (latest) on Windows 11
- **Firefox** (latest) on Windows 10
- **Safari** (latest) on macOS 14
- **Edge** (latest) on Windows 11

## 📦 Dependencies

See `requirements.txt`:
- **selenium** – WebDriver automation
- **requests** – HTTP requests for APIs
- **beautifulsoup4** – HTML parsing
- **python-dotenv** – Environment variable management

