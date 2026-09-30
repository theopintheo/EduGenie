# Team Work Document

This division follows the project brief and gives every member a clear deliverable and review responsibility.

This file is the single source of truth for team-member work. Use it for assignment, hand-off, review ownership, and release tracking; team responsibilities are documented here rather than in a separate web page.

## Theopin B

- Model selection and architecture decisions.
- Functional testing across all five workflows.
- Final integration review and release checklist.

## Antony Ragul A

- Frontend interface, responsive styling, and live form integration.
- Quiz answer interaction and result presentation.
- User guide review for clarity.

## Saravanan S

- FastAPI application and REST endpoint design.
- Request validation, health endpoint, and OpenAPI documentation.
- API error handling review.

## Karthick M

- Local run instructions and environment verification.
- Dependency installation and deployment checklist.
- Smoke-test evidence and troubleshooting notes.

## Shared review protocol

1. Work in a focused branch or clearly named change.
2. Add or update the relevant documentation with each feature.
3. Run `python -m compileall .` and a local `/health` request before review.
4. Demonstrate one successful and one invalid input for the changed feature.
5. Reviewer checks security, factual quality, accessibility, and mobile layout.
