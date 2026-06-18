
# Fix the two remaining issues and add all new JS functions
# Work from html3

final = html3

# ---- Fix F2: confirmDenyPending - use index-based replacement ----
pos_cd = final.find("function confirmDenyPending(pendingId) {")
if pos_cd >= 0:
    # replace signature only - just add showReason parameter
    final = final[:pos_cd] + "function confirmDenyPending(pendingId, showReason) {" + final[pos_cd + len("function confirmDenyPending(pendingId) {"):]
    # Now add the showReason logic - find the first line after the signature
    pos_cd2 = final.find("function confirmDenyPending(pendingId, showReason) {")
    # Insert the showReason logic after the opening brace
    insert_pt = pos_cd2 + len("function confirmDenyPending(pendingId, showReason) {")
    show_reason_code = """
        if (showReason === true) {
            document.getElementById('confirm-deny-reason-row').style.display = 'block';
            document.getElementById('deny-reason-text').value = '';
            document.getElementById('confirm-pending-deny-id').value = pendingId;
            openModal('confirm-deny-reason-modal');
            return;
        }"""
    final = final[:insert_pt] + show_reason_code + final[insert_pt:]
    print("F2 deny showReason added")
else:
    print("F2: confirmDenyPending not found - checking...")
    print(repr(final[156090:156150]))

# ---- Fix F6: renderOfficerLoanApps - add clickable Loan ID ----
# Find the return statement in renderOfficerLoanApps
rola_search = "return '<tr><td><strong>' + client.name + '</strong><br><small>' + client.phone + '</small></td>'"
pos_rola = final.find(rola_search)
if pos_rola >= 0:
    new_rola = "return '<tr><td><a href=\"javascript:void(0)\" onclick=\"openLoanDetailModal(\\'' + l.id + '\\')\" style=\"color:var(--info);font-weight:700;text-decoration:underline;\">' + l.id + '</a></td><td><strong>' + client.name + '</strong><br><small>' + client.phone + '</small></td>'"
    final = final[:pos_rola] + new_rola + final[pos_rola + len(rola_search):]
    print("F6 officer loan clickable ID added")
else:
    print("F6: return statement not found in renderOfficerLoanApps, checking...")
    rola_pos = final.find("function renderOfficerLoanApps(")
    rola_end = final.find("\n    function ", rola_pos + 200)
    print(repr(final[rola_pos:rola_end]))

print(f"\nfinal length: {len(final)}")
