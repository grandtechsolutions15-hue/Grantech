
import re

html = html_content  # work on a copy

# =========================================================================
# FEATURE 1: Transaction history in group dashboard remains after approval
# The issue: renderGroupView() has "if (!appData.currentUser || role !== 'group') return;"
# so history only shows when logged in as group. We need to also render
# history when admin/officer views a group. The actual approvePending already
# pushes to appData.groupTransactions correctly. The history rendering in 
# renderGroupView is fine - it reads from appData.groupTransactions.
# The real fix: ensure renderGroupView is called after saveAppData/Firebase
# refresh AND that the history section shows BOTH pending (with status) and
# approved transactions. We add "Approved" status column and include denied.
# =========================================================================

# Fix 1a: Update group transaction history table header to include Status column
old_gth_header = '''<th>Group Transaction ID</th>
                                    <th>Date</th>
                                    <th>Type</th>
                                    <th>Total Amount</th>
                                    <th>Member Count</th>
                                    <th>Total Distributed</th>
                                    <th>Individual Transaction IDs</th>'''
new_gth_header = '''<th>Group Transaction ID</th>
                                    <th>Date</th>
                                    <th>Type</th>
                                    <th>Total Amount</th>
                                    <th>Member Count</th>
                                    <th>Total Distributed</th>
                                    <th>Status</th>
                                    <th>Individual Transaction IDs</th>'''
html = html.replace(old_gth_header, new_gth_header, 1)

# Fix 1b: Update renderGroupView to include BOTH approved groupTransactions AND
# pending ones (with their status shown), so history always persists
old_history_render = '''        // Render group transaction history
        const groupTransactions = appData.groupTransactions.filter(gt => gt.groupId === group.id).sort((a, b) => new Date(b.date) - new Date(a.date));
        document.getElementById('group-transaction-history').innerHTML = groupTransactions.map(gt => {
            const individualTxnIds = gt.individualTransactionIds ? gt.individualTransactionIds.join(', ') : '--';
            return '<tr><td><strong>' + gt.id + '</strong></td><td>' + gt.date + '</td><td>' + gt.type + '</td>' +
                '<td>' + formatKES(gt.totalAmount) + '</td><td>' + gt.memberCount + '</td>' +
                '<td>' + formatKES(gt.totalDistributed || gt.totalAmount) + '</td><td style="font-size:0.8rem;"><code>' + individualTxnIds + '</code></td></tr>';
        }).join('');'''

new_history_render = '''        // Render group transaction history - includes approved, pending AND denied
        const approvedGT = appData.groupTransactions.filter(gt => gt.groupId === group.id).map(gt => ({
            txnId: gt.id, date: gt.date, type: gt.type, totalAmount: gt.totalAmount,
            memberCount: gt.memberCount, totalDistributed: gt.totalDistributed || gt.totalAmount,
            status: 'approved', individualTxnIds: (gt.individualTransactionIds || []).join(', ')
        }));
        // Also include all pending/denied group transaction requests so history is complete
        const allGroupPending = appData.pendingApprovals.filter(p => isGroupTransactionApproval(p) && p.payload && p.payload.groupId === group.id && p.status !== 'approved');
        const pendingRows = allGroupPending.map(p => {
            const txnId = p.transactionId || (p.payload ? p.payload.transactionId : p.id);
            return {
                txnId: txnId, date: p.date, type: p.payload ? p.payload.type : p.type,
                totalAmount: p.amount, memberCount: p.payload ? (p.payload.allocations || []).length : 0,
                totalDistributed: p.amount, status: p.status, individualTxnIds: '--'
            };
        });
        const allHistoryRows = [...approvedGT, ...pendingRows].sort((a, b) => new Date(b.date) - new Date(a.date));
        const statusBadgeMap = { approved: 'status-active', pending: 'status-awaiting', denied: 'status-cancelled' };
        document.getElementById('group-transaction-history').innerHTML = allHistoryRows.length ? allHistoryRows.map(row => {
            const badge = '<span class="status-badge ' + (statusBadgeMap[row.status] || 'status-awaiting') + '">' + row.status.toUpperCase() + '</span>';
            return '<tr><td><strong>' + row.txnId + '</strong></td><td>' + row.date + '</td><td>' + row.type + '</td>' +
                '<td>' + formatKES(row.totalAmount) + '</td><td>' + row.memberCount + '</td>' +
                '<td>' + formatKES(row.totalDistributed) + '</td><td>' + badge + '</td>' +
                '<td style="font-size:0.8rem;"><code>' + row.individualTxnIds + '</code></td></tr>';
        }).join('') : '<tr><td colspan="8" class="empty-state"><p>No transactions yet</p></td></tr>';'''

html = html.replace(old_history_render, new_history_render, 1)

