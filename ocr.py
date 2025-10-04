import os
import ocrmypdf

input_folder = r"C:\Users\rohit\Downloads\coe_assignment\allpdfs\allpdfs"
output_folder = r"C:\Users\rohit\Downloads\coe_assignment\output"
os.makedirs(output_folder, exist_ok=True)
pdf_files = [f for f in os.listdir(input_folder)]


if not pdf_files:
    print("No PDFs found in the input folder.")
else:
    for filename in pdf_files:
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        try:
            print(f"OCR running: {filename}")
            ocrmypdf.ocr(
                input_path,
                output_path,
                language="eng+hin+mar+ben+urd+chi_sim",
                progress_bar=True
            )
            print(f"OCR done: {filename}")
        except Exception as e:
            error_message = str(e)
            if "page already has text! - aborting" in error_message:
                os.replace(input_path, output_path)
                print(f"{filename} already has text, skipping")
            else:
                print(f"Error: {error_message}")