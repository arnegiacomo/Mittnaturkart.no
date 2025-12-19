This is mittnaturkart.no - a nature observation tracking webapp.

Tech stack:
- Vue with TypeScript
- Python with FastAPI
- PostgreSQL database
- Alembic for database migrations
- Docker for containerization with Docker Compose
- Grafana with Loki, Prometheus, and Tempo for monitoring and data visualization

Key principles:
- Compact and concise code
- Modular and reusable components
- Clear separation of frontend and backend
- RESTful API design
- Store observations with: species, date, time, location, notes, category
- Use Norwegian for all user-facing text
- Minimal code comments, focus on self-explanatory code

File structure:
- frontend/: Vue app source code
- backend/: FastAPI source code
- database/: SQL scripts and migrations
- docker/: Dockerfiles and Compose configs
- tests/: Unit and integration tests
- docs/: Documentation and design notes

Agent instructions:
- Don't make assumptions about intent, always ask for clarification
- Prioritize simplicity and elegance in code solutions
- Follow best practices for security and performance
- Write tests for all new features and bug fixes
- Suggest dependencies when appropriate, but avoid bloat

Roadmap:
- Phase 1: Basic observation CRUD functionality (POC)
- Phase 2: CI/CD pipeline setup + hardware setup instructions
- Phase 3: User authentication and profiles
- Phase 4: Integration with external species databases and APIs
- Phase 5: Observability and monitoring setup with Grafana stack