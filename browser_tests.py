from concurrent.futures import ThreadPoolExecutor, as_completed

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import BASE_URL, BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY
from logger import log_info


def _run_single_browserstack_session(environment):
    options = Options()

    bstack_options = {
        "userName": BROWSERSTACK_USERNAME,
        "accessKey": BROWSERSTACK_ACCESS_KEY,
        "os": environment.get("os"),
        "osVersion": environment.get("osVersion"),
        "deviceName": environment.get("deviceName"),
        "sessionName": environment.get("name"),
    }

    # Remove None values so BrowserStack doesn't get invalid caps
    bstack_options = {k: v for k, v in bstack_options.items() if v is not None}

    if environment.get("browserName"):
        options.set_capability("browserName", environment["browserName"])

    options.set_capability("bstack:options", bstack_options)

    driver = webdriver.Remote(
        command_executor="https://hub.browserstack.com/wd/hub",
        options=options,
    )

    try:
        driver.get(BASE_URL)
        log_info(f"BrowserStack test successful on {environment['name']}")
    finally:
        driver.quit()


def run_browserstack_tests():
    """
    Validate the scraper target page across 5 parallel BrowserStack environments
    (mix of desktop and mobile).
    """
    environments = [
        {
            "name": "Windows 11 - Chrome",
            "os": "Windows",
            "osVersion": "11",
            "browserName": "Chrome",
            "deviceName": None,
        },
        {
            "name": "macOS Sonoma - Safari",
            "os": "OS X",
            "osVersion": "Sonoma",
            "browserName": "Safari",
            "deviceName": None,
        },
        {
            "name": "iPhone 14 - Safari",
            "os": None,
            "osVersion": None,
            "browserName": "Safari",
            "deviceName": "iPhone 14",
        },
        {
            "name": "Samsung Galaxy S22 - Chrome",
            "os": None,
            "osVersion": None,
            "browserName": "Chrome",
            "deviceName": "Samsung Galaxy S22",
        },
        {
            "name": "iPad 9th - Safari",
            "os": None,
            "osVersion": None,
            "browserName": "Safari",
            "deviceName": "iPad 9th",
        },
    ]

    with ThreadPoolExecutor(max_workers=len(environments)) as executor:
        futures = {
            executor.submit(_run_single_browserstack_session, env): env
            for env in environments
        }

        for future in as_completed(futures):
            env = futures[future]
            try:
                future.result()
            except Exception as exc:
                log_info(
                    f"BrowserStack test failed on {env['name']}: {exc}"
                )