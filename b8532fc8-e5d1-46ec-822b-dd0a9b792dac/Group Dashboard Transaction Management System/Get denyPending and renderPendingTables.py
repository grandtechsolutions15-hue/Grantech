
# Get renderPendingTables  
rpt_pos = html_content.find('function renderPendingTables(')
rpt_end = html_content.find('\n        function ', rpt_pos + 200)
print("=== renderPendingTables FULL ===")
print(html_content[rpt_pos:rpt_end])

# Get denyPending full (it's huge - just get the first 2000)
dp_pos = html_content.find('function denyPending(')
print("\n\n=== denyPending (first 1000) ===")
print(html_content[dp_pos:dp_pos+1000])

# Get officer report - monthly part (if any)
# Look for what report options exist in officer view
orp_pos = html_content.find("'savings'")
print("\n\n=== Officer report type handling ===")
# Search updateOfficerReportPreview
uorp_pos = html_content.find('function updateOfficerReportPreview(')
uorp_end = html_content.find('\n        function ', uorp_pos + 200)
print(html_content[uorp_pos:uorp_end])
