This is mittnaturkart.no - a nature observation tracking webapp.

Tech stack:
- Vue with TypeScript
- Python with FastAPI
- PostgreSQL database
- Alembic for database migrations
- Keycloak for authentication
- Docker for containerization with Docker Compose
- Grafana with Loki, Prometheus, and Tempo for monitoring and data visualization

Key principles:
- Compact and concise code
- Modular and reusable components
- Clear separation of frontend and backend
- RESTful API design
- Store observations with: species, date, time, location, notes, category
- Use Norwegian as default for user-facing text
- Code is in English
- Minimal code comments, focus on self-explanatory code
- Comprehensive tests for reliability (unit, api, E2E)

File structure:
- frontend/: Vue app source code
- backend/: FastAPI source code
- docker/: Dockerfiles and Compose configs
- tests/: Unit and integration tests
- scripts/: Helper scripts for setup, testing, etc.

Agent instructions:
- Don't make assumptions about intent, always ask for clarification
- Prioritize simplicity and elegance in code solutions
- Follow best practices for security and performance
- Write tests for all new features and bug fixes
- Suggest dependencies when appropriate, but avoid bloat
- Make sure code is well-structured and maintainable
- Dependencies should be popular, well-maintained, have permissive licenses and versions should be as up-to-date as possible
- Use environment variables for configuration where applicable
- Local development should be equal to production as much as possible