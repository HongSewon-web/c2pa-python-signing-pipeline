from cryptography import x509
from cryptography.x509.oid import NameOID, ExtendedKeyUsageOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime

now = datetime.datetime.now(datetime.UTC)

# CA 키 생성
ca_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
ca_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Timelimit Test CA")])

ca_cert = (
    x509.CertificateBuilder()
    .subject_name(ca_name).issuer_name(ca_name)
    .public_key(ca_key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(now)
    .not_valid_after(now + datetime.timedelta(days=365))
    .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
    .add_extension(x509.KeyUsage(
        digital_signature=True, key_cert_sign=True, crl_sign=True,
        key_encipherment=False, key_agreement=False, content_commitment=False,
        data_encipherment=False, encipher_only=False, decipher_only=False
    ), critical=True)
    .add_extension(x509.SubjectKeyIdentifier.from_public_key(ca_key.public_key()), critical=False)
    .sign(ca_key, hashes.SHA256())
)

# 리프 키 생성
leaf_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
leaf_name = x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, "Timelimit Content Credentials"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Time-Limit"),
    x509.NameAttribute(NameOID.COUNTRY_NAME, "KR"),
])

leaf_cert = (
    x509.CertificateBuilder()
    .subject_name(leaf_name).issuer_name(ca_name)
    .public_key(leaf_key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(now)
    .not_valid_after(now + datetime.timedelta(days=365))
    .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
    .add_extension(x509.KeyUsage(
        digital_signature=True, key_cert_sign=False, crl_sign=False,
        key_encipherment=False, key_agreement=False, content_commitment=False,
        data_encipherment=False, encipher_only=False, decipher_only=False
    ), critical=True)
    .add_extension(x509.SubjectKeyIdentifier.from_public_key(leaf_key.public_key()), critical=False)
    .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()), critical=False)
    .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.EMAIL_PROTECTION]), critical=False)
    .sign(ca_key, hashes.SHA256())
)

# 저장
chain = leaf_cert.public_bytes(serialization.Encoding.PEM) + ca_cert.public_bytes(serialization.Encoding.PEM)
with open(r'C:\c2pa_work\test_cert_chain.pem', 'wb') as f:
    f.write(chain)

key_pem = leaf_key.private_bytes(
    serialization.Encoding.PEM,
    serialization.PrivateFormat.PKCS8,
    serialization.NoEncryption()
)
with open(r'C:\c2pa_work\test_key_chain.pem', 'wb') as f:
    f.write(key_pem)

print("테스트 인증서 생성 완료!")