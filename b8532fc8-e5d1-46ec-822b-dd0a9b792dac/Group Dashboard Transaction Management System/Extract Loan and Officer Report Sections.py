
# 1. Find where loan IDs are generated and loan apps table
loan_gen = html_content.find('function applyLoan')
print("=== applyLoan function ===")
print(html_content[loan_gen:loan_gen+1000])

# 2. Find officer loan apps table HTML
ola_pos = html_content.find('officer-loan-apps')
print("\n\n=== officer-loan-apps HTML ===")
print(html_content[ola_pos-300:ola_pos+800])

# 3. Find renderOfficerView or renderAdminGroups for "view group" action
rg_pos = html_content.find('function renderAdminGroups(')
print("\n\n=== renderAdminGroups (first 1500) ===")
print(html_content[rg_pos:rg_pos+1500])

# 4. Find renderOfficerGroups
rog_pos = html_content.find('function renderOfficerGroups(')
print("\n\n=== renderOfficerGroups (first 1500) ===")
print(html_content[rog_pos:rog_pos+1500])
