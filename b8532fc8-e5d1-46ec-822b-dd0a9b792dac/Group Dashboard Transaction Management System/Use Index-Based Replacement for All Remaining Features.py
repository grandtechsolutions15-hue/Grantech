
# Use index-based slicing to avoid whitespace match issues
# Work from 'html' (has features 1 & 2 + feature 5 login changes from html3)
# Actually let's start fresh from html3 which has feature 5 login changes applied

# Since html3 has feature 5 login tab changes applied, use it as base
# But features 3, 4, admin groups btn, officer loans header failed
# Let's use index-based insertion

base = html3  # use html3 which has F1, F2 (partial), F5 login

# ---- FEATURE 3: Reports card - use index slicing ----
pos = base.find('<div class="card">\n                    <div class="card-header">\n                        <h2 class="card-title"><i class="fas fa-chart-bar"></i> Reports</h2>')
# Find where this card ends
card_end_search = '</div>\n                </div>\n            </section>'
end_pos = base.find(card_end_search, pos)
old_card = base[pos:end_pos + len('</div>\n                </div>')]
print(f"F3 reports card: pos={pos}, end_pos={end_pos}, len={len(old_card)}")
print("OLD CARD END:", repr(old_card[-100:]))
