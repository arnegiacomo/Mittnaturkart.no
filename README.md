# Mittnaturkart.no
Kildekode til nettstedet mittnaturkart.no

## Kom i gang

Start applikasjonen:
```bash
./start.sh
```

Stopp applikasjonen:
```bash
./stop.sh
```

## Testing

Kjør API-tester:
```bash
./test.sh
```

Tester kjøres automatisk ved push til GitHub (unntatt `chore:` commits).

## CI/CD

**Automatisk testing:** Kjører på alle branches ved push og pull requests til main.

**Automatisk versjonering:** Ved push til main:
- `fix:` → +0.0.1 (patch)
- `feat:` → +0.1.0 (minor)
- `chore:` → ingen endring

Versjonsnummer oppdateres automatisk i `VERSION` fil og API. Git-tag (f.eks. `v1.0.1`) opprettes automatisk.

## Arkitektur

Applikasjonen bruker Nginx som reverse proxy:
- **Nginx** (port 80): Reverse proxy som håndterer alle innkommende forespørsler
- **Backend API** (port 8000): FastAPI backend, tilgjengelig kun via Nginx
- **PostgreSQL** (port 5432): Database

API er tilgjengelig på `http://localhost/api/v1/...` gjennom Nginx.

## Konfigurasjon

Opprett en `.env` fil i rotmappen med følgende innhold:

```env
# Database Configuration
POSTGRES_DB=mittnaturkart
POSTGRES_USER=postgres
POSTGRES_PASSWORD=change_me_in_production
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Backend Configuration
BACKEND_PORT=8000

# Nginx Configuration
NGINX_PORT=80
```

---

Bygget med hjelp fra [Claude Code](https://claude.com/product/claude-code)
