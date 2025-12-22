# Mittnaturkart.no
Kildekode til nettstedet [mittnaturkart.no](https://mittnaturkart.no)

## Kom i gang

Start applikasjonen med Docker (anbefalt):
```bash
./start.sh
```

Stopp applikasjonen:
```bash
./stop.sh
```

## Testing

Kjør test-suitte:
```bash
./test.sh
```

Tester kjøres i Docker mot et isolert miljø:
- **Unit-tester**: pytest (backend)
- **API-tester**: HTTP-kall (backend, db)
- **E2E-tester**: Playwright (frontend, backend, db)

## CI/CD

Automatisk testing og versjonering ved push til main. Versjon bumpes basert på commit-prefiks (`fix:`, `feat:`).

## Arkitektur

- **Frontend**: Vue 3 + TypeScript + Vite
- **Backend**: Python + FastAPI
- **Database**: PostgreSQL
- **Autentisering**: Keycloak
- **Reverse proxy**: Nginx
- **Containerisering**: Docker + Docker Compose
- **Domene/HTTPS**: Cloudflare (DNS, SSL, Tunnel)

Trafikk (i prod) går via Cloudflare Edge → Tunnel → Nginx → tjenester. Ingen åpne porter eller manuell sertifikathåndtering.

Tilgjengelig på `http://localhost` (frontend), `/api/v1/...` (API), og `/authentication` (Keycloak).

[API-dokumentasjon (Swagger)](https://mittnaturkart.no/docs)

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

# Keycloak Configuration
KEYCLOAK_ADMIN_PASSWORD=change_me_in_production
KEYCLOAK_PUBLIC_URL=http://localhost/authentication
KEYCLOAK_REALM=mittnaturkart
KEYCLOAK_CLIENT_ID=mittnaturkart-client
KEYCLOAK_CLIENT_SECRET=change_me_in_production
```

## Produksjon

Kjører på en **Raspberry Pi 5** med Docker og Cloudflare Tunnel for HTTPS.

![Raspberry Pi 5 setup](docs/pi.png)
*Her kjører nettstedet ved siden av min ruter og mitt pi-hole*

Sett `CLOUDFLARE_ENABLED=true` og `CLOUDFLARE_TUNNEL_TOKEN` i `.env` for å aktivere tunnelen.

## Fremtidige planer

- Dele lokasjoner med andre brukere
- Velge lokasjon via kart (Google Maps e.l.)
- Egendefinert Keycloak-tema
- Integrasjon med artsdatabaser/API-er
- Bildeopplasting og telling
- Sosiale funksjoner (venner, feed)
- Datavisualisering
- Integrasjon med Artsobservasjoner (import/eksport)

---

Laget og vedlikeholdt av **Arne Giacomo Munthe-Kaas**, kjører på egen maskinvare.

Bygget med hjelp fra [Claude Code](https://claude.com/product/claude-code)
