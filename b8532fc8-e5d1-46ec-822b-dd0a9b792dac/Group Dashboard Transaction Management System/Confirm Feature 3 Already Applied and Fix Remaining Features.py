
# Feature 3 (monthly card + date filter) is ALREADY in html3! 
# The replacement actually worked but the verification check was wrong
# Let's verify all features in html3 and handle the remaining ones

print("=== FEATURE STATUS IN html3 ===")
print("F1 (history status col):", 'Savings (KES)</th>' not in html3 and 'Individual Transaction IDs</th>' not in html3)
print("F1 check (new header):", 'Group Transaction ID</th>' in html3)
print("F2 (edit & approve btn):", 'Edit &amp; Approve' in html3 or 'Edit & Approve' in html3 or 'openEditApprovePending' in html3)
print("F3 (monthly card):", 'officer-monthly-summary-table' in html3)
print("F3 (date range filter):", 'officer-report-from' in html3)
print("F4 (savings column):", 'group-transaction-savings' in html3)
print("F4 (loan column):", 'group-transaction-loan' in html3)
print("F5 (no group tab):", 'id="login-tab-group"' not in html3)
print("F5 (officer tab active):", 'active" onclick="switchLoginTab(\'officer\')' in html3 or '"login-tab active" onclick="switchLoginTab' in html3)
print("F6 (Loan ID header in officer):", 'Loan ID</th><th>Client</th>' in html3)

# Check feature 4 (transaction columns)
pos4 = html3.find('group-transaction-savings')
print(f"\nF4 group-transaction-savings at: {pos4}")
if pos4 < 0:
    # Find what we have
    pos_amt = html3.find('group-transaction-amount')
    print(f"Still has group-transaction-amount at: {pos_amt}")
    print(repr(html3[pos_amt-100:pos_amt+400]))

# Check F6 officer loans header
pos6 = html3.find('Loan ID</th>')
print(f"\nF6 officer Loan ID col at: {pos6}")
if pos6 < 0:
    pos_ola = html3.find('officer-loan-apps')
    print(f"officer-loan-apps at: {pos_ola}")
    print(repr(html3[pos_ola-300:pos_ola+200]))
