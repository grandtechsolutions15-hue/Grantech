
# Insert the new JS functions before saveAppData function (at pos 124784)
pos_insert = 124784

final_with_js = final[:pos_insert] + new_js_functions + final[pos_insert:]
print(f"JS injected. New length: {len(final_with_js)}")

# Add the admin-edit-approve-modal (needed for Feature 2) and 
# confirm-deny-reason-modal (Feature 2) just before </body>
new_modals = """
    <!-- Admin Edit & Approve Modal (Feature 2) -->
    <div class="modal-overlay" id="admin-edit-approve-modal-overlay" onclick="closeModal('admin-edit-approve-modal')"></div>
    <div class="modal modal-lg" id="admin-edit-approve-modal" style="max-width:700px">
        <div class="modal-header">
            <h2>Edit & Approve Transaction</h2>
            <button class="modal-close" onclick="closeModal('admin-edit-approve-modal')"><i class="fas fa-times"></i></button>
        </div>
        <div class="modal-body"></div>
    </div>

    <!-- Deny Reason Input (for confirmDenyPending with reason) -->
    <input type="hidden" id="confirm-pending-deny-id" value="">
    <div id="confirm-deny-reason-row" style="display:none"></div>

"""

# Insert modals before </body>
body_close = final_with_js.rfind('</body>')
if body_close >= 0:
    final_with_js = final_with_js[:body_close] + new_modals + final_with_js[body_close:]
    print("Modals added before </body>")

# Also add a modal overlay CSS registration for the new modal
# (it uses the same modal pattern as existing modals which already have CSS)

# Also update the admin pending "Deny" button to pass true for showReason
# Find where the admin deny button is currently rendered in the updated renderPendingTables
old_admin_deny_btn = "confirmDenyPending(' + p.id + ')\">"
new_admin_deny_btn = "confirmDenyPending(' + p.id + ', true)\">"
# Count occurrences in admin context
count_before = final_with_js.count(old_admin_deny_btn)
# Replace only the one in the admin section (2nd occurrence - first is officer, second is admin)
positions = []
start = 0
while True:
    pos = final_with_js.find(old_admin_deny_btn, start)
    if pos == -1:
        break
    positions.append(pos)
    start = pos + 1
print(f"Found {len(positions)} occurrences of deny button at: {positions}")

# Replace the admin pending one (second occurrence) 
if len(positions) >= 2:
    admin_deny_pos = positions[1]  # 2nd occurrence is in admin section
    final_with_js = final_with_js[:admin_deny_pos] + new_admin_deny_btn + final_with_js[admin_deny_pos + len(old_admin_deny_btn):]
    print("Admin deny button updated to pass showReason=true")

print(f"\nFinal file length: {len(final_with_js)}")

# Verify all features
checks = {
    'F1 history status rows': 'allHistoryRows' in final_with_js,
    'F2 edit approve modal': 'admin-edit-approve-modal' in final_with_js,
    'F2 openEditApprovePending': 'openEditApprovePending' in final_with_js,
    'F2 saveEditAndApprove': 'saveEditAndApprove' in final_with_js,
    'F2 deny with reason': 'showReason' in final_with_js,
    'F3 monthly card HTML': 'officer-monthly-summary-table' in final_with_js,
    'F3 renderMonthlyCollectionSummary': 'renderMonthlyCollectionSummary' in final_with_js,
    'F3 date range': 'officer-report-from' in final_with_js,
    'F4 savings input HTML': 'group-transaction-savings' in final_with_js,
    'F4 history savings col': 'Savings (KES)</th>' in final_with_js,
    'F5 no group tab': 'id="login-tab-group"' not in final_with_js,
    'F5 officer default active': '<form class="login-form active" id="login-form-officer"' in final_with_js,
    'F5 openGroupDetailView': 'openGroupDetailView' in final_with_js,
    'F6 Loan ID th in officer': 'Loan ID</th><th>Client</th>' in final_with_js,
    'F6 openLoanDetailModal': 'openLoanDetailModal' in final_with_js,
    'F6 officer loan clickable': 'openLoanDetailModal' in final_with_js,
}
for k, v in checks.items():
    print(f"{'✓' if v else '✗'} {k}")
