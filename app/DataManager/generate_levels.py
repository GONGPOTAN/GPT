import os
import json
from config.symbols import SYMBOLS
from app.analyzer.analyzer import analyze_all

def generate_levels_from_analyzer():
    analysis_results = analyze_all()
    for result in analysis_results:
        market_type = result["market_type"]
        symbol = result["symbol"]
        strong_levels = result["result"].get("strong", [])
        weak_levels = result["result"].get("weak", [])

        base_dir = f"data/levels/{market_type}"
        os.makedirs(base_dir, exist_ok=True)
        file_path = os.path.join(base_dir, f"{symbol}.json")

        levels = {"strong": strong_levels, "weak": weak_levels}
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(levels, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generate_levels_from_analyzer()
