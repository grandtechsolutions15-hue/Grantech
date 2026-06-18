
with open("index_pending_modal_working.html", "r", encoding="utf-8") as f:
    html_content = f.read()

print(f"Loaded HTML file: {len(html_content):,} characters")
print(f"Lines: {html_content.count(chr(10)):,}")
