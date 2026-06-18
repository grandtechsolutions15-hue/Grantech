
# Look at: 
# 1. renderGroupView - the history rendering part
# 2. group transaction type selector  
# 3. officer reports section
# 4. loan application area and ID generation

# renderGroupView history part
rgv_pos = html_content.find('function renderGroupView(')
rgv_content = html_content[rgv_pos:rgv_pos+5000]
# find the history table rendering
hist_in_func = rgv_content.find('history')
print("=== renderGroupView history section ===")
print(rgv_content[max(0,hist_in_func-200):hist_in_func+1000])

print("\n\n=== GROUP TRANSACTION TYPE SELECTOR (HTML) ===")
type_sel = html_content.find('group-transaction-type')
print(html_content[type_sel-100:type_sel+400])

print("\n\n=== ADMIN GROUPS TABLE HTML ===")
agt_pos = html_content.find('id="admin-groups-table"')
print(html_content[agt_pos-200:agt_pos+600])
