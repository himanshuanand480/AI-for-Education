from pdf_loader import extract_text_from_pdf, extract_pagewise

file_path = "Resume_HimanshuAnand_R.pdf"



print("----- FULL TEXT OUTPUT -----\n")
text = extract_text_from_pdf(file_path)
print(text)


print("\n\n----- PAGE WISE OUTPUT -----\n")

data = extract_pagewise(file_path)

for page in data:
    print(f"Page {page['page']}:")
    print(page['content'])
    print("-" * 40)