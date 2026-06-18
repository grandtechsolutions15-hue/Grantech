
# The replacements are failing due to whitespace/indentation differences
# Let's find the exact text in html (which already has features 1+2)

# Feature 3: Find the exact officer reports card
pos = html.find('id="officer-report-type"')
print("=== Exact officer report card context ===")
print(repr(html[pos-400:pos+100]))
