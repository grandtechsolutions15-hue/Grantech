
# Get full renderGroupView function
rgv_pos = html_content.find('function renderGroupView(')
rgv_end = html_content.find('\n    function ', rgv_pos + 500)
full_rgv = html_content[rgv_pos:rgv_end]
print(f"renderGroupView length: {len(full_rgv)}")
print(full_rgv[3000:])  # Show the last part

# Also get the admin pending section HTML - the group transaction pending modal
print("\n\n=== admin-pending-table HTML ===")
apt_pos = html_content.find('id="admin-pending-table"')
print(html_content[apt_pos-500:apt_pos+500])

# Find the group transaction part of approvePending
ap_pos = html_content.find('function approvePending(')
ap_end = html_content.find('\n        function ', ap_pos + 100)
full_ap = html_content[ap_pos:ap_end]
# Find the group_transaction handling
gt_pos = full_ap.find('isGroupTransactionApproval')
print("\n\n=== approvePending group_transaction section ===")
print(full_ap[gt_pos:gt_pos+3000])
