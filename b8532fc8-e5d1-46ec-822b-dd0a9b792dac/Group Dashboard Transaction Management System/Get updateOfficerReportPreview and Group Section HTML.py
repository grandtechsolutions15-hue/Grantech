
# Get updateOfficerReportPreview
uorp_pos = html_content.find('function updateOfficerReportPreview(')
print("=== updateOfficerReportPreview (first 2000) ===")
print(html_content[uorp_pos:uorp_pos+2000])

# Get the group section transaction form HTML
# Find the group transaction form with the type selector
grp_form_start = html_content.find('Record Group Transaction')
print("\n\n=== Group transaction form ===")
print(html_content[grp_form_start-100:grp_form_start+2000])

# Find the group history table header
gth_hdr = html_content.find('Group Transaction ID')
print("\n\n=== Group history table header ===")
print(html_content[gth_hdr-300:gth_hdr+400])
