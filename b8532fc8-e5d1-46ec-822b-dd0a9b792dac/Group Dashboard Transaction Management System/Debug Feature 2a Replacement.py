
# Feature 2a didn't match - let's find the exact text in the HTML
# Look for the admin pending table row rendering

search = "confirmDenyPending(' + p.id + ')"
pos = html_content.find(search)
print(f"Found at pos: {pos}")
print(repr(html_content[pos-500:pos+200]))
