import c2pa
import json
import uuid

dng_path = r"C:\c2pa_work\0P0A4748.dng"
output_path = r"C:\c2pa_work\output_signed.dng"
cert_path = r"C:\c2pa_work\test_cert_chain.pem"
key_path = r"C:\c2pa_work\test_key_chain.pem"

with open(cert_path, "rb") as f:
    sign_cert = f.read()
with open(key_path, "rb") as f:
    private_key = f.read()

ingredient_id = "xmp.iid:" + uuid.uuid4().hex.upper()

ingredient_json = {
    "title": "source.dng",
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

with open(dng_path, 'rb') as f:
    builder.add_ingredient(ingredient_json, "image/x-adobe-dng", f)
builder.sign_file(dng_path, output_path, signer)
print("서명 완료!")