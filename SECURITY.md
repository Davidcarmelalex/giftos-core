# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in GiftOS Core, please report it responsibly.

**Do not** open a public issue. Instead:

1. Email **security@giftos.dev** with details
2. Include steps to reproduce
3. Include potential impact assessment
4. Allow up to 72 hours for initial response

## Disclosure Policy

- Reporter submits vulnerability privately
- Maintainers acknowledge receipt within 72 hours
- Maintainers investigate and develop fix
- Fix is released and vulnerability is publicly disclosed
- Reporter is credited (unless anonymity requested)

## Security Best Practices for Users

- Rotate API keys regularly
- Use environment variables for secrets (never commit to git)
- Enable webhook signature verification
- Monitor audit logs for unusual activity
- Keep GiftOS Core updated to the latest version

## Security Features

- API key authentication with scoped permissions
- Webhook HMAC signature verification
- Rate limiting on all endpoints
- Input validation and sanitization
- Audit logging for sensitive operations
