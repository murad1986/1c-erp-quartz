#!/usr/bin/env python3
"""Fix all broken links in Quartz site content."""
import re
from pathlib import Path

content = Path("/Users/muradnurmagomedov/1c-erp-fresh/content")

changes_total = 0


def fix_file(path, replacements):
    """Apply list of (old, new) replacements to a file."""
    global changes_total
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in replacements:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        count = sum(1 for old, new in replacements if old in original)
        print(f"  Fixed {path.relative_to(content)}")
        changes_total += 1
    return text != original


# ============================================================
# CATEGORY 1: Python relative .md navigation links (weeks 3-10)
# Fix (day_N.md) -> (/python/week_X/day_N/) and (../week_M/day_N.md) -> (/python/week_M/day_N/)
# ============================================================
print("\n=== Category 1: Python relative .md links ===")

for week_num in range(3, 11):
    week_dir = content / "python" / f"week_{week_num}"
    for day_num in range(1, 8):
        md_file = week_dir / f"day_{day_num}.md"
        if not md_file.exists():
            continue

        text = md_file.read_text(encoding="utf-8")
        original = text

        # Fix same-week relative links: (day_N.md) -> (/python/week_X/day_N/)
        for d in range(1, 8):
            text = text.replace(f"(day_{d}.md)", f"(/python/week_{week_num}/day_{d}/)")

        # Fix cross-week relative links: (../week_M/day_N.md) -> (/python/week_M/day_N/)
        for w in range(1, 11):
            for d in range(1, 8):
                text = text.replace(
                    f"(../week_{w}/day_{d}.md)", f"(/python/week_{w}/day_{d}/)"
                )

        if text != original:
            md_file.write_text(text, encoding="utf-8")
            print(f"  Fixed python/week_{week_num}/day_{day_num}.md")
            changes_total += 1

# Fix cross-week wikilinks like [[week_2/day_7|text]] in python files
# These generate slugs like /week_2/day_7 - convert to absolute markdown links
print("\n=== Category 1b: Python wikilink cross-week ===")

for week_num in range(3, 11):
    week_dir = content / "python" / f"week_{week_num}"
    for day_num in range(1, 8):
        md_file = week_dir / f"day_{day_num}.md"
        if not md_file.exists():
            continue

        text = md_file.read_text(encoding="utf-8")
        original = text

        # Fix [[week_M/day_N|text]] -> [text](/python/week_M/day_N/)
        pattern = r'\[\[week_(\d+)/day_(\d+)\|([^\]]+)\]\]'
        text = re.sub(
            pattern,
            lambda m: f"[{m.group(3)}](/python/week_{m.group(1)}/day_{m.group(2)}/)",
            text
        )
        # Also fix [[week_M/day_N]] without pipe
        pattern2 = r'\[\[week_(\d+)/day_(\d+)\]\]'
        text = re.sub(
            pattern2,
            lambda m: f"[week_{m.group(1)}/day_{m.group(2)}](/python/week_{m.group(1)}/day_{m.group(2)}/)",
            text
        )

        if text != original:
            md_file.write_text(text, encoding="utf-8")
            print(f"  Fixed python/week_{week_num}/day_{day_num}.md (wikilink)")
            changes_total += 1

# Fix absolute paths missing /python/ prefix in week_5 files
# /week_4/day_7 -> /python/week_4/day_7/ etc.
print("\n=== Category 1c: Python absolute paths missing /python/ prefix ===")

for week_num in range(3, 11):
    week_dir = content / "python" / f"week_{week_num}"
    for day_num in range(1, 8):
        md_file = week_dir / f"day_{day_num}.md"
        if not md_file.exists():
            continue

        text = md_file.read_text(encoding="utf-8")
        original = text

        # Fix (/week_M/day_N) -> (/python/week_M/day_N/)
        # But only for links that don't already have /python/ prefix
        for w in range(1, 11):
            for d in range(1, 8):
                # In markdown link: (/week_M/day_N)
                text = text.replace(f"(/week_{w}/day_{d})", f"(/python/week_{w}/day_{d}/)")
                # Also without trailing /
                text = text.replace(f"(/week_{w}/day_{d}/)", f"(/python/week_{w}/day_{d}/)")

        if text != original:
            md_file.write_text(text, encoding="utf-8")
            print(f"  Fixed python/week_{week_num}/day_{day_num}.md (abs path)")
            changes_total += 1

# ============================================================
# Also fix python/week_2 nav bars that reference Week 1/3 named files
# Week 2 files have wikilinks like [[Week 1 - Day 7 - Rest\|...]] and [[Week 3 - Day 1 - Dict Basics\|...]]
# These should become proper links
# ============================================================
print("\n=== Category 1d: Python week_2 nav wikilinks to week_1/week_3 named files ===")

