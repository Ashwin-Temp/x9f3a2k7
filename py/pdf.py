import fitz  # PyMuPDF
import os

print("📄 PDF Hybrid Cleaner (The One That Works)")
print("Type file name WITHOUT .pdf (type 'exit' to quit)\n")

while True:
    name = input("Enter PDF name: ").strip()

    if name.lower() == "exit":
        print("👋 Exiting...")
        break

    input_pdf = f"{name}.pdf"
    output_pdf = f"{name}_cleaned.pdf"

    if not os.path.exists(input_pdf):
        print("❌ File not found:", input_pdf)
        print()
        continue

    try:
        doc = fitz.open(input_pdf)

        # 1. Remove the 2nd Page
        if len(doc) > 1:
            doc.delete_page(1)
            print("✂️  Removed 2nd page.")

        print("🧹 Cleaning...")

        for page in doc:
            # ---------------------------
            # A. REMOVE BACKGROUND IMAGE (The "Double Tap" Method)
            # ---------------------------
            # This is the exact logic from the code that worked for you earlier.
            image_list = page.get_images(full=True)
            
            for img in image_list:
                xref = img[0]
                rects = page.get_image_rects(xref)
                
                for rect in rects:
                    # If image is big (Background)
                    if rect.width > 250 and rect.height > 250:
                        page.delete_image(xref)           # Step 1: Delete reference
                        page.add_redact_annot(rect)       # Step 2: Mark area for scrubbing
                        page.apply_redactions()           # Step 3: Scrub it (This was missing later!)

                    # If image is at the very top (Header Logo)
                    elif rect.y0 < 50:
                        page.delete_image(xref)           # Just delete, no scrub needed for small logos

            # ---------------------------
            # B. REMOVE HEADER TEXT (Targeted)
            # ---------------------------
            # Instead of the White Box, we find the text and delete ONLY the text.
            bad_words = ["Adda247", "Google Play", "GET IT ON"]
            for word in bad_words:
                text_instances = page.search_for(word)
                for inst in text_instances:
                    if inst.y0 < 100:  # Only delete if it's in the header area
                        page.add_redact_annot(inst)
            
            page.apply_redactions()

        # Save to new file
        doc.save(output_pdf, garbage=4, deflate=True)
        doc.close()

        print(f"✅ Processed: {output_pdf}")
        print(f"📂 Original:  {input_pdf}")
        print("-" * 30)

    except Exception as e:
        print("⚠️ Error:", e)
        if os.path.exists(output_pdf):
            os.remove(output_pdf)
        print()