
# 1. Get more of renderOfficerGroups to see what buttons exist
rog_pos = html_content.find('function renderOfficerGroups(')
print("=== renderOfficerGroups full ===")
rog_next = html_content.find('\n    function ', rog_pos + 200)
print(html_content[rog_pos:rog_pos+2000])

# 2. Find viewGroupMembers function
vgm_pos = html_content.find('function viewGroupMembers(')
print("\n\n=== viewGroupMembers ===")
print(html_content[vgm_pos:vgm_pos+1500])

# 3. Find officer report generation
orf_pos = html_content.find('function generateOfficerReportPDF(')
print("\n\n=== generateOfficerReportPDF ===")
print(html_content[orf_pos:orf_pos+1500])

# 4. Find group transaction history rendering in renderGroupView
rgv_pos = html_content.find('function renderGroupView(')
print("\n\n=== renderGroupView full ===")
rgv_end = html_content.find('\n    function ', rgv_pos + 200)
print(html_content[rgv_pos:rgv_pos+3000])
