import c2pa
import json
import sys

def verify(file_path, mime_type):
    with open(file_path, 'rb') as f:
        reader = c2pa.Reader.try_create(mime_type, f)
    
    data = json.loads(reader.json())
    state = data.get('validation_state', 'Unknown')
    
    print(f"파일: {file_path}")
    print(f"검증 결과: {state}")
    
    # 실패 항목만 출력
    manifests = data.get('manifests', {})
    for manifest_id, manifest in manifests.items():
        results = manifest.get('validation_results', {})
        failures = results.get('activeManifest', {}).get('failure', [])
        if failures:
            print("실패 항목:")
            for f in failures:
                print(f"  ❌ {f['code']}: {f['explanation']}")
        else:
            print("실패 항목: 없음 ✅")

# 사용법: python verify.py <파일경로> <mime_type>
if __name__ == "__main__":
    if len(sys.argv) == 3:
        verify(sys.argv[1], sys.argv[2])
    else:
        print("사용법: python verify.py <파일경로> <mime_type>")
        print("예시: python verify.py output_signed.jpg image/jpeg")