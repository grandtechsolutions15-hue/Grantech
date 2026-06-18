
# Get important function bodies
# 1. approvePending function
ap_pos = html_content.find('function approvePending(')
ap_end = html_content.find('\n        function ', ap_pos + 100)
print("=== approvePending() (first 3000 chars) ===")
print(html_content[ap_pos:min(ap_pos+3000, ap_end)])

print("\n\n=== recordGroupTransaction() ===")
rgt_pos = html_content.find('function recordGroupTransaction(')
rgt_end = html_content.find('\n        function ', rgt_pos + 100)
print(html_content[rgt_pos:min(rgt_pos+2000, rgt_end)])

print("\n\n=== renderGroupView() - first 2000 chars ===")
rgv_pos = html_content.find('function renderGroupView(')
print(html_content[rgv_pos:rgv_pos+2000])
