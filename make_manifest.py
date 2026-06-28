import json
import os

output_dir = r"C:\c2pa_work\pdf_signed"
output_manifest = r"C:\c2pa_work\pdf_signed\manifest.json"

# 서명된 페이지 목록 자동 생성
signed_pages = sorted([
    f for f in os.listdir(output_dir) 
    if f.endswith("_signed.jpg")
])

manifest = {
    "title": "화성예술의전당 - 도시의 일상에 예술을 심다",
    "publisher": "Timelimit Inc.",
    "creator": "Soyoung Yoon, CEO",
    "created": "2026-06-27",
    "total_pages": len(signed_pages),
    "print_evidence": {
        "cover_photo": "print_cover.jpg",
        "interior_photo": "print_interior_01.jpg"
    },
    "signed_pages": signed_pages,
    "signing_info": {
        "tool": "c2pa-python 0.36.0",
        "algorithm": "PS256",
        "signer": "Timelimit Content Credentials"
    }
}

with open(output_manifest, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"매니페스트 생성 완료! 총 {len(signed_pages)}페이지")