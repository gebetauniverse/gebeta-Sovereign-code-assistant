## 1. Secure Backend API Build

### Scenario
A fintech startup needs to build a payment processing API. The code contains proprietary business logic that cannot be exposed to cloud AI providers.

### Task
Create a FastAPI authentication microservice locally with no cloud AI access.

### Gebeta Workflow

```bash
@agent Create a FastAPI service with:
- User authentication (JWT)
- PostgreSQL integration
- Input validation
- Unit tests
- Environment variable configuration
```

What Gebeta Does

· Scaffolds service structure
· Generates endpoints and models
· Writes unit tests
· Asks before dependency installation
· Logs all file changes and command approvals

Outcome

Complete, testable API service built entirely locally. No source code sent to third parties.

---

2. Private Fintech Refactor

Scenario

A payment company needs to refactor a sensitive transaction validation module. The code contains PCI-related logic that cannot leave the organization.

Task

Refactor the validation module to improve performance without exposing source code.

Gebeta Workflow

```bash
@agent Analyze the payment validation module in /src/payment/validator.py
Suggest improvements for performance while maintaining security rules
```

What Gebeta Does

· Loads repo locally into Continue context
· Uses Ollama-hosted local model for analysis
· Applies rules from gebeta-rules.md
· Proposes changes under manual approval
· Preserves all analysis locally

Outcome

Performance improvements achieved. No code sent to external providers. Full audit trail of changes.

---

3. Spring Boot Microservice Setup

Scenario

A development team needs to create a new microservice for inventory management.

Task

Generate a Spring Boot microservice with OpenAPI specs, tests, and Docker support.

Gebeta Workflow

```bash
@agent Create a Spring Boot microservice for inventory management with:
- REST API endpoints (CRUD operations)
- OpenAPI 3.0 documentation
- Unit and integration tests
- Dockerfile and docker-compose.yml
- PostgreSQL configuration
```

What Gebeta Does

· Creates service structure following team rules
· Generates controller, service, and repository layers
· Adds test stubs for all endpoints
· Creates Docker configuration
· Asks before modifying infrastructure files

Outcome

Production-ready microservice scaffold. Follows team architecture standards.

---

4. Team Code Review Assistant

Scenario

Before a human code review, a developer wants AI to catch obvious issues locally.

Task

Review pull request changes for security issues, style violations, and test gaps.

Gebeta Workflow

```bash
@agent Review the changes in this PR:
- Check for hardcoded secrets
- Verify test coverage for new functions
- Flag any architecture violations
- Suggest improvements for code style
```

What Gebeta Does

· Summarizes changes
· Flags suspicious patterns (hardcoded keys, SQL injection risks)
· Suggests missing test cases
· Checks compliance with gebeta-rules.md
· Generates review report locally

Outcome

AI-assisted pre-review catches issues before human review. Developer productivity + governance layer.

---

5. Legacy Code Documentation

Scenario

A team inherits an undocumented legacy codebase. They need to understand it before refactoring.

Task

Generate documentation for a legacy Python module.

Gebeta Workflow

```bash
@agent Analyze /src/legacy/payment_processor.py and generate:
- Function summaries
- Parameter descriptions
- Return value documentation
- Usage examples
- Potential issues or edge cases
```

What Gebeta Does

· Reads the local file
· Uses local model to understand logic
· Generates markdown documentation
· Flags potential bugs or anti-patterns
· Saves documentation locally

Outcome

Understanding of legacy code without sending it to cloud AI.

---

6. Secure Dependency Audit

Scenario

Before adding a new dependency, a team wants to understand its security implications.

Task

Audit a proposed dependency for security risks.

Gebeta Workflow

```bash
@agent Review the package "requests" for:
- Known vulnerabilities
- Maintenance status
- License compatibility (must be MIT or Apache 2.0)
- Alternative recommendations
```

What Gebeta Does

· Searches local knowledge base (or optional web with approval)
· Summarizes findings
· Flags license issues
· Suggests alternatives if needed
· Asks before modifying requirements.txt

Outcome

Informed dependency decision. No automatic installation without approval.

---

Summary

Use Case Best For Mode
Secure Backend API Solo founders, startups A or B
Private Fintech Refactor Compliance teams A only
Spring Boot Setup Enterprise teams A or B
Code Review Assistant All teams A or B
Legacy Documentation Maintenance teams A or B
Dependency Audit Security teams A (offline) or B

---

Last updated: April 2026

```
