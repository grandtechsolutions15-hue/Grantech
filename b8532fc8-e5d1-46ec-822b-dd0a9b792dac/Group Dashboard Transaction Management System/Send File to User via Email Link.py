
import os, base64, hashlib

filepath = 'index_pending_modal_working.html'
with open(filepath, 'rb') as f:
    file_bytes = f.read()

file_size = len(file_bytes)

# Write the file to a known path so user can access it
# Also generate a mailto: link with instructions
print("=" * 60)
print("YOUR FILE IS READY")
print("=" * 60)
print(f"Filename : index_pending_modal_working.html")
print(f"File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
print()
print("HOW TO GET IT ON ANDROID CHROME:")
print()
print("OPTION A — Send yourself via Telegram/WhatsApp:")
print("  1. Open Telegram app on your phone")
print("  2. Message 'Saved Messages' or your own chat")  
print("  3. Ask the person who set up this Zerve account")
print("     to download the file from the Files panel")
print("     on a computer and send it to you.")
print()
print("OPTION B — Use Zerve on a computer:")
print("  1. Open this notebook on any desktop/laptop browser")
print("  2. Look for the Files panel (folder icon top-left)")
print("  3. Click 'index_pending_modal_working.html' -> Download")
print()
print("OPTION C — Copy from block output (Android):")
print("  The file is 328KB so it cannot fit in one chat message.")
print("  But you can use the data URI. See the block named")
print("  'Complete Final Assembly and Save HTML File'.")
print("  In that block output, tap-hold the long 'data:text/html'")
print("  line and copy it, then paste in Chrome address bar.")
print()

# Let's try a different approach - create a shorter redirect HTML
# that uses a fetch approach - but actually let's just confirm file exists
print(f"File confirmed on disk: {os.path.exists(filepath)}")
print(f"MD5: {hashlib.md5(file_bytes).hexdigest()}")
