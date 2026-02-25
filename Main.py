from scraper import scrape_articles_local
from translator import translate_text
from analyzer import analyze_titles
from reporter import generate_report
from runner import run_parallel
from utils import setup_logger, log_info


def main():
    setup_logger()

    # Step 1: Scrape opinion articles (title, body, image)
    articles = scrape_articles_local()

    # Step 2: Translate titles and attach to articles
    for article in articles:
        translated = translate_text(article["title"])
        article["translated_title"] = translated

    translated_titles = [article["translated_title"] for article in articles]

    # Step 3: Analyze repeated words
    repeated_words = analyze_titles(translated_titles)
    log_info(f"Repeated words (English titles): {repeated_words}")

    # Step 4: Generate timestamped JSON report
    report_path = generate_report(articles, repeated_words)
    log_info(f"Report generated at {report_path}")

    # Step 5: Parallel cross-browser validation via BrowserStack
    run_parallel()

    log_info("Task Completed Successfully")


if __name__ == "__main__":
    main()