# -*- coding: utf-8 -*-
"""Audit numeric tokens in shoulder-atlas against verified evidence files."""
import pathlib, re, sys, yaml
from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parent.parent
EVIDENCE_PATHS = [
    pathlib.Path(r"C:\Users\ahmed\OneDrive\Desktop\shoulder_evidence_verified.md"),
    pathlib.Path(r"C:\Users\ahmed\OneDrive\Desktop\upgrade_evidence_verified.md"),
]
PAGES_DIR = ROOT / "src" / "pages"
YAML_PATH = ROOT / "atlas" / "data" / "tests.yaml"

WHITELIST_RULES = [
    (
        "Nerve root / spinal level names (C4-T1)",
        re.compile(r"\b(?:C[4-8]|T1)(?:\s*[\-\u2013\u2014/]\s*(?:C[4-8]|T1|[4-8]))*\b"),
    ),
    (
        "Calculator scoring rules & scales (SPADI, WORC, ASES, SIRSI, QuickDASH, NPRS, PSFS, HHD)",
        re.compile(
            r"(?<![\d.])(?:0[\-\u2013]100%?|0[\-\u2013]50|0[\-\u2013]10|1[\-\u2013]5|"
            r"13\s+items|11\s+items|5\s+pain\s+items|8\s+disability\s+items|"
            r"\u00f7\s*2|\u00f7\s*11|\u00f7\s*8|\u00d7\s*25|\u00d7\s*100|cm\s*\u00f7\s*100)(?![\d.])"
        ),
    ),
    (
        "Visit / week numbers in log tables (1-12, Phase I-IV)",
        re.compile(r"\b(?:1[0-2]|[1-9])\b"),
    ),
    (
        "Page numbers (1-9, p1-p9)",
        re.compile(r"\b(?:p[1-9]|page\s*[1-9]|[1-9]\s*/\s*9)\b", re.IGNORECASE),
    ),
]

NUM_PATTERN = re.compile(r"(?<![A-Za-z0-9_])(?:\d+(?:\.\d+)?|\.\d+)(?![A-Za-z0-9_])")

def normalise_number(n: str) -> str:
    if "." in n:
        n = n.rstrip("0").rstrip(".")
    return n

def load_verified_numbers(paths: list[pathlib.Path]) -> set[str]:
    tokens = set()
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for match in NUM_PATTERN.finditer(text):
            tokens.add(normalise_number(match.group(0)))
    return tokens

def is_whitelisted(text_context: str, num_str: str) -> str | None:
    for label, pattern in WHITELIST_RULES:
        for m in pattern.finditer(text_context):
            if num_str in m.group(0):
                return label
    return None

def audit_file_content(content: str, label: str, verified_nums: set[str], unverified: list, whitelist_counts: dict):
    # Strip HTML tags
    soup = BeautifulSoup(content, "html.parser")
    # Also include svg text elements
    text = soup.get_text(separator=" ")
    for m in NUM_PATTERN.finditer(text):
        raw = m.group(0)
        norm = normalise_number(raw)
        if norm in verified_nums:
            continue
        start = max(0, m.start() - 30)
        end = min(len(text), m.end() + 30)
        context = text[start:end]
        wl = is_whitelisted(context, raw)
        if wl:
            whitelist_counts[wl] = whitelist_counts.get(wl, 0) + 1
        else:
            unverified.append((label, raw, context.replace("\n", " ").strip()))

def main() -> int:
    verified_nums = load_verified_numbers(EVIDENCE_PATHS)
    whitelist_counts: dict[str, int] = {label: 0 for label, _ in WHITELIST_RULES}
    unverified: list[tuple[str, str, str]] = []

    # 1. Audit pages
    page_files = sorted(PAGES_DIR.glob("p*.html"))
    for pf in page_files:
        content = pf.read_text(encoding="utf-8")
        audit_file_content(content, pf.name, verified_nums, unverified, whitelist_counts)

    # 2. Audit YAML
    if YAML_PATH.exists():
        with open(YAML_PATH, "r", encoding="utf-8") as f:
            cards = yaml.safe_load(f) or []
        for card in cards:
            cid = card.get("id", "unknown")
            for field in ["metrics", "interpretation", "summary", "positive", "steps"]:
                val = card.get(field)
                if not val:
                    continue
                if isinstance(val, list):
                    val = " ".join(str(x) for x in val)
                audit_file_content(str(val), f"card:{cid}:{field}", verified_nums, unverified, whitelist_counts)

    print("=" * 72)
    print("SHOULDER DOSSIER + ATLAS NUMBER AUDIT (Rule 2.10 & Section 6.3)")
    print("=" * 72)
    print("Evidence sources:")
    for ep in EVIDENCE_PATHS:
        print(f"  - {ep}")
    print(f"Verified tokens : {len(verified_nums)} distinct numeric values across 2 evidence files")
    print(f"Pages audited   : {len(page_files)} files")
    print(f"YAML audited    : {len(cards) if YAML_PATH.exists() else 0} cards")
    print("-" * 72)
    print("Rule 2.10 Whitelist Applied:")
    for label, _ in WHITELIST_RULES:
        print(f"  - {label}: {whitelist_counts.get(label, 0)} matches")
    print("-" * 72)

    if unverified:
        print(f"UNVERIFIED NUMBERS FOUND: {len(unverified)}")
        for source, num, ctx in unverified[:40]:
            print(f"  [!] {source}: '{num}' in ...{ctx}...")
        if len(unverified) > 40:
            print(f"  ... and {len(unverified) - 40} more")
        print(f"\nSTATUS: FAIL ({len(unverified)} unverified numbers)")
        return 1
    else:
        print("Unverified numbers count: 0")
        print("STATUS: PASS (0 unverified numbers)")
        return 0

if __name__ == "__main__":
    sys.exit(main())
