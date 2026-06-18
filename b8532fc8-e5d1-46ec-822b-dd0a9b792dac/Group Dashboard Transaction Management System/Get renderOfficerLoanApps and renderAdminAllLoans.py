
# Get renderOfficerLoanApps full
rola_pos = html_content.find('function renderOfficerLoanApps(')
rola_end = html_content.find('\n    function ', rola_pos + 200)
print("=== renderOfficerLoanApps FULL ===")
print(html_content[rola_pos:rola_end])

# Get renderAdminAllLoans
ral_pos = html_content.find('function renderAdminAllLoans(')
ral_end = html_content.find('\n    function ', ral_pos + 200)
print("\n\n=== renderAdminAllLoans FULL ===")
print(html_content[ral_pos:ral_end])

# Get the denyPending function
dp_pos = html_content.find('function denyPending(')
dp_end = html_content.find('\n        function ', dp_pos + 100)
print("\n\n=== denyPending FULL ===")
print(html_content[dp_pos:dp_end])
