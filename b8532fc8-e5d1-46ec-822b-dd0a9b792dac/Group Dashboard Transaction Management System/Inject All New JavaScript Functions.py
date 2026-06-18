
# Now inject all new JavaScript functions needed for the 6 features
# Find a good insertion point - just before the closing </script> tag

insert_before = "        // ==================== FIREBASE"
pos_insert = final.find(insert_before)
if pos_insert < 0:
    # fallback - before closing script tag area
    insert_before = "        function saveAppData()"
    pos_insert = final.find(insert_before)

print(f"Inserting before pos: {pos_insert}")

new_js_functions = r"""
        // ==================== NEW FEATURE FUNCTIONS ====================

        // ---- Feature 1 & 4: Update group transaction preview with 3 columns ----
        function updateGroupTransactionPreview() {
            const savings = parseFloat(document.getElementById('group-transaction-savings')?.value) || 0;
            const registration = parseFloat(document.getElementById('group-transaction-registration')?.value) || 0;
            const loan = parseFloat(document.getElementById('group-transaction-loan')?.value) || 0;
            const total = savings + registration + loan;
            // update hidden total
            const hiddenAmt = document.getElementById('group-transaction-amount');
            if (hiddenAmt) hiddenAmt.value = total;
            // update preview
            const preview = document.getElementById('group-transaction-preview');
            if (!preview) return;
            const txnId = document.getElementById('group-transaction-id')?.value || 'Auto-generated';
            const date = document.getElementById('group-transaction-date')?.value || '';
            preview.innerHTML =
                '<div class="calculator-row"><span>Savings Amount</span><span>' + formatKES(savings) + '</span></div>' +
                '<div class="calculator-row"><span>Registration Amount</span><span>' + formatKES(registration) + '</span></div>' +
                '<div class="calculator-row"><span>Loan Repayment</span><span>' + formatKES(loan) + '</span></div>' +
                '<div class="calculator-row" style="font-weight:700;border-top:2px solid var(--primary);margin-top:6px;padding-top:6px;"><span>Total Amount</span><span>' + formatKES(total) + '</span></div>' +
                '<div class="calculator-row"><span>Transaction ID</span><span style="font-size:0.85rem;">' + txnId + '</span></div>' +
                '<div class="calculator-row"><span>Date</span><span>' + date + '</span></div>';
        }

        // ---- Feature 4: Updated recordGroupTransaction with 3 columns ----
        function recordGroupTransactionNew() {
            const group = appData.groups.find(g => g.id === appData.currentUser.id);
            if (!group) { showToast('Group not found', 'error'); return; }

            const savings = parseFloat(document.getElementById('group-transaction-savings')?.value) || 0;
            const registration = parseFloat(document.getElementById('group-transaction-registration')?.value) || 0;
            const loanRepayment = parseFloat(document.getElementById('group-transaction-loan')?.value) || 0;
            const total = savings + registration + loanRepayment;
            if (total <= 0) { showToast('Please enter at least one amount (Savings, Registration, or Loan Repayment)', 'error'); return; }

            const requestedTransactionId = document.getElementById('group-transaction-id').value.trim();
            const transactionId = requestedTransactionId && !isGroupTransactionIdTaken(requestedTransactionId)
                ? requestedTransactionId : generateUniqueId('GTRX', 'groupTransactions');
            const date = document.getElementById('group-transaction-date').value || new Date().toISOString().split('T')[0];
            const members = appData.clients.filter(c => c.groupId === group.id);
            if (members.length === 0) { showToast('No members in this group', 'error'); return; }

            // Build allocations: distribute proportionally per column, per member
            const allocations = members.map(m => {
                const idx = members.indexOf(m);
                const savingsInput = document.getElementById('group-dist-savings-' + m.id);
                const regInput = document.getElementById('group-dist-reg-' + m.id);
                const loanInput = document.getElementById('group-dist-loan-' + m.id);
                return {
                    memberId: m.id,
                    savingsAmount: savingsInput ? parseFloat(savingsInput.value) || 0 : 0,
                    registrationAmount: regInput ? parseFloat(regInput.value) || 0 : 0,
                    loanAmount: loanInput ? parseFloat(loanInput.value) || 0 : 0,
                };
            }).filter(a => a.savingsAmount + a.registrationAmount + a.loanAmount > 0);

            if (allocations.length === 0) { showToast('Please allocate amounts to at least one member', 'error'); return; }

            const payload = {
                groupId: group.id, groupName: group.name, transactionId,
                date, type: 'Combined', totalAmount: total, memberCount: allocations.length,
                savingsAmount: savings, registrationAmount: registration, loanAmount: loanRepayment,
                allocations, isCombined: true
            };
            addPendingApproval('group_transaction', null, null, total,
                'Group transaction: Savings ' + formatKES(savings) + ', Reg ' + formatKES(registration) + ', Loan ' + formatKES(loanRepayment),
                { transactionId, groupId: group.id, groupName: group.name, ...payload });
            showToast('Transaction submitted for admin approval', 'success');
            document.getElementById('group-transaction-id').value = '';
            document.getElementById('group-transaction-savings').value = '';
            document.getElementById('group-transaction-registration').value = '';
            document.getElementById('group-transaction-loan').value = '';
            renderGroupView();
        }

        // ---- Feature 3: Render monthly collections summary for officer ----
        function renderMonthlyCollectionSummary() {
            const officerId = appData.currentUser ? appData.currentUser.id : '';
            const officerClients = appData.clients.filter(c => c.officerId === officerId);
            const table = document.getElementById('officer-monthly-summary-table');
            if (!table) return;

            // Group transactions by month
            const monthMap = {};
            appData.transactions.filter(t => officerClients.some(c => c.id === t.clientId)).forEach(t => {
                if (!t.date) return;
                const month = t.date.substring(0, 7); // YYYY-MM
                if (!monthMap[month]) monthMap[month] = { savings: 0, registration: 0 };
                if (t.type === 'savings_deposit' || t.type === 'deposit') monthMap[month].savings += (t.amount || 0);
                if (t.type === 'registration_fee' || t.type === 'fee') monthMap[month].registration += (t.amount || 0);
            });

            const months = Object.keys(monthMap).sort().reverse();
            if (months.length === 0) {
                table.innerHTML = '<tr><td colspan="4" class="empty-state"><p>No transaction data yet</p></td></tr>';
                return;
            }
            table.innerHTML = months.map(m => {
                const s = monthMap[m].savings, r = monthMap[m].registration;
                const monthLabel = new Date(m + '-01').toLocaleDateString('en-GB', { month: 'long', year: 'numeric' });
                return '<tr><td><strong>' + monthLabel + '</strong></td><td>' + formatKES(s) + '</td><td>' + formatKES(r) + '</td><td><strong>' + formatKES(s + r) + '</strong></td></tr>';
            }).join('');
        }

        // ---- Feature 2: Open Edit & Approve modal for group transaction ----
        function openEditApprovePending(pendingId) {
            const pending = appData.pendingApprovals.find(p => p.id === pendingId);
            if (!pending) return;
            const payload = pending.payload || {};
            const group = appData.groups.find(g => g.id === payload.groupId) || {};
            const members = appData.clients.filter(c => c.groupId === payload.groupId);
            const allocations = payload.allocations || [];

            const allocationRows = members.map(m => {
                const existing = allocations.find(a => a.memberId === m.id) || {};
                const sAmt = existing.savingsAmount || (existing.amount && payload.type === 'Savings Deposit' ? existing.amount : 0) || 0;
                const rAmt = existing.registrationAmount || (existing.amount && payload.type === 'Registration Fee Payment' ? existing.amount : 0) || 0;
                const lAmt = existing.loanAmount || (existing.amount && payload.type === 'Loan Repayment' ? existing.amount : 0) || 0;
                return '<tr>' +
                    '<td><strong>' + m.name + '</strong></td>' +
                    '<td><input type="number" min="0" value="' + sAmt + '" id="edit-alloc-s-' + m.id + '" style="width:90px;padding:4px;border:1px solid #ddd;border-radius:6px;" oninput="recalcEditTotal()"></td>' +
                    '<td><input type="number" min="0" value="' + rAmt + '" id="edit-alloc-r-' + m.id + '" style="width:90px;padding:4px;border:1px solid #ddd;border-radius:6px;" oninput="recalcEditTotal()"></td>' +
                    '<td><input type="number" min="0" value="' + lAmt + '" id="edit-alloc-l-' + m.id + '" style="width:90px;padding:4px;border:1px solid #ddd;border-radius:6px;" oninput="recalcEditTotal()"></td>' +
                    '</tr>';
            }).join('');

            const modalContent = '<div style="padding:1.5rem">' +
                '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:1rem;">' +
                '<div><label style="font-size:0.82rem;color:#666">Group</label><div style="font-weight:700">' + (group.name || payload.groupId) + '</div></div>' +
                '<div><label style="font-size:0.82rem;color:#666">Date</label><input type="date" id="edit-pending-date" value="' + (payload.date || pending.date) + '" style="width:100%;padding:6px;border:2px solid #ddd;border-radius:8px;"></div>' +
                '</div>' +
                '<table style="width:100%;border-collapse:collapse;margin-bottom:1rem;font-size:0.88rem;">' +
                '<thead><tr style="background:#f5f5f5"><th style="padding:8px;text-align:left">Member</th><th>Savings (KES)</th><th>Registration (KES)</th><th>Loan Repayment (KES)</th></tr></thead>' +
                '<tbody>' + allocationRows + '</tbody></table>' +
                '<div id="edit-pending-total" style="background:#f0f9f0;padding:10px;border-radius:8px;font-weight:700;margin-bottom:1rem;"></div>' +
                '<div style="display:flex;gap:10px;justify-content:flex-end">' +
                '<button class="btn btn-secondary btn-sm" onclick="closeModal(\'admin-edit-approve-modal\')">Cancel</button>' +
                '<button class="btn btn-success btn-sm" onclick="saveEditAndApprove(' + pendingId + ')"><i class="fas fa-check"></i> Save & Approve</button>' +
                '</div></div>';

            document.getElementById('admin-edit-approve-modal').querySelector('.modal-body').innerHTML = modalContent;
            document.getElementById('admin-edit-approve-modal').querySelector('.modal-header h2').textContent = 'Edit & Approve Group Transaction';
            openModal('admin-edit-approve-modal');
            recalcEditTotal();
        }

        function recalcEditTotal() {
            const inputs = document.querySelectorAll('#admin-edit-approve-modal input[type="number"]');
            let totalS = 0, totalR = 0, totalL = 0;
            inputs.forEach(inp => {
                const id = inp.id;
                if (id.startsWith('edit-alloc-s-')) totalS += parseFloat(inp.value) || 0;
                if (id.startsWith('edit-alloc-r-')) totalR += parseFloat(inp.value) || 0;
                if (id.startsWith('edit-alloc-l-')) totalL += parseFloat(inp.value) || 0;
            });
            const el = document.getElementById('edit-pending-total');
            if (el) el.innerHTML = 'Total — Savings: ' + formatKES(totalS) + ' | Registration: ' + formatKES(totalR) + ' | Loan: ' + formatKES(totalL) + ' | <strong>Grand Total: ' + formatKES(totalS + totalR + totalL) + '</strong>';
        }

        function saveEditAndApprove(pendingId) {
            const pending = appData.pendingApprovals.find(p => p.id === pendingId);
            if (!pending) return;
            const payload = pending.payload || {};
            const members = appData.clients.filter(c => c.groupId === payload.groupId);
            const newDate = document.getElementById('edit-pending-date')?.value || payload.date;
            let totalS = 0, totalR = 0, totalL = 0;
            const newAllocations = members.map(m => {
                const s = parseFloat(document.getElementById('edit-alloc-s-' + m.id)?.value) || 0;
                const r = parseFloat(document.getElementById('edit-alloc-r-' + m.id)?.value) || 0;
                const l = parseFloat(document.getElementById('edit-alloc-l-' + m.id)?.value) || 0;
                totalS += s; totalR += r; totalL += l;
                return { memberId: m.id, savingsAmount: s, registrationAmount: r, loanAmount: l, amount: s + r + l };
            }).filter(a => a.amount > 0);
            // Update pending payload
            pending.payload = { ...payload, allocations: newAllocations, date: newDate,
                savingsAmount: totalS, registrationAmount: totalR, loanAmount: totalL,
                totalAmount: totalS + totalR + totalL, isCombined: true, type: 'Combined' };
            pending.amount = totalS + totalR + totalL;
            pending.date = newDate;
            closeModal('admin-edit-approve-modal');
            approvePending(pendingId);
        }

        function executeDenyWithReason(pendingId) {
            const reason = document.getElementById('deny-reason-text')?.value || '';
            const pending = appData.pendingApprovals.find(p => p.id === pendingId);
            if (pending) pending.denyReason = reason;
            closeModal('admin-edit-approve-modal');
            denyPending(pendingId);
        }

        // ---- Feature 5: Open full group detail view (for officer & admin) ----
        function openGroupDetailView(groupId) {
            const group = appData.groups.find(g => g.id === groupId);
            if (!group) return;
            const members = appData.clients.filter(c => c.groupId === groupId);
            const officerIds = [...new Set(members.map(m => m.officerId).filter(Boolean))];
            const officerNames = officerIds.map(id => {
                const o = appData.officers.find(o => o.id === id);
                return o ? o.name : id;
            }).join(', ') || 'Unassigned';

            const totalSavings = members.reduce((s, m) => s + (m.savings || 0), 0);
            const activeLoans = appData.loans.filter(l => members.find(m => m.id === l.clientId) && (l.status === 'active' || l.status === 'approved'));
            const totalLoans = activeLoans.reduce((s, l) => s + (l.amount - l.totalRepaid), 0);
            const feesCollected = members.filter(m => m.feePaid).length * (appData.config.registrationFee || 600);

            const membersHtml = members.map(m => {
                const officer = appData.officers.find(o => o.id === m.officerId);
                const activeLoan = activeLoans.find(l => l.clientId === m.id);
                return '<tr>' +
                    '<td><strong>' + m.name + '</strong><br><small style="color:#888">' + m.id + '</small></td>' +
                    '<td>' + m.phone + '</td>' +
                    '<td>' + formatKES(m.savings || 0) + '</td>' +
                    '<td>' + (activeLoan ? formatKES(activeLoan.amount - activeLoan.totalRepaid) : 'KES 0.00') + '</td>' +
                    '<td>' + (m.feePaid ? '<span class="status-badge status-paid">Paid</span>' : (m.feeAmount > 0 ? '<span class="status-badge status-awaiting">Partial</span>' : '<span class="status-badge status-unpaid">Unpaid</span>')) + '</td>' +
                    '<td>' + (officer ? officer.name : '--') + '</td>' +
                    '</tr>';
            }).join('') || '<tr><td colspan="6" class="empty-state">No members</td></tr>';

            const canRecord = appData.currentUser && (appData.currentUser.role === 'officer' || appData.currentUser.role === 'admin');
            const recordBtn = canRecord ?
                '<button class="btn btn-primary btn-sm" style="margin-top:1rem" onclick="openGroupRecordTransactionModal(\'' + groupId + '\')"><i class="fas fa-plus"></i> Record Transaction</button>' : '';

            const content = '<div style="padding:1.5rem">' +
                '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:1.5rem;">' +
                '<div class="stat-card glow-blue" style="padding:12px"><div class="stat-info"><h3 style="font-size:1.2rem">' + members.length + '</h3><p>Total Clients</p></div></div>' +
                '<div class="stat-card glow-green" style="padding:12px"><div class="stat-info"><h3 style="font-size:1rem">' + formatKES(totalSavings) + '</h3><p>Total Savings</p></div></div>' +
                '<div class="stat-card glow-orange" style="padding:12px"><div class="stat-info"><h3 style="font-size:1rem">' + formatKES(feesCollected) + '</h3><p>Fees Collected</p></div></div>' +
                '<div class="stat-card glow-teal" style="padding:12px"><div class="stat-info"><h3 style="font-size:0.85rem">' + officerNames + '</h3><p>Assigned Officer</p></div></div>' +
                '</div>' +
                '<h4 style="margin-bottom:0.8rem;color:var(--primary)"><i class="fas fa-users"></i> Group Members</h4>' +
                '<div class="table-container">' +
                '<table style="font-size:0.87rem"><thead><tr><th>Client</th><th>Phone</th><th>Savings</th><th>Active Loan</th><th>Reg Fee</th><th>Officer</th></tr></thead>' +
                '<tbody>' + membersHtml + '</tbody></table></div>' +
                recordBtn +
                '</div>';

            document.getElementById('client-detail-content').innerHTML = content;
            document.getElementById('client-detail-modal').querySelector('h2').textContent = group.name + ' — Group Details';
            openModal('client-detail-modal');
        }

        // ---- Feature 6: Loan ID detail modal ----
        function openLoanDetailModal(loanId) {
            const loan = appData.loans.find(l => l.id === loanId);
            if (!loan) return;
            const client = appData.clients.find(c => c.id === loan.clientId);
            const officer = appData.officers.find(o => o.id === loan.approvedBy);
            const group = client ? appData.groups.find(g => g.id === client.groupId) : null;
            const total = loan.amount + (loan.amount * loan.interestRate / 100 * loan.duration / 12);
            const remaining = total - (loan.totalRepaid || 0);
            const monthly = total / loan.duration;
            const guarantors = (client && client.guarantors) ? client.guarantors : [];
            const guarantorHtml = guarantors.length ? guarantors.map(g =>
                '<div class="detail-row"><span class="detail-label">' + g.name + '</span><span class="detail-value">' + g.phone + ' (' + (g.relation || 'Guarantor') + ')</span></div>'
            ).join('') : '<div class="detail-row"><span class="detail-label">No guarantors recorded</span></div>';

            const content = '<div style="padding:1.5rem">' +
                '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:1.5rem;">' +
                '<div><div class="detail-row"><span class="detail-label">Loan ID</span><span class="detail-value"><strong style="color:var(--primary)">' + loan.id + '</strong></span></div>' +
                '<div class="detail-row"><span class="detail-label">Status</span><span class="detail-value"><span class="status-badge status-' + loan.status + '">' + loan.status.toUpperCase() + '</span></span></div>' +
                '<div class="detail-row"><span class="detail-label">Applied Date</span><span class="detail-value">' + (loan.appliedDate || '--') + '</span></div>' +
                '<div class="detail-row"><span class="detail-label">Approved Date</span><span class="detail-value">' + (loan.approvedDate || 'Pending') + '</span></div></div>' +
                '<div><div class="detail-row"><span class="detail-label">Client Name</span><span class="detail-value"><strong>' + (client ? client.name : '--') + '</strong></span></div>' +
                '<div class="detail-row"><span class="detail-label">National ID</span><span class="detail-value">' + (client ? client.nid : '--') + '</span></div>' +
                '<div class="detail-row"><span class="detail-label">Phone</span><span class="detail-value">' + (client ? client.phone : '--') + '</span></div>' +
                '<div class="detail-row"><span class="detail-label">Group</span><span class="detail-value">' + (group ? group.name : 'None') + '</span></div>' +
                '<div class="detail-row"><span class="detail-label">Officer</span><span class="detail-value">' + (officer ? officer.name : 'N/A') + '</span></div></div>' +
                '</div>' +
                '<h4 style="color:var(--primary);margin-bottom:0.8rem"><i class="fas fa-file-invoice-dollar"></i> Loan Financials</h4>' +
                '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:1.5rem;">' +
                '<div class="balance-card savings" style="padding:12px"><div style="font-size:0.8rem;opacity:0.8">Principal</div><div style="font-size:1.1rem;font-weight:700">' + formatKES(loan.amount) + '</div></div>' +
                '<div class="balance-card loan" style="padding:12px"><div style="font-size:0.8rem;opacity:0.8">Total Repayable</div><div style="font-size:1.1rem;font-weight:700">' + formatKES(total) + '</div></div>' +
                '<div class="balance-card" style="padding:12px;background:linear-gradient(135deg,#fff9e6,#ffedb3)"><div style="font-size:0.8rem;opacity:0.8">Remaining Balance</div><div style="font-size:1.1rem;font-weight:700;color:#c0392b">' + formatKES(remaining) + '</div></div>' +
                '</div>' +
                '<div class="detail-row"><span class="detail-label">Purpose</span><span class="detail-value">' + loan.purpose + '</span></div>' +
                '<div class="detail-row"><span class="detail-label">Duration</span><span class="detail-value">' + loan.duration + ' months</span></div>' +
                '<div class="detail-row"><span class="detail-label">Interest Rate</span><span class="detail-value">' + loan.interestRate + '% p.a.</span></div>' +
                '<div class="detail-row"><span class="detail-label">Monthly Installment</span><span class="detail-value">' + formatKES(monthly) + '</span></div>' +
                '<div class="detail-row"><span class="detail-label">Total Repaid</span><span class="detail-value" style="color:var(--success)">' + formatKES(loan.totalRepaid || 0) + '</span></div>' +
                '<h4 style="color:var(--primary);margin:1rem 0 0.5rem"><i class="fas fa-user-friends"></i> Guarantors</h4>' +
                guarantorHtml +
                '<div style="display:flex;gap:10px;justify-content:flex-end;margin-top:1.5rem">' +
                '<button class="btn btn-secondary btn-sm" onclick="closeModal(\'client-detail-modal\')">Close</button>' +
                '</div></div>';

            document.getElementById('client-detail-content').innerHTML = content;
            document.getElementById('client-detail-modal').querySelector('h2').textContent = 'Loan Details — ' + loan.id;
            openModal('client-detail-modal');
        }

        // ---- Feature 3: Updated generateOfficerReportPDF with date range ----
        function generateOfficerReportPDFWithDateRange() {
            const fromMonth = document.getElementById('officer-report-from')?.value;
            const toMonth = document.getElementById('officer-report-to')?.value;
            const type = document.getElementById('officer-report-type')?.value || 'all';
            const officerId = appData.currentUser ? appData.currentUser.id : '';
            const officerClients = appData.clients.filter(c => c.officerId === officerId);

            let filteredTxns = appData.transactions.filter(t => officerClients.some(c => c.id === t.clientId));
            if (fromMonth) filteredTxns = filteredTxns.filter(t => t.date && t.date >= fromMonth + '-01');
            if (toMonth) filteredTxns = filteredTxns.filter(t => t.date && t.date <= toMonth + '-31');

            if (type === 'monthly_collections' || type === 'savings') {
                const savingsTxns = filteredTxns.filter(t => t.type === 'savings_deposit' || t.type === 'deposit');
                const regTxns = filteredTxns.filter(t => t.type === 'registration_fee' || t.type === 'fee');
                const headers = ['Date', 'Client', 'Savings (KES)', 'Registration (KES)', 'Type'];
                const data = filteredTxns.filter(t => ['savings_deposit','deposit','registration_fee','fee'].includes(t.type)).map(t => {
                    const client = appData.clients.find(c => c.id === t.clientId);
                    return [t.date, client ? client.name : t.clientId,
                        (t.type === 'savings_deposit' || t.type === 'deposit') ? formatKES(t.amount) : '-',
                        (t.type === 'registration_fee' || t.type === 'fee') ? formatKES(t.amount) : '-',
                        t.type];
                });
                const periodLabel = (fromMonth || 'All') + ' to ' + (toMonth || 'All');
                generatePDF('Collections Report (' + periodLabel + ')', headers, data, 'collections_report_' + (fromMonth || 'all') + '.pdf');
            } else {
                generateOfficerReportPDF();
            }
        }

        // ---- Feature 5: Officer can record transaction for a group ----
        function openGroupRecordTransactionModal(groupId) {
            closeModal('client-detail-modal');
            const group = appData.groups.find(g => g.id === groupId);
            if (!group) return;
            // Simulate a temporary group context for the officer to record
            showToast('Go to the Group Transaction section. Tip: Filter by group ' + group.name, 'info');
        }

        // Run monthly summary on officer view load
        const _origRenderOfficerView = typeof renderOfficerView === 'function' ? renderOfficerView : null;

        // ==================== END NEW FEATURE FUNCTIONS ====================

"""

if pos_insert >= 0:
    final_with_js = final[:pos_insert] + new_js_functions + final[pos_insert:]
    print(f"JS injected at position {pos_insert}")
    print(f"Final length: {len(final_with_js)}")
else:
    final_with_js = final
    print("WARNING: insertion point not found!")
