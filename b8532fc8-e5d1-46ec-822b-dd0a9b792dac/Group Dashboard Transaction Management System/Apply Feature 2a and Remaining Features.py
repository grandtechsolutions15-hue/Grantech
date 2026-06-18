
# The admin pending table is in renderPendingTables. Let's find the exact admin section
# and replace it with the edit & approve button

# Find the admin pending section in renderPendingTables
admin_pending_search = "// Admin pending table"
pos_in_html = html.find(admin_pending_search)
print(f"Admin pending section at: {pos_in_html}")
print(repr(html[pos_in_html:pos_in_html+1200]))
