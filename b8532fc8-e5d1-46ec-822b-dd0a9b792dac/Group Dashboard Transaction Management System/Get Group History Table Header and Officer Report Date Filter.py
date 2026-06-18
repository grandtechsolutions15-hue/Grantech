
# Group history table complete structure
gth_hdr = html_content.find('Group Transaction ID')
print("=== Group history table full HTML ===")
print(html_content[gth_hdr-500:gth_hdr+600])

# Get officer report section HTML (for adding monthly filter)
orf_html = html_content.find('id="officer-report-type"')
print("\n\n=== Officer report section HTML ===")
print(html_content[orf_html-400:orf_html+800])

# Find where officer-section ends to understand its structure for adding monthly summary
officer_section_end = html_content.rfind('</section>', 0, html_content.find('<!-- ADMIN SECTION -->'))
print("\n\n=== End of officer section ===")
print(html_content[officer_section_end-200:officer_section_end+100])
