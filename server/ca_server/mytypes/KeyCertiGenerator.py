from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID
from datetime import datetime, timedelta
import base64
from mytypes.CertiGenerator import CertiGenerator

class KeyCertiGenerator(CertiGenerator):
    def generate_key_certificate(self, user_uid, user_public_key_pem):
        public_key_der = base64.b64decode(user_public_key_pem)
        user_public_key = serialization.load_der_public_key(
            public_key_der,
            backend=default_backend()
        )

        not_before = datetime.utcnow()
        not_after = datetime.utcnow() + timedelta(days=365)

        cert, issuer = self.generate_certificate(user_uid, user_public_key, not_before, not_after)

        cert_der = cert.public_bytes(serialization.Encoding.DER)
        cert_base64 = base64.b64encode(cert_der).decode('utf-8')
        not_before_timestamp = not_before.isoformat()
        not_after_timestamp = not_after.isoformat()
        issuer_string = issuer.rfc4514_string()

        certi_payload = {
            "issuer_name": issuer_string,
            "not_before": not_before_timestamp,
            "not_after": not_after_timestamp,
            "status": 1,
            "certi": cert_base64,
            "public_key": user_public_key_pem
        }

        return certi_payload
