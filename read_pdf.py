import pymupdf

pdf_path = r'C:\Users\23961\Desktop\ISYS3001 A2 Assessment Brief.pdf'
doc = pymupdf.open(pdf_path)
print(f'Pages: {doc.page_count}')
for i, page in enumerate(doc):
    print(f'\n--- PAGE {i+1} ---')
    print(page.get_text("text", sort=True))
