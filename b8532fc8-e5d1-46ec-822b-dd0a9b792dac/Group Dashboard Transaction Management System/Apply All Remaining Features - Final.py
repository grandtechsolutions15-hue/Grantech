
# Starting from 'html' which has features 1 and 2 applied
# Apply features 3, 4, 5, 6 using exact text

html3 = html  # will accumulate all changes

# =========================================================================
# FEATURE 3: Monthly collections summary + date range report download
# =========================================================================
old_rpt_card = '''<div class="card">
                    <div class="card-header">
                        <h2 class="card-title"><i class="fas fa-chart-bar"></i> Reports</h2>
                        <div class="report-filters">
                            <select id="officer-report-type" onchange="updateOfficerReportPreview()">
                                <option value="all">All Activity</option>
                                <option value="loans">Loans</option>
                                <option value="savings">Savings</option>
                                <option value="clients">Clients</option>
                                <option value="groups">Groups</option>
                            </select>
                            <button class="btn btn-danger btn-sm" onclick="generateOfficerReportPDF()"><i class="fas fa-file-pdf"></i> Generate PDF</button>
                        </div>
                    </div>
                    <div id="officer-report-preview" style="max-height:400px;overflow-y:auto;"></div>
                </div>'''

new_rpt_card = '''<!-- Monthly Collections Summary Card -->
                <div class="card" id="officer-monthly-card">
                    <div class="card-header">
                        <h2 class="card-title"><i class="fas fa-calendar-alt"></i> Monthly Collections Summary</h2>
                        <button class="btn btn-success btn-sm" onclick="renderMonthlyCollectionSummary()"><i class="fas fa-sync-alt"></i> Refresh</button>
                    </div>
                    <div class="table-container">
                        <table>
                            <thead><tr><th>Month</th><th>Savings Collected (KES)</th><th>Registration Collected (KES)</th><th>Total (KES)</th></tr></thead>
                            <tbody id="officer-monthly-summary-table"><tr><td colspan="4" class="empty-state"><p>Click Refresh to load monthly data</p></td></tr></tbody>
                        </table>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title"><i class="fas fa-chart-bar"></i> Reports &amp; Downloads</h2>
                        <div class="report-filters">
                            <select id="officer-report-type" onchange="updateOfficerReportPreview()">
                                <option value="all">All Activity</option>
                                <option value="loans">Loans</option>
                                <option value="savings">Savings</option>
                                <option value="clients">Clients</option>
                                <option value="groups">Groups</option>
                                <option value="monthly_collections">Monthly Collections</option>
                            </select>
                            <div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin-top:6px;">
                                <label style="font-size:0.82rem;color:#666;">From:</label>
                                <input type="month" id="officer-report-from" style="padding:6px 10px;border:2px solid #e8e8e8;border-radius:8px;font-size:0.82rem;">
                                <label style="font-size:0.82rem;color:#666;">To:</label>
                                <input type="month" id="officer-report-to" style="padding:6px 10px;border:2px solid #e8e8e8;border-radius:8px;font-size:0.82rem;">
                                <button class="btn btn-danger btn-sm" onclick="generateOfficerReportPDF()"><i class="fas fa-file-pdf"></i> Download Report</button>
                            </div>
                        </div>
                    </div>
                    <div id="officer-report-preview" style="max-height:400px;overflow-y:auto;"></div>
                </div>'''

html3 = html3.replace(old_rpt_card, new_rpt_card, 1)
print(f"Feature 3: {old_rpt_card[:50] not in html3}")

# =========================================================================
# FEATURE 4: Transaction columns: Savings, Registration, Loan (not alternatives)
# =========================================================================

# Fix group transaction form - replace amount+type with 3 separate columns
old_txn_form_block = '''                            <div class="floating-input-group">
                                <input type="number" id="group-transaction-amount" placeholder=" " oninput="updateGroupTransactionPreview()">
                                <label>Total Amount (KES)</label>
                            </div>
                            <div class="floating-input-group">
                                <select id="group-transaction-type" onchange="updateGroupTransactionPreview()">
                                    <option value="Savings Deposit">Savings Deposit</option>
                                    <option value="Loan Repayment">Loan Repayment</option>
                                    <option value="Registration Fee Payment">Registration Fee Payment</option>
                                </select>
                                <label>Transaction Type</label>
                            </div>'''

new_txn_form_block = '''                            <div class="floating-input-group">
                                <input type="number" id="group-transaction-savings" placeholder=" " min="0" oninput="updateGroupTransactionPreview()">
                                <label>Savings (KES)</label>
                            </div>
                            <div class="floating-input-group">
                                <input type="number" id="group-transaction-registration" placeholder=" " min="0" oninput="updateGroupTransactionPreview()">
                                <label>Registration (KES)</label>
                            </div>
                            <div class="floating-input-group">
                                <input type="number" id="group-transaction-loan" placeholder=" " min="0" oninput="updateGroupTransactionPreview()">
                                <label>Loan Repayment (KES)</label>
                            </div>
                            <input type="hidden" id="group-transaction-amount" value="0">
                            <input type="hidden" id="group-transaction-type" value="Combined">'''

html3 = html3.replace(old_txn_form_block, new_txn_form_block, 1)
print(f"Feature 4 form: {old_txn_form_block[:60] not in html3}")

