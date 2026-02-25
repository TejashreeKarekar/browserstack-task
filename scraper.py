import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from config import BASE_URL, ARTICLE_LIMIT
from utils import log_info, ensure_dir


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    log_info("Initializing Chrome driver...")
    driver = webdriver.Chrome(options=options)
    # Defensive timeouts so we don't hang forever on slow pages
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(5)
    log_info("Chrome driver initialized.")
    return driver


def scrape_articles_local():
    log_info("Running locally...")

    driver = setup_driver()
    log_info(f"Opening base URL: {BASE_URL}")
    try:
        driver.get(BASE_URL)
    except Exception as e:
        log_info(f"Error loading BASE_URL: {e}")
        driver.quit()
        return []

    # ✅ Scroll and collect dynamic article links
    links = set()

    # Scroll a finite number of times to avoid hanging
    max_scrolls = 15
    scroll_count = 0

    while len(links) < ARTICLE_LIMIT and scroll_count < max_scrolls:
        scroll_count += 1
        log_info(f"Scroll iteration {scroll_count}, current opinion links: {len(links)}")
        elements = driver.find_elements(By.CSS_SELECTOR, "h2 a")

        for el in elements:
            href = el.get_attribute("href")
            # Only keep opinion articles
            if href and "elpais.com/opinion/" in href:
                links.add(href)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    links = list(links)
    # Preserve only unique links in the order collected
    seen = set()
    ordered_links = []
    for link in links:
        if link not in seen:
            seen.add(link)
            ordered_links.append(link)

    links = ordered_links[:ARTICLE_LIMIT]
    log_info(f"Collected Links: {links}")

    # Reuse cookies from Selenium session for HTTP requests
    cookies = driver.get_cookies()
    driver.quit()

    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie["name"], cookie["value"])

    articles = []

    for index, link in enumerate(links, start=1):
        try:
            image_url = None
            image_path = None

            resp = session.get(link, timeout=20)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "html.parser")

            # Title via BeautifulSoup
            title_tag = soup.find("h1")
            title = title_tag.get_text(strip=True) if title_tag else "Title not found"

            # Article body via main opinion body selector
            body_container = soup.select_one("div[data-dtm-region='articulo_cuerpo']")
            paragraphs = body_container.find_all("p") if body_container else []
            content_parts = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]

            # Fallback: any <article> paragraphs
            if not content_parts:
                fallback_paragraphs = soup.select("article p")
                content_parts = [p.get_text(strip=True) for p in fallback_paragraphs if p.get_text(strip=True)]

            content = "\n\n".join(content_parts) if content_parts else "Content not found"

            log_info(f"\n[LOCAL] --- Article {index} ---")
            log_info(f"[LOCAL] Title (Spanish): {title}")
            log_info(f"[LOCAL] Content (Spanish):\n{content}")
            log_info("[LOCAL]================================================================================")

            # Extract cover image via BeautifulSoup
            try:
                img_tag = soup.select_one("figure img")
                if img_tag:
                    src = img_tag.get("src")
                    if src and src.startswith("http"):
                        image_url = src

                        images_dir = os.path.join("output", "images")
                        ensure_dir(images_dir)

                        img_response = session.get(image_url, timeout=20)
                        img_response.raise_for_status()

                        image_path = os.path.join(images_dir, f"article_{index}.jpg")
                        with open(image_path, "wb") as f:
                            f.write(img_response.content)

                        log_info(f"[LOCAL] Image saved: {image_path}")
                else:
                    log_info("[LOCAL] No valid article image found")
            except Exception as e:
                log_info(f"[LOCAL] Image error: {e}")

            articles.append(
                {
                    "title": title,
                    "url": link,
                    "body": content,
                    "image_url": image_url,
                    "image_path": image_path,
                }
            )

        except Exception as e:
            log_info(f"Article processing error for {link}: {e}")
            continue

    return articles


def scrape_articles(driver, env: str | None = None):
    """
    Lightweight scraper used in BrowserStack environments.
    Uses the provided WebDriver to open BASE_URL and return
    a minimal list of discovered article links.
    """
    log_info(f"[BSTACK] ({env}) Opening {BASE_URL}")
    driver.get(BASE_URL)
    driver.implicitly_wait(5)

    elements = driver.find_elements(By.CSS_SELECTOR, "h2 a")
    links: list[str] = []
    for el in elements:
        href = el.get_attribute("href")
        if href and "elpais.com/opinion/" in href:
            links.append(href)

    unique_links = []
    seen = set()
    for link in links:
        if link not in seen:
            seen.add(link)
            unique_links.append(link)

    limited = unique_links[:ARTICLE_LIMIT]
    log_info(f"[BSTACK] ({env}) Found {len(limited)} opinion links")
    return [{"url": link} for link in limited]