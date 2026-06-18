
# Get the actual HTML login tabs buttons
login_div_pos = html_content.find('<div class="login-tabs">')
print("=== LOGIN TABS HTML ===")
print(html_content[login_div_pos:login_div_pos+600])

print("\n\n=== GROUP LOGIN FORM ===")
group_form_pos = html_content.find('id="login-form-group"')
print(html_content[group_form_pos-10:group_form_pos+500])

print("\n\n=== GROUP TRANSACTION HISTORY TABLE ===")
gth_pos = html_content.find('group-transaction-history')
print(html_content[gth_pos:gth_pos+800])

print("\n\n=== APPROVE PENDING FUNCTION SEARCH ===")
ap_pos = html_content.find('function approvePending(')
print(html_content[ap_pos:ap_pos+200])
