
# Get the full group_transaction approval section
ap_pos = html_content.find('function approvePending(')
ap_end = html_content.find('\n        function ', ap_pos + 100)
full_ap = html_content[ap_pos:ap_end]
gt_pos = full_ap.find('isGroupTransactionApproval')
print("=== full group transaction approval ===")
print(full_ap[gt_pos:gt_pos+4000])

# Get renderOfficerLoanApps
rola_pos = html_content.find('function renderOfficerLoanApps(')
rola_end = html_content.find('\n    function ', rola_pos + 200)
print("\n\n=== renderOfficerLoanApps ===")
print(html_content[rola_pos:rola_end])