# Week 1 and 2 have named files like "Week 1 - Day 7 - Rest.md"
# Week 3 onwards have day_N.md files
# The wikilinks from week_2 files: [[Week 1 - Day 7 - Rest\|text]] -> already working since file exists
# But [[Week 3 - Day 1 - Dict Basics\|text]] -> file is day_1.md not "Week 3 - Day 1 - Dict Basics.md"
# So fix: [[Week 3 - Day 1 - Dict Basics\|text]] -> [text](/python/week_3/day_1/)
week2_dir = content / "python" / "week_2"
for md_file in week2_dir.glob("*.md"):
    text = md_file.read_text(encoding="utf-8")
    original = text

    # Fix [[Week 3 - Day 1 - Dict Basics\|text]] -> [text](/python/week_3/day_1/)
    text = re.sub(
        r'\[\[Week 3 - Day 1 - Dict Basics\\?\|([^\]]+)\]\]',
        r'[\1](/python/week_3/day_1/)',
        text
    )
    # Also fix prerequisites field which uses double-quotes
    text = re.sub(
        r'"?\[\[Week 3 - Day 1 - Dict Basics\]\]"?',
        '"[week_3/day_1](/python/week_3/day_1/)"',
        text
    )

    if text != original:
        md_file.write_text(text, encoding="utf-8")
        print(f"  Fixed python/week_2/{md_file.name}")
        changes_total += 1

# Fix [[Week 1 - Day 7 - Rest\|text]] in week_2 - this file EXISTS as "Week 1 - Day 7 - Rest.md"
# So actually that wikilink should work. Let's verify by checking broken links list:
# /Week-1---Day-7---Rest broken from python/week_2/Week-2---Day-1---List-Basics.html
# So it IS broken. Fix it:
week2_day1 = content / "python" / "week_2" / "Week 2 - Day 1 - List Basics.md"
if week2_day1.exists():
    text = week2_day1.read_text(encoding="utf-8")
    original = text
    # Fix [[Week 1 - Day 7 - Rest\|text]] -> [text](/python/week_1/Week 1 - Day 7 - Rest/)
    # The actual URL would be /python/week_1/Week-1---Day-7---Rest/
    text = re.sub(
        r'\[\[Week 1 - Day 7 - Rest\\?\|([^\]]+)\]\]',
        r'[\1](/python/week_1/Week%201%20-%20Day%207%20-%20Rest/)',
        text
    )
    # Also fix prerequisites
    text = text.replace(
        '"[[Week 1 - Day 7 - Rest]]"',
        '"[Week 1 - Day 7 - Rest](/python/week_1/Week%201%20-%20Day%207%20-%20Rest/)"'
    )
    if text != original:
        week2_day1.write_text(text, encoding="utf-8")
        print(f"  Fixed python/week_2/Week 2 - Day 1 - List Basics.md (Week 1 Rest link)")
        changes_total += 1

# Fix /Week-2---Day-7---Rest broken from week_2/Week-2---Day-6
# Already in the file as [[Week 2 - Day 7 - Rest\|...]] which should work since file exists
# But it's showing broken. Let's check...

# ============================================================
# CATEGORY 2: README/course links in navigation bars
# ============================================================
print("\n=== Category 2: README/course links ===")

# Build mapping: course folder -> correct README link
course_readme_map = {
    "retail_finance/README": "[Оглавление](/retail-finance/)",
    "python_basics/README": "[Оглавление](/python/)",
    "1c_erp_qcom/README": "[Оглавление](/1c-erp/)",
    "value_stream_mapping/README": "[Оглавление](/vsm/)",
}

# Fix [[course/README|Оглавление]] and [[course/README\|Оглавление]]
def fix_readme_links(file_path, course_prefix):
    global changes_total
    text = file_path.read_text(encoding="utf-8")
    original = text

    for old_prefix, new_link in course_readme_map.items():
        # Fix [[prefix|Оглавление]] and [[prefix\|Оглавление]] patterns
        text = text.replace(f"[[{old_prefix}|Оглавление]]", new_link)
        text = text.replace(f"[[{old_prefix}\\|Оглавление]]", new_link)
        # Also fix in frontmatter course field
        text = text.replace(f"[[{old_prefix}]]", f"[Оглавление](/{old_prefix.split('/')[0].replace('_', '-').replace('1c-erp-qcom', '1c-erp').replace('retail-finance', 'retail-finance').replace('python-basics', 'python').replace('value-stream-mapping', 'vsm')}/)")

    # Fix [[README|Оглавление]] and [[README\|Оглавление]] (bare README, need course context)
    text = text.replace("[[README|Оглавление]]", f"[Оглавление](/{course_prefix}/)")
    text = text.replace("[[README\\|Оглавление]]", f"[Оглавление](/{course_prefix}/)")

    if text != original:
        file_path.write_text(text, encoding="utf-8")
        print(f"  Fixed {file_path.relative_to(content)}")
        changes_total += 1