print("Feature 1: Transaction history fix applied:", old_history_render[:50] in html_content and new_history_render[:50] in html)

# =========================================================================
# FEATURE 2: Admin can edit group transaction when approving or denying it
# Add "Edit & Approve" button to admin pending table for group transactions
# Add a modal for editing group transaction details before approving
# Add deny reason field in confirmDenyPending
# =========================================================================

# Fix 2a: Add "Edit & Approve" button in admin pending table for group transactions
old_admin_pending_row = '''                return \'<tr><td><span class="status-badge status-awaiting">\' + (isGroupTransactionApproval(p) ? \'GROUP_TRANSACTION\' : p.type.toUpperCase()) + \'</span></td>\' +
                    \'<td>\' + txnId + \'</td><td>\' + subject + \'</td><td>\' + (officer ? officer.name : \'N/A\') + \'</td>\' +
                    \'<td>\' + formatKES(p.amount) + \'</td><td>\' + p.date + \'</td>\' +
                    \'<td><div class="btn-group"><button class="btn btn-success btn-sm" onclick="confirmApprovePending(\' + p.id + \')"><i class="fas fa-check"></i> Approve</button>\' +
                    \'<button class="btn btn-danger btn-sm" onclick="confirmDenyPending(\' + p.id + \')"><i class="fas fa-times"></i> Deny</button></div></td></tr>\';'''

new_admin_pending_row = '''                const editBtn = isGroupTransactionApproval(p) ?
                    \'<button class="btn btn-warning btn-sm" onclick="openEditApprovePending(\' + p.id + \')"><i class="fas fa-edit"></i> Edit & Approve</button>\' : \'\';
                return \'<tr><td><span class="status-badge status-awaiting">\' + (isGroupTransactionApproval(p) ? \'GROUP_TRANSACTION\' : p.type.toUpperCase()) + \'</span></td>\' +
                    \'<td>\' + txnId + \'</td><td>\' + subject + \'</td><td>\' + (officer ? officer.name : \'N/A\') + \'</td>\' +
                    \'<td>\' + formatKES(p.amount) + \'</td><td>\' + p.date + \'</td>\' +
                    \'<td><div class="btn-group"><button class="btn btn-success btn-sm" onclick="confirmApprovePending(\' + p.id + \')"><i class="fas fa-check"></i> Approve</button>\' +
                    editBtn +
                    \'<button class="btn btn-danger btn-sm" onclick="confirmDenyPending(\' + p.id + \', true)"><i class="fas fa-times"></i> Deny</button></div></td></tr>\';'''

html = html.replace(old_admin_pending_row, new_admin_pending_row, 1)
print("Feature 2a: Edit & Approve button added:", old_admin_pending_row[:60] not in html)

# Fix 2b: Update confirmDenyPending to accept optional reason parameter and show reason input
old_confirm_deny = '''function confirmDenyPending(pendingId, event) {
        if (event) event.stopPropagation();'''

new_confirm_deny = '''function confirmDenyPending(pendingId, showReason, event) {
        if (event) event.stopPropagation();
        if (showReason === true) {
            // Admin denying - show reason modal
            const reasonHtml = \'<div style="padding:1.5rem"><h3 style="margin-bottom:1rem;color:var(--danger)"><i class="fas fa-times-circle"></i> Deny Transaction</h3>\' +
                \'<p style="margin-bottom:1rem;color:#666;">Provide a reason for denial (optional):</p>\' +
                \'<textarea id="deny-reason-input" placeholder="Enter reason for denial..." style="width:100%;padding:10px;border:2px solid #e8e8e8;border-radius:8px;min-height:80px;font-size:0.95rem;margin-bottom:1rem;"></textarea>\' +
                \'<div style="display:flex;gap:10px;justify-content:flex-end">\' +
                \'<button class="btn btn-secondary btn-sm" onclick="closeModal(\\\'admin-edit-approve-modal\\\')">Cancel</button>\' +
                \'<button class="btn btn-danger btn-sm" onclick="executeDenyWithReason(\' + pendingId + \')"><i class="fas fa-times"></i> Confirm Deny</button>\' +
                \'</div></div>\';
            document.getElementById(\'admin-edit-approve-modal\').querySelector(\'.modal-body\').innerHTML = reasonHtml;
            document.getElementById(\'admin-edit-approve-modal\').querySelector(\'.modal-header h2\').textContent = \'Deny Transaction\';
            openModal(\'admin-edit-approve-modal\');
            return;
        }'''

html = html.replace(old_confirm_deny, new_confirm_deny, 1)
print("Feature 2b: confirmDenyPending updated:", old_confirm_deny[:50] not in html)

print("\nAll feature 2 replacements done. HTML length:", len(html))
