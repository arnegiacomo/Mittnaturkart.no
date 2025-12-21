# Mittnaturkart.no
Kildekode til nettstedet mittnaturkart.no

## Kom i gang

Start applikasjonen med Docker:
```bash
./start.sh
```

Stopp applikasjonen:
```bash
./stop.sh
```

### Lokal utvikling

Kjør backend lokalt (krever Python 3.12+ og PostgreSQL):
```bash
cd backend
./dev.sh
```

Kjør frontend lokalt (krever Node.js 20+):
```bash
cd frontend
./dev.sh
```

## Testing
Tester kjøres gjennom en egen Docker Compose-konfigurasjon. Dette lar oss teste både API og frontend i et isolert miljø, og sikrer at testene kjører mot samme oppsett som produksjon, slik at vi dekker en så stor del av verdikjeden som mulig.

Kjør alle tester (API + E2E):
```bash
./test.sh
```

Testene inkluderer:
- **API-tester**: Tester backend endpoints med HTTP-kall
- **E2E-tester**: Playwright-baserte tester av frontend (klikk, input, etc.)

## CI/CD

Automatisk testing og versjonering ved push til main. Versjon bumpes basert på commit-prefiks (`fix:`, `feat:`).

## Arkitektur

Applikasjonen bruker Nginx som reverse proxy:
- **Nginx** (port 80): Reverse proxy som håndterer alle innkommende forespørsler
- **Frontend** (Vue 3 + Vite): Brukergrensesnitt for naturobservasjoner
- **Backend API** (port 8000): FastAPI backend, tilgjengelig kun via Nginx
- **PostgreSQL** (port 5432): Database

Frontend er tilgjengelig på `http://localhost` og API på `http://localhost/api/v1/...` gjennom Nginx.

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

# Frontend Configuration
FRONTEND_PORT=5173

# Nginx Configuration
NGINX_PORT=80
```

---

Bygget med hjelp fra [Claude Code](https://claude.com/product/claude-code)
