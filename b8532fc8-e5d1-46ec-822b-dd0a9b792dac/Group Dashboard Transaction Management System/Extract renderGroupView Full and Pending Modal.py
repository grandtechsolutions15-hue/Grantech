
# Get the full renderGroupView function
rgv_pos = html_content.find('function renderGroupView(')
rgv_end = html_content.find('\n    function ', rgv_pos + 500)
print("=== renderGroupView FULL ===")
print(html_content[rgv_pos:rgv_end])
