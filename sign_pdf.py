import c2pa
import json
import uuid
import fitz  # pymupdf
import os

pdf_path = r"C:\c2pa_work\화성예술의전당-최종 펼침면.pdf"  # PDF 파일 경로
output_dir = r"C:\c2pa_work\pdf_signed"
cert_path = r"C:\c2pa_work\test_cert_chain.pem"
key_path = r"C:\c2pa_work\test_key_chain.pem"

os.makedirs(output_dir, exist_ok=True)

with open(cert_path, "rb") as f:
    sign_cert = f.read()
with open(key_path, "rb") as f:
    private_key = f.read()

# PDF → JPG 변환 후 서명
doc = fitz.open(pdf_path)
print(f"총 {len(doc)} 페이지")

for page_num in range(len(doc)):
    page = doc[page_num]
    pix = page.get_pixmap(dpi=300)
    jpg_path = os.path.join(output_dir, f"page_{page_num+1:03d}.jpg")
    pix.save(jpg_path)
    
    # C2PA 서명
    ingredient_id = "xmp.iid:" + uuid.uuid4().hex.upper()
    ingredient_json = {
        "title": f"page_{page_num+1:03d}_source.jpg",
        "relationship": "parentOf",
        "instance_id": ingredient_id
    }
    manifest = {
        "claim_generator": "Timelimit Content Credentials/1.0",
        "assertions": [
            {
                "label": "c2pa.actions",
                "data": {
                    "actions": [
                        {
                            "action": "c2pa.opened",
                            "parameters": {
                                "ingredientIds": [ingredient_id]
                            }
                        }
                    ]
                },
                "created": True
            }
        ]
    }
    
    signer_info = c2pa.C2paSignerInfo(
        alg="ps256",
        sign_cert=sign_cert,
        private_key=private_key,
        ta_url="http://timestamp.digicert.com"
    )
    signer = c2pa.Signer.from_info(signer_info)
    builder = c2pa.Builder(manifest)
    
    with open(jpg_path, 'rb') as f:
        builder.add_ingredient(ingredient_json, "image/jpeg", f)
    
    output_path = os.path.join(output_dir, f"page_{page_num+1:03d}_signed.jpg")
    builder.sign_file(jpg_path, output_path, signer)
    print(f"페이지 {page_num+1} 서명 완료 → {output_path}")

print("전체 완료!")