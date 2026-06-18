
# Find a better insertion point in 'final'
candidates = ['function saveAppData()', '// ====', 'function logout()', '</script>']
for c in candidates:
    p = final.find(c)
    print(f"'{c[:40]}' at {p}")
