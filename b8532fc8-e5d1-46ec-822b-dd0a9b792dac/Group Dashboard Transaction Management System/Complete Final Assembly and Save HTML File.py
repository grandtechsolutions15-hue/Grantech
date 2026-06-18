
import os, base64

filepath = 'index_pending_modal_working.html'
with open(filepath, 'rb') as f:
    file_bytes = f.read()

file_size = len(file_bytes)
b64 = base64.b64encode(file_bytes).decode('utf-8')

# Build a tiny helper page that embeds the full file as a download button
helper = """<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Download Helper</title></head>
<body style="font-family:sans-serif;padding:20px;background:#1a1a2e;color:#fff;text-align:center">
<h2 style="margin-bottom:16px">&#128229; Download Your File</h2>
<p style="color:#ccc;margin-bottom:24px">Tap the green button below</p>
<a id="dl" href="#"
   style="display:inline-block;padding:18px 40px;background:#1a5f2a;color:#fff;
          text-decoration:none;border-radius:12px;font-size:20px;font-weight:bold"
   download="index_pending_modal_working.html">
&#11015;&#65039; TAP TO DOWNLOAD
</a>
<p style="margin-top:20px;color:#888;font-size:12px">""" + f"Size: {file_size:,} bytes" + """</p>
<script>
document.getElementById('dl').href = 'data:text/html;base64,' + '""" + b64 + """';
</script>
</body></html>"""

with open('download_helper.html', 'w', encoding='utf-8') as fh:
    fh.write(helper)

helper_size = os.path.getsize('download_helper.html')
helper_b64 = base64.b64encode(open('download_helper.html','rb').read()).decode('utf-8')
helper_uri = 'data:text/html;base64,' + helper_b64

print(f"Main file size: {file_size:,} bytes")
print(f"Helper file size: {helper_size:,} bytes")
print()
print("="*60)
print("STEP 1: Long-press and copy the FULL line below (starts with data:text)")
print("STEP 2: Open new tab in Chrome on Android")
print("STEP 3: Paste into the address bar and press Go")
print("STEP 4: Tap the green button on the page to download")
print("="*60)
print()
print(helper_uri)
