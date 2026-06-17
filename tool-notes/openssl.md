# openssl

TLS/crypto swiss army knife; certificates, keys, CSRs, and server debugging.

## Inspect certs & connections

```bash
openssl s_client -connect example.com:443 -servername example.com   # debug a TLS handshake
openssl x509 -in cert.pem -noout -text          # decode a certificate
openssl x509 -in cert.pem -noout -subject -issuer -dates   # the fields you usually want
```

## Keys & CSRs

```bash
openssl genrsa -out key.pem 4096                # RSA private key
openssl ecparam -genkey -name prime256v1 -out ec.pem   # EC key
openssl req -new -key key.pem -out req.csr      # certificate signing request
openssl req -x509 -newkey rsa:4096 -keyout k.pem -out c.pem -days 365 -nodes   # self-signed
```

## Digests, encoding, random

```bash
openssl dgst -sha256 file               # checksum
openssl rand -base64 32                 # random token
openssl base64 -d -in encoded.txt       # decode base64
```

## Notes

- `s_client -servername` sends SNI — needed for name-based virtual hosts
- `-noout` suppresses the encoded blob; pair with `-text`/`-dates`/`-subject`
