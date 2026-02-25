import json
import os
from datetime import datetime
from typing import Any, Dict, List

from utils import ensure_dir, log_info


def generate_report(articles: List[Dict[str, Any]], repeated_words: Dict[str, int]) -> str:
    """
    Build and save a timestamped JSON report under output/reports/.
    Returns the path to the created report file.
    """
    reports_dir = os.path.join("output", "reports")
    ensure_dir(reports_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(reports_dir, f"articles_{timestamp}.json")

    result = {
        "generated_at": timestamp,
        "repeated_words": repeated_words,
        "articles": articles,
    }

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    log_info(f"Articles JSON saved to {report_path}")
    return report_path


