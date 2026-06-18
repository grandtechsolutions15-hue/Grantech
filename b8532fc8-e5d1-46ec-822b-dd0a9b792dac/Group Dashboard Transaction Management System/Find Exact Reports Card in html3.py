
# html3 already has Feature 5 login changes
# The reports card uses different indentation in html3
# Let's find the position of the reports title in html3
search_term = 'fa-chart-bar"></i> Reports</h2>'
pos = html3.find(search_term)
print(f"In html3 at pos: {pos}")
if pos > 0:
    # Show context
    start = max(0, pos - 300)
    end = min(len(html3), pos + 800)
    print(repr(html3[start:end]))
else:
    # try variations
    for term in ['chart-bar', 'Reports</h2>', 'officer-report-type', 'fa-chart-bar']:
        p = html3.find(term)
        print(f"'{term}' at {p}")
