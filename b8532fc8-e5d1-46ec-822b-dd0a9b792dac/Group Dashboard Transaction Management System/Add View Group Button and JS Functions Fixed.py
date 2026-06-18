
# Fix the syntax error - the issue is with escaped quotes in the JS strings within Python strings
# Use a different approach - use raw index-based replacement

# Work from html3 which has all HTML changes applied
html4 = html3

# Step 1: Add View Group button in admin groups render using simpler string
rag_pos = html4.find("function renderAdminGroups(")
rag_end = html4.find("\n    function ", rag_pos + 200)
admin_grp_func = html4[rag_pos:rag_end]

# Find the action buttons part
old_btns_search = "'<td><div class=\"action-btns\">' +\n                '<button class=\"action-btn edit\" onclick=\"openEditGroup"
pos_in_func = admin_grp_func.find(old_btns_search)
print(f"Old admin group btns found at offset {pos_in_func}")

if pos_in_func >= 0:
    print(repr(admin_grp_func[pos_in_func:pos_in_func+300]))
