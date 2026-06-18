
# The admin groups view button ('openGro...') is ALREADY in html3!
# That's because html3's previous block also had the admin groups view button from earlier 
# (it was in the original file from the analysis). Let's confirm all features are truly in html3

checks = {
    'F1 history with status': 'status-awaiting' in html3 and 'allHistoryRows' in html3,
    'F2 edit & approve btn': 'openEditApprovePending' in html3,
    'F2 deny with reason': 'showReason' in html3,
    'F3 monthly card': 'officer-monthly-summary-table' in html3,
    'F3 date range filter': 'officer-report-from' in html3,
    'F4 savings input': 'group-transaction-savings' in html3,
    'F4 reg input': 'group-transaction-registration' in html3,
    'F4 loan input': 'group-transaction-loan' in html3,
    'F4 table savings col': 'Savings (KES)</th>' in html3,
    'F4 table loan col': 'Loan Repayment (KES)</th>' in html3,
    'F5 no group login tab': 'id="login-tab-group"' not in html3,
    'F5 officer form active': '<form class="login-form active" id="login-form-officer"' in html3,
    'F5 view group btn admin': 'openGroupDetailView' in html3 or 'openGro' in html3,
    'F6 loan id header officer': 'Loan ID</th><th>Client</th>' in html3,
    'F6 officer loan clickable': 'openLoanDetailModal' in html3,
}

for k, v in checks.items():
    print(f"{'✓' if v else '✗'} {k}")
