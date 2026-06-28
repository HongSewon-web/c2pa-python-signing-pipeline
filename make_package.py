import zipfile
import os
import shutil

pdf_signed_dir = r"C:\c2pa_work\pdf_signed"
cover_path = r"C:\c2pa_work\print_cover.jpg"
interior_path = r"C:\c2pa_work\print_interior_01.jpg"
output_zip = r"C:\c2pa_work\화성예술의전당_C2PA.zip"

with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
    # 매니페스트
    zf.write(os.path.join(pdf_signed_dir, "manifest.json"), "manifest.json")
    
    # 표지/내지 사진
    zf.write(cover_path, "print_evidence/print_cover.jpg")
    zf.write(interior_path, "print_evidence/print_interior_01.jpg")
    
    # 서명된 페이지들
    for f in sorted(os.listdir(pdf_signed_dir)):
        if f.endswith("_signed.jpg"):
            zf.write(os.path.join(pdf_signed_dir, f), f"signed_pages/{f}")

print(f"패키지 완료! → {output_zip}")