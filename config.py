import os
from dotenv import load_dotenv

load_dotenv()

# EL PAÍS Opinion URL
BASE_URL = "https://elpais.com/opinion/"

# RapidAPI Google Translate
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", " 7df97c3e09msh815f5bf8aacb18ep175d2djsnf96dfe2d8d47")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "deep-translate1.p.rapidapi.com")

# BrowserStack Credentials
BROWSERSTACK_USERNAME = os.getenv("BROWSERSTACK_USERNAME", "tejashreekarekar_8UryMB")
BROWSERSTACK_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY", "aH4DZxWxZutozPt6Aujq")
BS_HUB_URL = (
    f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}"
    "@hub.browserstack.com/wd/hub"
)

# Logging
LOG_FILE = os.getenv("LOG_FILE", "output/output.log")

# Number of articles
ARTICLE_LIMIT = 5