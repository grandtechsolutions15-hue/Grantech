
# Find the exact admin groups buttons
rag_pos = html4.find("function renderAdminGroups(")
rag_end = html4.find("\n    function ", rag_pos + 200)
admin_grp_func = html4[rag_pos:rag_end]
print("Admin groups function:")
print(repr(admin_grp_func))