# Process all courses
course_dirs = {
    "1c-erp": "1c-erp",
    "retail-finance": "retail-finance",
    "python": "python",
    "vsm": "vsm",
}

for course_folder, course_url in course_dirs.items():
    course_path = content / course_folder
    for md_file in course_path.rglob("*.md"):
        fix_readme_links(md_file, course_url)

# ============================================================
# CATEGORY 3: Retail Finance colon-title wikilinks
# [[Week N - Day M: Russian title]] -> [Russian title](/retail-finance/week_N/Week N - Day M - English Name/)
# ============================================================
print("\n=== Category 3: Retail Finance colon-title wikilinks ===")

# Build mapping from broken slug patterns to correct paths
# Based on actual files in week_4, week_5, week_6
rf_mapping = {
    # Week 4
    r'Week 4 - Day 1[: ][^\]|]*': 'retail-finance/week_4/Week 4 - Day 1 - Budgeting vs Forecasting',
    r'Week 4 - Day 2[: ][^\]|]*': 'retail-finance/week_4/Week 4 - Day 2 - Sensitivity Analysis',
    r'Week 4 - Day 3[: ][^\]|]*': 'retail-finance/week_4/Week 4 - Day 3 - Valuation Basics',
    r'Week 4 - Day 4[: ][^\]|]*': 'retail-finance/week_4/Week 4 - Day 4 - Final Project Strategy',
    r'Week 4 - Day 5[: ][^\]|]*': 'retail-finance/week_4/Week 4 - Day 5 - Project Presentation',
    r'Week 4 - Day 6[: ][^\]|]*': 'retail-finance/week_4/Week 4 - Day 6 - Final Exam',
    r'Week 4 - Day 7[: ][^\]|]*': 'retail-finance/week_4/Week 4 - Day 7 - Graduation Part 1',
    # Week 5
    r'Week 5 - Day 1[: ][^\]|]*': 'retail-finance/week_5/Week 5 - Day 1 - Intro to TOC Cost vs Throughput',
    r'Week 5 - Day 2[: ][^\]|]*': 'retail-finance/week_5/Week 5 - Day 2 - TOC Metrics T I OE',
    r'Week 5 - Day 3[: ][^\]|]*': 'retail-finance/week_5/Week 5 - Day 3 - Inventory as Liability',
    r'Week 5 - Day 4[: ][^\]|]*': 'retail-finance/week_5/Week 5 - Day 4 - Bullwhip Effect',
    r'Week 5 - Day 5[: ][^\]|]*': 'retail-finance/week_5/Week 5 - Day 5 - Retailer Dilemma Cloud',
    r'Week 5 - Day 6[: ][^\]|]*': 'retail-finance/week_5/Week 5 - Day 6 - PL Analysis TOC',
    r'Week 5 - Day 7[: ][^\]|]*': 'retail-finance/week_5/Week 5 - Day 7 - Rest',
    # Week 6
    r'Week 6 - Day 1[: ][^\]|]*': 'retail-finance/week_6/Week 6 - Day 1 - DBM Dynamic Buffer Management',
    r'Week 6 - Day 2[: ][^\]|]*': 'retail-finance/week_6/Week 6 - Day 2 - Pull Replenishment',
    r'Week 6 - Day 3[: ][^\]|]*': 'retail-finance/week_6/Week 6 - Day 3 - MTA vs MTO',
    r'Week 6 - Day 4[: ][^\]|]*': 'retail-finance/week_6/Week 6 - Day 4 - Mafia Offer',
    r'Week 6 - Day 5[: ][^\]|]*': 'retail-finance/week_6/Week 6 - Day 5 - Viable Vision Strategy',
    r'Week 6 - Day 6[: ][^\]|]*': 'retail-finance/week_6/Week 6 - Day 6 - Final TOC Exam',
    r'Week 6 - Day 7[: ][^\]|]*': 'retail-finance/week_6/Week 6 - Day 7 - Grand Finale',
}

