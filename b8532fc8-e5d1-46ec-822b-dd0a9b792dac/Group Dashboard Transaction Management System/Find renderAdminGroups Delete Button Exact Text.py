
# Find renderAdminGroups action buttons
rag_pos = html3.find("function renderAdminGroups(")
rag_end = html3.find("\n    function ", rag_pos + 200)
admin_grp_func = html3[rag_pos:rag_end]
# Print characters 400-900 to find the buttons
print(repr(admin_grp_func[400:900]))
