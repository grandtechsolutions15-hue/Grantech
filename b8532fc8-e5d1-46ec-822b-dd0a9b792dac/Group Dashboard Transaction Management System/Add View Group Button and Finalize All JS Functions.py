
# html3 has all HTML changes applied. Need to:
# 1. Add "View Group" button in admin groups render (Feature 5)
# 2. Add "View Group" button in officer groups (Feature 5) - already has "View Members" btn
# 3. Add all new JavaScript functions for all 6 features
# 4. Update existing JS functions to handle the new features

# Step 1: Add View Group button in admin groups render
old_admin_grp_btns = """'<td><div class="action-btns">' +
                '<button class="action-btn edit" onclick="openEditGroup(\\'' + g.id + '\\')\" title=\"Edit\"><i class="fas fa-edit"></i></button>' +
                '<button class="action-btn delete" onclick="confirmDeleteGroup(\\'' + g.id + '\\')\" title=\"Delete\"><i class="fas fa-trash"></i></button>' +
                '</div></td></tr>';"""

new_admin_grp_btns = """'<td><div class="action-btns">' +
                '<button class="action-btn view" onclick="openGroupDetailView(\\'' + g.id + '\\')\" title=\"View Group\"><i class="fas fa-eye"></i></button>' +
                '<button class="action-btn edit" onclick="openEditGroup(\\'' + g.id + '\\')\" title=\"Edit\"><i class="fas fa-edit"></i></button>' +
                '<button class="action-btn delete" onclick="confirmDeleteGroup(\\'' + g.id + '\\')\" title=\"Delete\"><i class="fas fa-trash"></i></button>' +
                '</div></td></tr>';"""

html4 = html3.replace(old_admin_grp_btns, new_admin_grp_btns, 1)
print(f"F5 admin view group: {old_admin_grp_btns[:60] not in html4}")

# Step 2: Update renderOfficerGroups "View Members" to "View Group" for full view
old_view_members_btn = '\'<button class=\"btn btn-sm btn-primary\" onclick=\"viewGroupMembers(\\'' + g.id + \'\\')"><i class=\"fas fa-eye\"></i> View Members</button>\''
new_view_group_btn = '\'<button class=\"btn btn-sm btn-primary\" onclick=\"openGroupDetailView(\\'' + g.id + \'\\')"><i class=\"fas fa-eye\"></i> View Group</button>\''
html4 = html4.replace(old_view_members_btn, new_view_group_btn, 1)
print(f"F5 officer view group: {old_view_members_btn[:60] not in html4}")

# Step 3: Update renderOfficerLoanApps to show Loan ID as clickable link (Feature 6)
old_officer_loan_row = """            const client = appData.clients.find(c => c.id === l.clientId);
            const multiplier = (l.amount / client.savings).toFixed(1);
            const canApprove = l.amount <= client.savings * appData.config.savingsMultiplier;
            return '<tr><td><strong>' + client.name + '</strong><br><small>' + client.phone + '</small></td>' +
                '<td>' + formatKES(l.amount) + '</td>' +
                '<td>' + l.purpose + '</td>' +
                '<td>' + l.duration + ' months</td>' +
                '<td>' + multiplier + 'x (' + (canApprove ? '<span style=\"color:var(--success)\">OK</span>' : '<span style=\"color:var(--danger)\">Exceeds</span>') + ')</td>' +
                '<td><div class=\"btn-group\">' +
                '<button class=\"btn btn-success btn-sm\" ' + (canApprove ? '' : 'disabled') + ' onclick=\"approveLoan(\\'' + l.id + '\\')"><i class=\"fas fa-check\"></i> Approve</button>' +
                '<button class=\"btn btn-danger btn-sm\" onclick=\"rejectLoan(\\'' + l.id + '\\')"><i class=\"fas fa-times\"></i> Reject</button>' +
                '</div></td></tr>';"""

