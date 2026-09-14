# Chirrp Backend v0.1

A backend for a "Reddit meets X" service with nested comments.

## Prerequisites

- Docker
- Docker Compose

## Quickstart

1. Copy `.env.example` to `.env` and adjust if needed.

2. Build and start the services: `docker compose up --build`
3. Run the migrations inside the container: `docker exec -it chirrp-api alembic upgrade head`
4. Access the API at http://localhost:8001/api/v1/healthz (should return {"status": "ok"}). 
5. OpenAPI docs at http://localhost:8001/docs. 
6. Seed sample data: `docker compose exec api python -m scripts.seed`
7. List posts: `curl http://localhost:8001/api/v1/posts`

P.S. test push 1

## test fixture

```
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAhb03OePaygGh4IaiQcEHWkABEIR8S0zf9zlxRPi80l+a2itu
B+qP3guGHuixCn2T+eZy+cJISd11qpB2hILbKFIz+3QtfZIIE8QAaaGncyWkT5A9
pJf8/N1NvJXXyg8mygnl4NbqRyciLQQsbYRsc2P26jn+Rp7ZpTlbNKF5Q/nBhI17
qLYLu/7fmrIFZxTTK2ppdnICrW1otThB8NtNA/CzxjD2Lwbtdsn5IBw6r9SizdoS
v+QaFL+iAVvrIvzOHDok0i5gYEe5OvM1gqzRfk1BsU0djcB8xKnHqJq6V2IGKNuR
5Cl7cO8yyF2dMtHVHgx8EfDNqhGw9q7OeurztQIDAQABAoIBAB6JvgRPQeyKEmFf
RMogblIels+jfPFB0MtWN8XQyWb9MzIZpCKVHjxM49eHeTOkyKcRxtO+l/yb38wu
eA2ahroOiTWkCeYoNAV1ZkW4hrCtmfcb/+NnXDqOOvuyuIc4Tfpo56+fS3grWKuw
TgfE6vGvVBiYXPZZu+d1MR0TuQm698NAbJ26uLqUPM15u/iV+n4Id4Gr4aMtg+tJ
2x7kaXbznAgTOmdzBFCFuX35L/kt5P6/4OqId0aM2COoreIYDR+7hj1NCUPu5KdU
QomrAa/Jb9fjEao0bafRD7YmHbYr1+AhKpe86SwKnP5DePg4RSIJKpxSfFCfujR7
3aqRC7kCgYEAud0Iw0xDfvJJ2LMYyKwWk3j2zW0GGWzi9dDIWYPlfmVDQyEWQb2D
tqqiQHXVfY4/JmNYb3FvTXfTTrvyx36ZodibxCvajLCH/MkFOj7wB95CQU7hpq9w
5pGl6PvPdGh6OFGgIGxDlepaaHw6dLCr68IZOZhbjACRSi8KYsHe530CgYEAuDTR
ZlF3tnE48b+W2gtDg2A8l9j33raY01GMcH96UcE+tAnfRYykIJ89i5Fr1xjwTJHn
2lc9BXV1t0GmeaWCTtYnT1hG5Jn5NrVS13LFo3wS3CEkN7Wdx8Mh6uTss89cBv7J
bkMv+9NIlTMmKSjQ8tOuK8uy2VnirvEKKDQEIpkCgYA+9wyS7PEovngZ+4J36SS0
zRP/P+IDFwpEcHiPKsnCahfBVCIwHz3R0jipUcIDiP8HyDwbdPhZ7DAfyjhTMSZm
1/TdHmYpp1xKXOdydgPnBnq3mTuEtoau9cSZC0WakBJnpe9zTHoQ/ZWnM/6xrXBw
rA7TnjPVWBPgZ9NC5Z7YGQKBgQCtRoHzjY7ev4KhZWexlAbd/hkBfccsaPc5UOya
pk+Zt/4TvXWZJsL9LM3oC9M1cvAYFufSK13rVKJ2z/qZU2dQYYJ40MFfKLeVDtvu
brgbIQtcppA7F0xkLNoq60z9l4Ep02IHpovshsMwFf0/mnVy9kxQRjzm1/a0OWkk
iEmbgQKBgAN4BGgpqM/O++xLchM/oMt8yBbkdccWxfQxMxCRQRMXmo8bWHGg4I0t
Zbr6RDjBuGD3X16/heeFxTMQslaYm1tl3mR36K9FIRe11FhccUMCHuqYH752dmoP
KNkDcELOR6r0UdDOm02ix+o2NNGTVP5VCBza7thBFH6YCPwfzUb6
-----END RSA PRIVATE KEY-----
```
