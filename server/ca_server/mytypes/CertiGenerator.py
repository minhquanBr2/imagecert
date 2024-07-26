from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID

class CertiGenerator:
    def __init__(self, ca_private_key: rsa.RSAPrivateKey, hash_algo):
        self.ca_private_key = ca_private_key
        self.hash_algo = hash_algo

    def generate_certificate(self, subject_name, public_key, not_before, not_after):
        issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"VN"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"HCMCity"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"HCMUS"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"HCMUSMHUD"),
            x509.NameAttribute(NameOID.COMMON_NAME, u"myca.example.com"),
        ])
        subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"VN"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"HCMCity"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"HCMUS"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"HCMUSMHUD"),
            x509.NameAttribute(NameOID.COMMON_NAME, subject_name),
        ])

        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            public_key
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            not_before
        ).not_valid_after(
            not_after
        ).add_extension(
            x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
            critical=False,
        ).sign(self.ca_private_key, self.hash_algo, default_backend())

        return cert, issuer
