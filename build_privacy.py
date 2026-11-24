#!/usr/bin/env python3
"""Builds privacy.html (English) and privacy-<lang>.html for every app language from privacy_i18n.json.

privacy_i18n.json: {"en": {segment: text}, "<lang>": {...}} with the same 27 segments per language.
English stays at privacy.html (the URL the App Store listings use). Arabic pages are right-to-left.
Run after editing the English text: re-translate the changed segments, then `python3 build_privacy.py`.
"""
import json, pathlib

HERE = pathlib.Path(__file__).parent
T = json.load(open(HERE / "privacy_i18n.json", encoding="utf-8"))
NAMES = {"en": "English", "ar": "العربية", "de": "Deutsch", "es": "Español", "fr": "Français", "hi": "हिन्दी",
         "id": "Bahasa Indonesia", "it": "Italiano", "ja": "日本語", "ko": "한국어", "ms": "Bahasa Melayu",
         "nl": "Nederlands", "pl": "Polski", "pt-BR": "Português (Brasil)", "pt-PT": "Português (Portugal)",
         "ru": "Русский", "sv": "Svenska", "th": "ไทย", "tr": "Türkçe", "vi": "Tiếng Việt",
         "zh-Hans": "简体中文", "zh-Hant": "繁體中文"}
ORDER = ["en"] + sorted([l for l in NAMES if l != "en"], key=lambda l: NAMES[l].lower())

CSS = """body{font:17px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;max-width:680px;margin:0 auto;padding:32px 20px;color:#1d1d1f;background:#fbfbfd}
h1{font-size:28px;line-height:1.25}h2{font-size:20px;margin-top:28px}a{color:#0a66d8}nav{margin-bottom:24px;font-size:15px;display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between}
select{font:inherit;font-size:15px;padding:4px 8px;border-radius:8px;border:1px solid #c7c7cc;background:inherit;color:inherit}
.note{font-size:14px;color:#6e6e73;border-left:3px solid #c7c7cc;padding-left:12px}
[dir=rtl] .note{border-left:0;border-right:3px solid #c7c7cc;padding-left:0;padding-right:12px}
@media(prefers-color-scheme:dark){body{background:#111;color:#eee}a{color:#5aa9ff}.note{color:#a1a1a6}}"""


def page_name(lang):
    return "privacy.html" if lang == "en" else f"privacy-{lang}.html"


def build(lang):
    s = T[lang]
    opts = "".join(f'<option value="{page_name(l)}"{" selected" if l == lang else ""}>{NAMES[l]}</option>' for l in ORDER)
    note = "" if lang == "en" else f'<p class="note">{s["prevails"]} <a href="privacy.html">English</a></p>'
    return f"""<!doctype html><html lang="{lang}" dir="{"rtl" if lang == "ar" else "ltr"}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{s["title"]}</title>
{"".join(f'<link rel="alternate" hreflang="{l}" href="{page_name(l)}">' for l in ORDER)}
<style>{CSS}</style></head><body>
<nav><span><a href="./">TapSpend</a> · <a href="{page_name(lang)}">{s["nav_privacy"]}</a></span>
<label>{s["lang_label"]}: <select onchange="location.href=this.value">{opts}</select></label></nav>
<h1>{s["title"]}</h1>
<p><em>{s["updated"]}</em></p>
{note}
<p>{s["intro"]}</p>
<h2>{s["h_stay"]}</h2>
<p>{s["p_stay"]}</p>
<h2>{s["h_icloud"]}</h2>
<p>{s["p_icloud"]}</p>
<h2>{s["h_smart"]}</h2>
<p>{s["p_smart"]}</p>
<h2>{s["h_purchases"]}</h2>
<p>{s["p_purchases"]}</p>
<h2>{s["h_exports"]}</h2>
<p>{s["p_exports"]}</p>
<h2>{s["h_dont"]}</h2>
<ul><li>{s["li_accounts"]}</li><li>{s["li_ads"]}</li><li>{s["li_analytics"]}</li><li>{s["li_sell"]}</li></ul>
<h2>{s["h_children"]}</h2><p>{s["p_children"]}</p>
<h2>{s["h_changes"]}</h2><p>{s["p_changes"]}</p>
<h2>{s["h_contact"]}</h2><p>{s["p_contact"]}</p></body></html>
"""


for lang in ORDER:
    (HERE / page_name(lang)).write_text(build(lang), encoding="utf-8")
print(len(ORDER), "pages:", ", ".join(page_name(l) for l in ORDER))
