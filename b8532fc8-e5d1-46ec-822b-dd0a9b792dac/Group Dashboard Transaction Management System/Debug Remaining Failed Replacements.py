
# Debug feature 3 - find exact reports card
pos = html.find('<i class="fas fa-chart-bar"></i> Reports</h2>')
print(f"Found at: {pos}")
print("EXACT:", repr(html[pos-200:pos+600]))
