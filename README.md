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

## Konfigurasjon
Database-innstillinger plasseres i `.env` filen
