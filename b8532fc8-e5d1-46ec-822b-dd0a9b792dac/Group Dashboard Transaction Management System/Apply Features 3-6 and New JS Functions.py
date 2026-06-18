
# The 'html' variable already has features 1 and 2 partially applied (edit btn is already there from previous block)
# Now apply remaining features

# =========================================================================
# FEATURE 3: Officer sees savings collected & registration collected per month
# Add monthly summary section + date-range report download
# =========================================================================

# Insert monthly summary card BEFORE the Reports card in officer section
# The officer section ends just before <!-- ADMIN SECTION -->
# We insert a new monthly summary card before the reports card

old_officer_reports_card = '''<div class="card">
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

new_officer_reports_card = '''<!-- Monthly Savings & Registration Summary -->
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title"><i class="fas fa-calendar-alt"></i> Monthly Collections Summary</h2>
                        <button class="btn btn-success btn-sm" onclick="renderMonthlyCollectionSummary()"><i class="fas fa-sync-alt"></i> Refresh</button>
                    </div>
                    <div class="table-container">
                        <table>
                            <thead><tr><th>Month</th><th>Savings Collected (KES)</th><th>Registration Collected (KES)</th><th>Total (KES)</th></tr></thead>
                            <tbody id="officer-monthly-summary-table"></tbody>
                        </table>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title"><i class="fas fa-chart-bar"></i> Reports</h2>
                        <div class="report-filters">
                            <select id="officer-report-type" onchange="updateOfficerReportPreview()">
                                <option value="all">All Activity</option>
                                <option value="loans">Loans</option>
                                <option value="savings">Savings</option>
                                <option value="clients">Clients</option>
                                <option value="groups">Groups</option>
                                <option value="monthly_collections">Monthly Collections</option>
                            </select>
                            <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
                                <label style="font-size:0.85rem;color:#666;">From:</label>
                                <input type="month" id="officer-report-from" style="padding:6px 10px;border:2px solid #e8e8e8;border-radius:8px;font-size:0.85rem;">
                                <label style="font-size:0.85rem;color:#666;">To:</label>
                                <input type="month" id="officer-report-to" style="padding:6px 10px;border:2px solid #e8e8e8;border-radius:8px;font-size:0.85rem;">
                                <button class="btn btn-danger btn-sm" onclick="generateOfficerReportPDF()"><i class="fas fa-file-pdf"></i> Download Report</button>
                            </div>
                        </div>
                    </div>
                    <div id="officer-report-preview" style="max-height:400px;overflow-y:auto;"></div>
                </div>'''

html2 = html.replace(old_officer_reports_card, new_officer_reports_card, 1)
print("Feature 3 HTML:", old_officer_reports_card[:60] not in html2)

# =========================================================================
# FEATURE 4: Transaction recording columns: Savings, Registration, Loan (not alternatives)
# Update group transaction form to have 3 amount inputs instead of a type selector
# =========================================================================

old_group_txn_type_block = '''<div class="floating-input-group">
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

new_group_txn_type_block = '''<div class="floating-input-group">
                                <input type="number" id="group-transaction-savings" placeholder=" " min="0" oninput="updateGroupTransactionPreview()">
                                <label>Savings Amount (KES)</label>
                            </div>
                            <div class="floating-input-group">
                                <input type="number" id="group-transaction-registration" placeholder=" " min="0" oninput="updateGroupTransactionPreview()">
                                <label>Registration Amount (KES)</label>
                            </div>
                            <div class="floating-input-group">
                                <input type="number" id="group-transaction-loan" placeholder=" " min="0" oninput="updateGroupTransactionPreview()">
                                <label>Loan Repayment (KES)</label>
                            </div>
                            <!-- Keep hidden total and type for backward compat -->
                            <input type="hidden" id="group-transaction-amount" value="0">
                            <input type="hidden" id="group-transaction-type" value="Combined">'''

html2 = html2.replace(old_group_txn_type_block, new_group_txn_type_block, 1)
print("Feature 4 form:", old_group_txn_type_block[:60] not in html2)

# Update group history table to show Savings/Registration/Loan columns (Feature 4)
# Update the group transaction history table header
old_gth_header2 = new_gth_header.strip()  # the header we already changed in feature 1 - we need to add more columns
# The header was already changed to include Status. Now update Total Amount → show breakdown columns
old_gth_header_f4 = '''<th>Group Transaction ID</th>
                                    <th>Date</th>
                                    <th>Type</th>
                                    <th>Total Amount</th>
                                    <th>Member Count</th>
                                    <th>Total Distributed</th>
                                    <th>Status</th>
                                    <th>Individual Transaction IDs</th>'''

new_gth_header_f4 = '''<th>Group Transaction ID</th>
                                    <th>Date</th>
                                    <th>Savings (KES)</th>
                                    <th>Registration (KES)</th>
                                    <th>Loan Repayment (KES)</th>
                                    <th>Total Amount</th>
                                    <th>Members</th>
                                    <th>Status</th>
                                    <th>Individual Transaction IDs</th>'''

html2 = html2.replace(old_gth_header_f4, new_gth_header_f4, 1)
print("Feature 4 table header:", old_gth_header_f4[:60] not in html2)

print("HTML length after features 3-4:", len(html2))