new_officer_loan_row = """            const client = appData.clients.find(c => c.id === l.clientId);
            const multiplier = (l.amount / client.savings).toFixed(1);
            const canApprove = l.amount <= client.savings * appData.config.savingsMultiplier;
            return '<tr><td><button class=\"btn btn-sm\" style=\"background:none;color:var(--info);text-decoration:underline;border:none;cursor:pointer;font-weight:700;padding:0;\" onclick=\"openLoanDetailModal(\\'' + l.id + '\\')\">' + l.id + '</button></td>' +
                '<td><strong>' + client.name + '</strong><br><small>' + client.phone + '</small></td>' +
                '<td>' + formatKES(l.amount) + '</td>' +
                '<td>' + l.purpose + '</td>' +
                '<td>' + l.duration + ' months</td>' +
                '<td>' + multiplier + 'x (' + (canApprove ? '<span style=\"color:var(--success)\">OK</span>' : '<span style=\"color:var(--danger)\">Exceeds</span>') + ')</td>' +
                '<td><div class=\"btn-group\">' +
                '<button class=\"btn btn-success btn-sm\" ' + (canApprove ? '' : 'disabled') + ' onclick=\"approveLoan(\\'' + l.id + '\\')"><i class=\"fas fa-check\"></i> Approve</button>' +
                '<button class=\"btn btn-danger btn-sm\" onclick=\"rejectLoan(\\'' + l.id + '\\')"><i class=\"fas fa-times\"></i> Reject</button>' +
                '</div></td></tr>';"""

html4 = html4.replace(old_officer_loan_row, new_officer_loan_row, 1)
print(f"F6 officer loan ID clickable: {old_officer_loan_row[:60] not in html4}")

# Step 4: Update renderAdminAllLoans to show Loan ID as clickable link (Feature 6)
old_admin_loan_row = "return '<tr><td>' + l.id + '</td><td>' + client.name + '</td><td>' + formatKES(l.amount) + '</td>'"
new_admin_loan_row = "return '<tr><td><button class=\"action-btn view\" onclick=\"openLoanDetailModal(\\'' + l.id + '\\')\" title=\"View Loan Details\" style=\"background:linear-gradient(135deg,#dde4f5,#c4d0f0);color:#3b5de7;\"><i class=\"fas fa-id-card\"></i></button> ' + l.id + '</td><td>' + client.name + '</td><td>' + formatKES(l.amount) + '</td>'"
html4 = html4.replace(old_admin_loan_row, new_admin_loan_row, 1)
print(f"F6 admin loan ID clickable: {old_admin_loan_row[:60] not in html4}")

# Step 5: Update renderGroupTransactionHistory rows to include Savings/Registration/Loan breakdown
# The new renderGroupView already shows the new breakdown columns
# But the row data needs to reflect savings/reg/loan breakdown from the transaction
# Update the history row rendering inside renderGroupView to use breakdown
old_hist_row = """            return '<tr><td><strong>' + row.txnId + '</strong></td><td>' + row.date + '</td><td>' + row.type + '</td>' +
                '<td>' + formatKES(row.totalAmount) + '</td><td>' + row.memberCount + '</td>' +
                '<td>' + formatKES(row.totalDistributed) + '</td><td>' + badge + '</td>' +
                '<td style="font-size:0.8rem;"><code>' + row.individualTxnIds + '</code></td></tr>';"""

new_hist_row = """            const savingsAmt = row.savingsAmount || (row.type === 'Savings Deposit' ? row.totalAmount : 0);
            const regAmt = row.registrationAmount || (row.type === 'Registration Fee Payment' ? row.totalAmount : 0);
            const loanAmt = row.loanAmount || (row.type === 'Loan Repayment' ? row.totalAmount : 0);
            return '<tr><td><strong>' + row.txnId + '</strong></td><td>' + row.date + '</td>' +
                '<td>' + formatKES(savingsAmt) + '</td><td>' + formatKES(regAmt) + '</td><td>' + formatKES(loanAmt) + '</td>' +
                '<td>' + formatKES(row.totalAmount) + '</td><td>' + row.memberCount + '</td>' +
                '<td>' + badge + '</td>' +
                '<td style="font-size:0.8rem;"><code>' + row.individualTxnIds + '</code></td></tr>';"""

html4 = html4.replace(old_hist_row, new_hist_row, 1)
print(f"F4 hist row breakdown: {old_hist_row[:60] not in html4}")

print(f"\nhtml4 length: {len(html4)}")
