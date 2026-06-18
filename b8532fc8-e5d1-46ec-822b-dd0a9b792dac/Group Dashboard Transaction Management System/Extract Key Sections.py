
# Find the key patterns we need to modify
import re

# 1. Find login tabs section
login_tab_start = html_content.find('login-tabs')
login_tab_end = html_content.find('</div>', login_tab_start + 100)
print("=== LOGIN TABS ===")
print(html_content[login_tab_start-50:login_tab_end+100])

print("\n\n=== SEARCHING FOR GROUP LOGIN FORM ===")
group_form_pos = html_content.find('login-form-group')
print(html_content[group_form_pos-50:group_form_pos+400])
