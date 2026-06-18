
# Get exact reports card text
rpt_card_marker = '<div class="card">\n                    <div class="card-header">\n                        <h2 class="card-title"><i class="fas fa-chart-bar"></i> Reports</h2>'
pos = html.find(rpt_card_marker)
end_marker = '</div>\n            </section>\n\n            <!-- ADMIN SECTION'
end_pos = html.find(end_marker, pos)
reports_card_actual = html[pos:end_pos + len('</div>')]
print("EXACT REPORTS CARD:")
print(reports_card_actual)

# Get exact group transaction form type block
print("\n\n--- EXACT GROUP TXN FORM ---")
gtf_pos = html.find('id="group-transaction-amount"')
print(repr(html[gtf_pos-200:gtf_pos+400]))

# Get the group history table header exact
print("\n\n--- EXACT GROUP HISTORY HEADER ---")
gth_pos = html.find('Group Transaction ID')
print(repr(html[gth_pos-200:gth_pos+400]))
