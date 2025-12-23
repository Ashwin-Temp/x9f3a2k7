from pypdf import PdfReader, PdfWriter
import os

print("📄 PDF 2nd Page Remover")
print("Type file name WITHOUT .pdf (type 'exit' to quit)\n")

while True:
    name = input("Enter PDF name: ").strip()

    if name.lower() == "exit":
        print("👋 Exiting...")
        break

    input_pdf = f"{name}.pdf"
    output_pdf = f"{name}_d.pdf"

    if not os.path.exists(input_pdf):
        print("❌ File not found:", input_pdf)
        print()
        continue

    try:
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        for i, page in enumerate(reader.pages):
            if i == 1:  # remove 2nd page
                continue
            writer.add_page(page)

        with open(output_pdf, "wb") as f:
            writer.write(f)

        os.remove(input_pdf)

        print(f"✅ Done → {output_pdf}")
        print(f"🗑 Deleted → {input_pdf}\n")

    except Exception as e:
        print("⚠️ Error:", e)
        print()
