"""
Bot that keeps the profile README "alive".

What it does every time it runs (once a day via GitHub Actions):
1. Pulls a random recent AI/ML paper title + authors from the arXiv API.
2. Picks a random quote from a small local pool.
3. Writes both into the README between the
   <!--START_SECTION:live--> ... <!--END_SECTION:live--> markers.

No API keys required — arXiv's API is public.
"""

import random
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

README_PATH = "README.md"
START_MARKER = "<!--START_SECTION:live-->"
END_MARKER = "<!--END_SECTION:live-->"

ARXIV_CATEGORIES = ["cs.LG", "cs.AI", "cs.CL", "cs.CV"]

QUOTES = [
    "The question of whether a computer can think is no more interesting than the question of whether a submarine can swim. — Edsger Dijkstra",
    "In God we trust, all others bring data. — W. Edwards Deming",
    "A model is a lie that helps you see the truth. — Howard Skipper (paraphrased)",
    "It's not who has the best algorithm that wins, it's who has the most data. — Andrew Ng",
    "Machine learning is the last invention humanity will ever need to make. — Nick Bostrom",
    "The best way to predict the future is to invent it. — Alan Kay",
]


def fetch_random_paper() -> str:
    category = random.choice(ARXIV_CATEGORIES)
    url = (
        "http://export.arxiv.org/api/query?"
        f"search_query=cat:{category}&sortBy=submittedDate&sortOrder=descending"
        "&start=0&max_results=25"
    )
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = resp.read()
        root = ET.fromstring(data)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entries = root.findall("atom:entry", ns)
        if not entries:
            return "No paper found today — arXiv might be napping."
        entry = random.choice(entries)
        title = entry.find("atom:title", ns).text.strip().replace("\n", " ")
        link = entry.find("atom:id", ns).text.strip()
        authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]
        author_str = authors[0] + (" et al." if len(authors) > 1 else "")
        return f"**{title}** — *{author_str}* ([link]({link}))"
    except Exception as e:
        return f"Couldn't reach arXiv today ({e}) — check back tomorrow."


def build_section() -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    paper = fetch_random_paper()
    quote = random.choice(QUOTES)
    return (
        f"📅 **{today} (UTC)**\n\n"
        f"📄 Today's random paper from arXiv:\n> {paper}\n\n"
        f"💬 Quote of the day:\n> {quote}\n"
    )


def update_readme() -> None:
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    new_section = build_section()
    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER), re.DOTALL
    )
    replacement = f"{START_MARKER}\n{new_section}\n{END_MARKER}"

    if pattern.search(content):
        content = pattern.sub(replacement, content)
    else:
        content += f"\n\n{replacement}\n"

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    update_readme()
    print("README live section updated.")
