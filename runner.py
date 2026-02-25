import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions

from config import BS_HUB_URL
from scraper import scrape_articles


# Environments Testing
ENVIRONMENTS = [
    {
        "label": "Chrome · Windows 11",
        "browserName": "Chrome",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "11",
            "sessionName": "ElPais_Chrome_Win11",
        },
    },
    {
        "label": "Firefox · Windows 10",
        "browserName": "Firefox",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "10",
            "sessionName": "ElPais_Firefox_Win10",
        },
    },
    {
        "label": "Safari · macOS Sonoma",
        "browserName": "Safari",
        "browserVersion": "17",
        "bstack:options": {
            "os": "OS X",
            "osVersion": "Sonoma",
            "sessionName": "ElPais_Safari_Sonoma",
        },
    },
    {
        "label": "iPhone 15 · Mobile Safari",
        "browserName": "safari",
        "bstack:options": {
            "deviceName": "iPhone 15",
            "osVersion": "17",
            "realMobile": "true",
            "sessionName": "ElPais_iPhone15",
        },
    },
    {
        "label": "Samsung Galaxy S23 · Chrome Mobile",
        "browserName": "chrome",
        "bstack:options": {
            "deviceName": "Samsung Galaxy S23",
            "osVersion": "13.0",
            "realMobile": "true",
            "sessionName": "ElPais_GalaxyS23",
        },
    },
]


def _build_driver(caps: dict):
    browser = caps.get("browserName", "").lower()

    if "firefox" in browser:
        options = FirefoxOptions()
    elif "safari" in browser:
        options = SafariOptions()
    else:
        options = ChromeOptions()

    for key, value in caps.items():
        if key != "label":
            options.set_capability(key, value)

    return webdriver.Remote(command_executor=BS_HUB_URL, options=options)


def _run_single(caps: dict) -> str:
    label = caps.get("label", caps.get("browserName", "unknown"))
    driver = None
    try:
        driver = _build_driver(caps)
        articles = scrape_articles(driver, env=label)
        status_msg = f"Scraped {len(articles)} articles"
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": '
            f'{{"status": "passed", "reason": "{status_msg}"}}}}'
        )
        logging.info(f"[{label}] PASSED — {status_msg}")
        return f"PASSED: {label}"
    except Exception as exc:
        reason = str(exc)[:120].replace('"', "'")
        logging.error(f"[{label}] FAILED — {exc}")
        if driver:
            driver.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", "arguments": '
                f'{{"status": "failed", "reason": "{reason}"}}}}'
            )
        return f"FAILED: {label}"
    finally:
        if driver:
            driver.quit()


def run_parallel(max_workers: int = 5) -> list[str]:
    logging.info(
        f"\n+---BrowserStack: starting {len(ENVIRONMENTS)} parallel sessions---+"
    )
    results: list[str] = []

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(_run_single, caps): caps["label"] for caps in ENVIRONMENTS}
        for future in as_completed(futures):
            results.append(future.result())

    logging.info("\n+---BrowserStack Results---+")
    for r in results:
        logging.info(f"  {r}")
    logging.info("View dashboard : https://automate.browserstack.com/dashboard")

    return results