rf_path = content / "retail-finance"
for md_file in rf_path.rglob("*.md"):
    text = md_file.read_text(encoding="utf-8")
    original = text

    # Fix [[Week N - Day M: Russian title]] -> [Russian title](/retail-finance/week_N/...)
    # Pattern: [[Week N - Day M: some text]] with optional pipe
    def replace_colon_wikilink(m):
        full_match = m.group(0)
        inner = m.group(1)  # content inside [[ ]]

        # Try to find matching path
        for pattern, path in rf_mapping.items():
            if re.match(pattern, inner):
                # Get display text - try to extract from pipe or use inner
                if '|' in inner:
                    display = inner.split('|', 1)[1]
                else:
                    # Use the Russian part after the colon
                    if ':' in inner:
                        display = inner.split(':', 1)[1].strip()
                    else:
                        display = inner
                return f"[{display}](/{path}/)"
        return full_match  # No match, leave unchanged

    # Match [[...]] patterns with colon in them (Week N - Day M: ...)
    text = re.sub(
        r'\[\[(Week [4-6] - Day \d+:[^\]]*)\]\]',
        replace_colon_wikilink,
        text
    )

    if text != original:
        md_file.write_text(text, encoding="utf-8")
        print(f"  Fixed retail-finance/{md_file.relative_to(rf_path)}")
        changes_total += 1

# ============================================================
# CATEGORY 4: 1C:ERP old English file name references
# ============================================================
print("\n=== Category 4: 1C:ERP old English file references ===")

erp_path = content / "1c-erp"

# Mapping from old English names to new Russian file names (without .md)
erp_name_map = {
    "Неделя 1 - День 4 - Posting Logic": "Неделя 1 - День 4 - Документооборот и регистры",
    "Неделя 1 - День 5 - Reporting Basics": "Неделя 1 - День 5 - Отчётность и аналитика",
    "Неделя 1 - День 6 - Enterprise Design Workshop": "Неделя 1 - День 6 - Практикум по архитектуре",
    "Неделя 2 - День 1 - Nomenclature Master": "Неделя 2 - День 1 - Номенклатура",
    # Also fix the Week-4 reference in week_3/day_7
    "Week 4 - Day 1 - Ордерная схема склада": "Неделя 4 - День 1 - Ордерная схема склада",
}

for md_file in erp_path.rglob("*.md"):
    text = md_file.read_text(encoding="utf-8")
    original = text

    for old_name, new_name in erp_name_map.items():
        # Fix [[old_name|text]] -> [[new_name|text]]
        text = text.replace(f"[[{old_name}|", f"[[{new_name}|")
        text = text.replace(f"[[{old_name}\\|", f"[[{new_name}\\|")
        # Fix bare [[old_name]]
        text = text.replace(f"[[{old_name}]]", f"[[{new_name}]]")

    if text != original:
        md_file.write_text(text, encoding="utf-8")
        print(f"  Fixed 1c-erp/{md_file.relative_to(erp_path)}")
        changes_total += 1

# ============================================================
# Fix remaining README links in 1c-erp (bare [[README|...]] without course prefix)
# These are in files where course is 1c-erp
# ============================================================
print("\n=== Fix 1c-erp bare README links ===")
# Already handled above in Category 2

# ============================================================
# Fix VSM broken links
# ============================================================
print("\n=== VSM broken links ===")
vsm_path = content / "vsm"

for md_file in vsm_path.rglob("*.md"):
    text = md_file.read_text(encoding="utf-8")
    original = text

    # Fix [[Week 1 - Day 4 - VA vs NVA\|text]] -> [text](/vsm/week_1/Week 1 - Day 4 - Value vs Non-Value/)
    # Actual file: Week 1 - Day 4 - Value vs Non-Value.md
    text = re.sub(
        r'\[\[Week 1 - Day 4 - VA vs NVA\\?\|([^\]]+)\]\]',
        r'[\1](/vsm/week_1/Week%201%20-%20Day%204%20-%20Value%20vs%20Non-Value/)',
        text
    )
    text = text.replace("[[Week 1 - Day 4 - VA vs NVA]]",
                        "[Week 1 - Day 4 - Value vs Non-Value](/vsm/week_1/Week%201%20-%20Day%204%20-%20Value%20vs%20Non-Value/)")

    # Fix [[value_stream_mapping/week_2/Week 2 - Day 1|text]] -> [text](/vsm/) (week_2 doesn't exist)
    text = re.sub(
        r'\[\[value_stream_mapping/week_2/Week 2 - Day 1\\?\|([^\]]+)\]\]',
        r'[\1](/vsm/)',
        text
    )
    text = text.replace("[[value_stream_mapping/week_2/Week 2 - Day 1]]", "[Неделя 2, День 1](/vsm/)")

    # Fix [[value_stream_mapping/README|Оглавление]] -> [Оглавление](/vsm/)
    text = text.replace("[[value_stream_mapping/README|Оглавление]]", "[Оглавление](/vsm/)")
    text = text.replace("[[value_stream_mapping/README\\|Оглавление]]", "[Оглавление](/vsm/)")

    if text != original:
        md_file.write_text(text, encoding="utf-8")
        print(f"  Fixed vsm/{md_file.relative_to(vsm_path)}")
        changes_total += 1

print(f"\n=== Total files modified: {changes_total} ===")
