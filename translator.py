import time
import requests
from utils import log_info
from config import RAPIDAPI_KEY, RAPIDAPI_HOST

# When the RapidAPI subscription is missing the service returns
# "You are not subscribed to this API." — cache that state so we
# avoid repeatedly calling the API and flooding the logs.
_translation_disabled = False


def translate_text(text):
    """
    Translate Spanish text to English using the configured RapidAPI host.
    Falls back to the original text if the API errors or rate limits.
    """
    # Build URL from configured host – this API expects /translate
    # rather than the Google Cloud /language/translate/v2 path.
    url = f"https://{RAPIDAPI_HOST}/translate"

    payload = {
        "q": text,
        "target": "en",
        "source": "es",
    }

    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST,
    }

    global _translation_disabled

    # If we previously detected an unsubscribed account, skip calls.
    if _translation_disabled:
        log_info("Translation skipped: API not subscribed")
        return text

    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        data = response.json()
        log_info(f"API RESPONSE: {data}")

        # Explicitly handle common error shape from RapidAPI
        if isinstance(data, dict) and "message" in data:
            msg = data.get("message", "")
            log_info(f"Translation API error message: {msg}")
            # If the account is not subscribed, disable further calls.
            lower = msg.lower()
            if "not subscribed" in lower:
                _translation_disabled = True
                log_info("Disabling translation API calls: not subscribed to API")
                return text
            # If the configured host does not expose the expected path,
            # disable calls to avoid repeated "Endpoint '/translate' does not exist" logs.
            if "endpoint" in lower and "does not exist" in lower:
                _translation_disabled = True
                log_info("Disabling translation API calls: endpoint does not exist on host")
                return text
            # If rate limited, wait a bit and return original text
            if "Too many requests" in msg:
                time.sleep(1)
            return text

        # Proper structure check for successful translation
        if "data" in data and "translations" in data["data"]:
            translations = data["data"]["translations"]
            if translations:
                translated = translations[0].get("translatedText", text)
                log_info(f"[ENGLISH TITLE]: {translated}")
                return translated

        # Fallback if structure is not as expected
        log_info(f"Translation API returned unexpected structure: {data}")
        return text

    except Exception as e:
        log_info(f"Translation error: {e}")
        return text