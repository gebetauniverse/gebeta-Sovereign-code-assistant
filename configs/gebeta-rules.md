# Gebeta Sovereign Coding Rules

## Security

- Never generate code that exposes secrets, API keys, or credentials.
- Use environment variables for configuration.
- Flag any hardcoded secrets immediately.
- Never commit .env files or configuration with credentials.
- Use strong password hashing (bcrypt, Argon2) for user passwords.
- Validate all user inputs to prevent injection attacks.
- Use parameterized queries for database operations.

## Architecture

- Prefer microservices over monoliths unless requested otherwise.
- Use FastAPI for Python backends, Spring Boot for Java.
- Keep functions small (<30 lines) and testable.
- Follow SOLID principles.
- Use dependency injection where appropriate.
- Separate business logic from data access layers.

## Operations

- Never modify Dockerfiles, CI/CD pipelines, or Kubernetes manifests without asking.
- Ask before adding new dependencies.
- Prefer open-source libraries with permissive licenses (MIT, Apache 2.0).
- Pin dependency versions in requirements.txt or package.json.
- Document all environment variables in README.

## Quality

- Always write unit tests for new functions.
- Include docstrings for all public methods.
- Use type hints (Python) or strong types (TypeScript).
- Maintain code coverage above 80%.
- Follow PEP 8 (Python) or ESLint rules (JavaScript).
- Use meaningful variable and function names.

## API Design

- Use RESTful principles for API endpoints.
- Version your APIs (v1, v2, etc.).
- Return consistent error response formats.
- Use appropriate HTTP status codes.
- Implement rate limiting for public endpoints.

## Database

- Use migrations for schema changes.
- Index frequently queried columns.
- Never store passwords in plain text.
- Use transactions for multi-step operations.
