
# Only 2 issues remain:
# - F2 deny with reason (confirmDenyPending fix didn't apply - showReason param)
# - F6 officer loan clickable (renderOfficerLoanApps row update)
# Let's fix those then add all new JS functions

final = html3  # start from html3

# ---- Fix F2: confirmDenyPending ----
# Check what's in html3 vs what we expected
pos_cd = final.find("function confirmDenyPending(")
print("Current confirmDenyPending signature:")
print(repr(final[pos_cd:pos_cd+100]))

# ---- Check F6: renderOfficerLoanApps ----
rola_pos = final.find("function renderOfficerLoanApps(")
rola_end = final.find("\n    function ", rola_pos + 200)
rola_func = final[rola_pos:rola_end]
print("\nrenderOfficerLoanApps (first 500):")
print(repr(rola_func[:500]))
