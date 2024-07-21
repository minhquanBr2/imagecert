import { CertificateRequest } from '@peculiar/asn1-pkcs9';
import { AsnConvert } from '@peculiar/asn1-schema';
import { Crypto } from '@peculiar/webcrypto';
import { Buffer } from 'buffer';

const createCsr = async (keyPair: CryptoKeyPair) => {
  const crypto = new Crypto();
  (global as any).crypto = crypto;

  const publicKeyInfo = await crypto.subtle.exportKey('spki', keyPair.publicKey);
  const subject = new CertificateRequest({
    subject: {
      typesAndValues: [
        {
          type: '2.5.4.3', // CN
          value: new Buffer.from('example.com')
        }
      ]
    },
    subjectPublicKeyInfo: AsnConvert.parse(publicKeyInfo, PublicKeyInfo),
    signatureAlgorithm: {
      algorithm: '1.2.840.113549.1.1.5' // SHA1withRSA
    }
  });

  const csrDer = AsnConvert.serialize(subject);
  const signature = await crypto.subtle.sign(
    {
      name: 'RSASSA-PKCS1-v1_5'
    },
    keyPair.privateKey,
    csrDer
  );

  subject.signature = signature;

  setCsrPem(pemEncode(AsnConvert.serialize(subject), 'CERTIFICATE REQUEST'));
};