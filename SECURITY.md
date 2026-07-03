# Security

- Admin panel is protected by a 6-digit PIN (changeable in-app or via `ADMIN_PIN` constant)
- API keys stored in `localStorage` — never transmitted to third parties
- Backend `.env` is gitignored — never commit secrets
- Database credentials and encryption keys are environment-controlled
- Infrastructure services (PostgreSQL, Redis, Keycloak) use separate credentials defined in `docker-compose.yml`

## Reporting

Open an issue for any security concerns.
