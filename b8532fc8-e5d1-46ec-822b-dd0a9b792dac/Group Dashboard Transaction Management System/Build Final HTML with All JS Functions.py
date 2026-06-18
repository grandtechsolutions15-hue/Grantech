
# Start fresh from html3 (has all 6 feature HTML changes applied)
# Now add the View Group btn and all new JavaScript functions

final_html = html3  # html3 has features 1,2,3,4,5 HTML changes applied

# ---- Feature 5: Add "View Group" button in admin groups render ----
# Use a unique substring that's definitely in the code
old_admin_delete = "confirmDeleteGroup(\\''  + g.id + '\\')\" title=\"Delete\"><i class=\"fas fa-trash\"></i></button>' +\n                '</div></td></tr>';"
new_admin_delete = "confirmDeleteGroup(\\''  + g.id + '\\')\" title=\"Delete\"><i class=\"fas fa-trash\"></i></button>' +\n                '</div></td></tr>';"

# Let's just look for the exact pattern
delete_search = "confirmDeleteGroup"
pos1 = final_html.find(delete_search)
print(f"confirmDeleteGroup at: {pos1}")
print(repr(final_html[pos1-150:pos1+200]))