# Update group history table header to show Savings/Registration/Loan columns
old_gth_hdr = '''                                    <th>Group Transaction ID</th>
                                    <th>Date</th>
                                    <th>Type</th>
                                    <th>Total Amount</th>
                                    <th>Member Count</th>
                                    <th>Total Distributed</th>
                                    <th>Status</th>
                                    <th>Individual Transaction IDs</th>'''

new_gth_hdr = '''                                    <th>Group Transaction ID</th>
                                    <th>Date</th>
                                    <th>Savings (KES)</th>
                                    <th>Registration (KES)</th>
                                    <th>Loan Repayment (KES)</th>
                                    <th>Total (KES)</th>
                                    <th>Members</th>
                                    <th>Status</th>
                                    <th>Individual IDs</th>'''

html3 = html3.replace(old_gth_hdr, new_gth_hdr, 1)
print(f"Feature 4 table header: {old_gth_hdr[:60] not in html3}")

# =========================================================================
# FEATURE 5: Remove GROUP login tab; officer/admin view group with full details
# =========================================================================

# Remove group login tab button
old_group_tab_btn = '<button class="login-tab active" onclick="switchLoginTab(\'group\')" id="login-tab-group"><i class="fas fa-users"></i> Group</button>'
new_group_tab_btn = ''
html3 = html3.replace(old_group_tab_btn, new_group_tab_btn, 1)
print(f"Feature 5 remove group tab: {old_group_tab_btn[:60] not in html3}")

# Make officer tab active by default instead
old_officer_tab = '<button class="login-tab" onclick="switchLoginTab(\'officer\')" id="login-tab-officer"><i class="fas fa-user-tie"></i> Officer</button>'
new_officer_tab = '<button class="login-tab active" onclick="switchLoginTab(\'officer\')" id="login-tab-officer"><i class="fas fa-user-tie"></i> Officer</button>'
html3 = html3.replace(old_officer_tab, new_officer_tab, 1)
print(f"Feature 5 officer tab active: {old_officer_tab[:60] not in html3}")

# Make officer login form active by default, hide group form
old_group_form_active = '<form class="login-form active" id="login-form-group" onsubmit="handleLogin(event, \'group\')">'
new_group_form_active = '<form class="login-form" id="login-form-group" onsubmit="handleLogin(event, \'group\')" style="display:none!important;">'
html3 = html3.replace(old_group_form_active, new_group_form_active, 1)
print(f"Feature 5 hide group form: {old_group_form_active[:60] not in html3}")

# Make officer login form active by default
old_officer_form = '<form class="login-form" id="login-form-officer" onsubmit="handleLogin(event, \'officer\')">'
new_officer_form = '<form class="login-form active" id="login-form-officer" onsubmit="handleLogin(event, \'officer\')">'
html3 = html3.replace(old_officer_form, new_officer_form, 1)
print(f"Feature 5 officer form active: {old_officer_form[:60] not in html3}")

# Add "View Group" button with full details to admin groups table (enhance renderAdminGroups)
old_admin_groups_render = ''''<td><div class="action-btns">' +
                '<button class="action-btn edit" onclick="openEditGroup(\\'' + g.id + '\\')\" title=\"Edit\"><i class="fas fa-edit"></i></button>' +
                '<button class="action-btn delete" onclick="confirmDeleteGroup(\\'' + g.id + '\\')\" title=\"Delete\"><i class="fas fa-trash"></i></button>' +
                '</div></td></tr>';'''

new_admin_groups_render = ''''<td><div class="action-btns">' +
                '<button class="action-btn view" onclick="openGroupDetailView(\\'' + g.id + '\\')" title="View Group"><i class="fas fa-eye"></i></button>' +
                '<button class="action-btn edit" onclick="openEditGroup(\\'' + g.id + '\\')\" title=\"Edit\"><i class="fas fa-edit"></i></button>' +
                '<button class="action-btn delete" onclick="confirmDeleteGroup(\\'' + g.id + '\\')\" title=\"Delete\"><i class="fas fa-trash"></i></button>' +
                '</div></td></tr>';'''

html3 = html3.replace(old_admin_groups_render, new_admin_groups_render, 1)
print(f"Feature 5 admin view group btn: {old_admin_groups_render[:60] not in html3}")

# =========================================================================
# FEATURE 6: Loan ID generation + clickable Loan ID in officer & admin tables
# =========================================================================

# Update officer loan apps table to show Loan ID as first column
old_officer_loans_hdr = '<table>\n                            <thead><tr><th>Client</th><th>Amount</th><th>Purpose</th><th>Duration</th><th>Savings Multiplier</th><th>Actions</th></tr></thead>\n                            <tbody id="officer-loan-apps"></tbody>'
new_officer_loans_hdr = '<table>\n                            <thead><tr><th>Loan ID</th><th>Client</th><th>Amount</th><th>Purpose</th><th>Duration</th><th>Savings Multiplier</th><th>Actions</th></tr></thead>\n                            <tbody id="officer-loan-apps"></tbody>'
html3 = html3.replace(old_officer_loans_hdr, new_officer_loans_hdr, 1)
print(f"Feature 6 officer loans hdr: {old_officer_loans_hdr[:60] not in html3}")

print(f"\nFinal HTML length: {len(html3)}")
