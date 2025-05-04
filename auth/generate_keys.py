from jwcrypto import jwk
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import json

key = jwk.JWK.generate(kty='RSA', alg='RS256', use='sig', size=2048)

# 生成 JWK 金鑰
key = jwk.JWK.generate(kty='RSA', alg='RS256', use='sig', size=2048)

# 匯出 JWK 格式的私鑰 (JSON 字串)
jwk_private_str  = key.export_private()
jwk_public_str   = key.export_public() # 公鑰，註冊到 Line 上
jwk_private_dict = json.loads(jwk_private_str)

# 從 JWK 欄位重建 RSA 金鑰
from cryptography.hazmat.primitives.asymmetric import rsa
import base64

def b64_to_long(b64):
    padded = b64 + '=' * (-len(b64) % 4)
    return int.from_bytes(base64.urlsafe_b64decode(padded), byteorder='big')

rsa_private_key = rsa.RSAPrivateNumbers(
    p=b64_to_long(jwk_private_dict["p"]),
    q=b64_to_long(jwk_private_dict["q"]),
    d=b64_to_long(jwk_private_dict["d"]),
    dmp1=b64_to_long(jwk_private_dict["dp"]),
    dmq1=b64_to_long(jwk_private_dict["dq"]),
    iqmp=b64_to_long(jwk_private_dict["qi"]),
    public_numbers=rsa.RSAPublicNumbers(
        e=b64_to_long(jwk_private_dict["e"]),
        n=b64_to_long(jwk_private_dict["n"])
    )
).private_key(backend=default_backend())

# 儲存為 PEM 格式（PKCS8 格式）
rsa_private_pem = rsa_private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8, # 建議 PKCS8
    encryption_algorithm=serialization.NoEncryption()
)

# 寫入檔案
with open("private_key.pem", "wb") as f:
    f.write(rsa_private_pem)

print("已成功儲存為 private_key.pem")

# 匯出 json 格式公私鑰
with open("private_key.jwk.json", "w") as f:
    json.dump(json.loads(jwk_private_str), f, indent=2)
print("已儲存 JWK 私鑰：private_key.jwk.json")

jwk_public = key.export_public()
with open("public_key.jwk.json", "w") as f:
    json.dump(json.loads(jwk_public_str), f, indent=2)
print("已儲存 JWK 公鑰：public_key.jwk.json (可上傳 LINE)")
