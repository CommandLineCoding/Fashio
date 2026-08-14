# Contributing to Fashio

Thank you for contributing to Fashio. This document outlines the development standards, workspace architecture, issue tracking protocol, and pull request workflow required for maintaining a structured open-source codebase.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Monorepo Architecture & Rules](#monorepo-architecture--rules)
3. [Functional Team Clusters](#functional-team-clusters)
4. [Issue Labeling Strategy](#issue-labeling-strategy)
5. [Development Environment Setup](#development-environment-setup)
6. [Branching & Development Workflow](#branching--development-workflow)
7. [Coding & Quality Verification](#coding--quality-verification)
8. [Commit Message Specification](#commit-message-specification)
9. [Submitting a Pull Request](#submitting-a-pull-request)
10. [Milestone Roadmap Summary](#milestone-roadmap-summary)

---

## Code of Conduct

All contributors are expected to uphold a professional, respectful, and inclusive environment. Discriminatory behavior, harassment, or non-constructive communication will not be tolerated.

---

## Monorepo Architecture & Rules

The project operates as a decoupled monorepo containing a Django REST Framework backend managed by `uv` and a React frontend built with Vite.

```text
fashio/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── workflows/
│   │   ├── backend-ci.yml
│   │   └── frontend-ci.yml
│   └── PULL_REQUEST_TEMPLATE.md
│
├── backend/                        # Django REST Framework application (managed by uv)
│   ├── .python-version             # Python version pinned by uv
│   ├── pyproject.toml              # Dependencies and tool settings managed by uv
│   ├── uv.lock                     # Deterministic dependency lockfile
│   ├── Dockerfile
│   ├── manage.py
│   ├── config/                     # Core Django settings and URLs
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── settings/
│   │       ├── __init__.py
│   │       ├── base.py
│   │       ├── local.py
│   │       └── prod.py
│   └── apps/                       # Modular Django domain applications
│       ├── __init__.py
│       ├── authentication/
│       ├── catalog/
│       ├── orders/
│       ├── profiles/
│       └── sellers/
│
├── frontend/                       # React single-page application (Vite)
│   ├── .eslintrc.cjs
│   ├── .prettierrc
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   └── src/
│       ├── components/             # Reusable UI primitives (Buttons, Modals)
│       ├── context/                # React Context providers
│       ├── features/               # Domain-specific UI and state logic
│       │   ├── auth/
│       │   ├── catalog/
│       │   ├── cart/
│       │   └── checkout/
│       ├── layouts/                # Page shell layouts
│       ├── pages/                  # Route views
│       ├── services/               # API interaction layer
│       └── store/                  # State management store
│
├── compose.yml              # Container orchestration specification
├── .env.example
├── ARCHITECTURE.md
├── CONTRIBUTING.md
└── README.md
```

### Workspace Execution Rules

* **Backend Environment (`uv`):** All Python interactions must use `uv`. Dependencies are synced via `uv sync`, and scripts/management commands must execute using `uv run python manage.py <command>`.
* **Modular Django Apps:** All domain logic resides inside `/backend/apps/`. The settings configuration inserts `/backend/apps/` into `sys.path` to permit direct application imports (e.g., `from catalog.models import Product`).
* **Modular Settings:** Environment configuration is divided within `config/settings/` (`base.py`, `local.py`, `prod.py`) using `django-environ` for secret isolation.
* **Frontend Component Architecture:** Primitive, generic UI components belong in `src/components/`, while domain-specific state, API service calls, and sub-views must be placed inside `src/features/<domain>/`.

---

## Functional Team Clusters

To avoid merge bottlenecks across contributor teams, tasks are organized into three primary functional domain clusters:

* **Cluster A (Core & Identity):** Covers Milestone 0 (Infrastructure), Milestone 1 (Auth & Identity), and Milestone 6 (Customer Profiles & History).
* **Cluster B (Catalog & Vendor Engine):** Covers Milestone 2 (Catalog & Product Engine), Milestone 3 (Seller/Vendor Management), and Milestone 7 (Global UI Navigation & Search).
* **Cluster C (Commerce & Operations):** Covers Milestone 4 (Cart & Wishlist), Milestone 5 (Checkout & Orders), and Milestone 8 (Security, Hardening & Launch).

---

## Issue Labeling Strategy

All backlog tasks and pull requests must be classified using three label categories:

### 1. Layer Classification
* `layer:backend/drf`
* `layer:frontend/react`
* `layer:database`
* `layer:devops`
* `layer:docs`
* `layer:design/ui`

### 2. Type Classification
* `type:feat`
* `type:fix`
* `type:refactor`
* `type:test`
* `type:security`

### 3. Complexity Estimation
* `good-first-issue` (1–2 Story Points)
* `complexity:medium` (3–5 Story Points)
* `complexity:complex` (8+ Story Points)

---

## Development Environment Setup

### Prerequisites

* Python >= 3.12
* [uv](https://github.com/astral-sh/uv) package manager
* Node.js >= 20.0.0
* Podman / Docker Engine with Compose support

### Setup Steps

1. Fork the repository on GitHub and clone your fork locally:
```bash
   git clone [https://github.com/YOUR_USERNAME/Fashio.git](https://github.com/YOUR_USERNAME/Fashio.git)
   cd Fashio
```

2. Configure the upstream remote repository:
```bash
git remote add upstream [https://github.com/ORIGINAL_OWNER/Fashio.git](https://github.com/ORIGINAL_OWNER/Fashio.git)
```


3. Initialize environment configuration:
```bash
cp .env.example .env
```


4. Launch the local container environment using Podman or Docker:
```bash
# Using Podman
podman compose up --build

# Using Docker
docker compose up --build
```

Application addresses:

* Backend API: `http://localhost:8000`
* Frontend Application: `http://localhost:5173`
* PostgreSQL Database: `localhost:5432`

---

## Branching & Development Workflow

Do not commit directly to `main` or `dev`. All work must occur on dedicated feature branches.

1. Fetch and rebase against upstream tracking branch:
```bash
git fetch upstream
git checkout -b <type>/<short-description> upstream/main
```

2. Keep branches small and focused on a single issue.

### Branch Prefix Naming

* `feat/` - New functionality
* `fix/` - Bug fixes
* `docs/` - Documentation modifications
* `refactor/` - Code changes that do not alter behavior
* `test/` - Adding or updating test suites
* `ci/` - Pipeline configuration changes

---

## Coding & Quality Verification

Before committing, run local verification checks.

### Backend Validation (`/backend`)

```bash
cd backend

# Sync environment
uv sync

# Static analysis and linting
uv run ruff check .

# Validate formatting
uv run ruff format --check .

# Execute test suite
uv run pytest
```

Automated code formatting can be applied using:

```bash
uv run ruff format .

```

### Frontend Validation (`/frontend`)

```bash
cd frontend

# Install dependencies
npm install

# Run linter
npm run lint

# Validate production build compilation
npm run build
```

---

## Commit Message Specification

Commits must conform to the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```text
<type>(<scope>): <short message>

[optional detailed description]

[optional issue reference]

```

### Supported Types

* `feat`: A new feature implementation
* `fix`: A bug resolution
* `docs`: Documentation-only updates
* `style`: White-space, formatting, or missing semi-colon fixes
* `refactor`: Code restructures that do not alter public API behavior
* `perf`: Performance optimizations
* `test`: Adding or correcting tests
* `chore`: Build process or tooling updates

### Example Commit Message

```text
feat(auth): implement Google OAuth2 token exchange endpoint

Integrate ID token validation flow for frontend authentication calls.
Includes unit test coverage for user creation and JWT pair issuance.

Closes #19

```

---

## Submitting a Pull Request

1. Rebase your feature branch onto the latest upstream branch:
```bash
git fetch upstream
git rebase upstream/main

```


2. Push your topic branch to your fork:
```bash
git push -u origin <type>/<short-description>

```


3. Open a Pull Request on GitHub against the target branch (`main` or `dev`).
4. Ensure your PR description clearly states:
* The issue being addressed.
* A summary of technical changes.
* Steps required to manually verify the implementation.


5. Verify that all GitHub Actions CI status checks pass cleanly.

---

## Milestone Roadmap Summary

The roadmap is structured into 8 sequential milestones containing granular implementation tasks:

* **Milestone 0: Environment, CI/CD & Architecture Setup:** Repository initialization, containerization, quality pipelines, and project documentation.


* **Milestone 1: Authentication & Identity Management:** JWT pair issuance, registration, password recovery, and Google/GitHub OAuth integrations.


* **Milestone 2: Catalog, Categories & Product Engine:** Hierarchical categories (`mptt`), product models, full-text search, filtering, and catalog UI.


* **Milestone 3: Seller Management & Vendor System:** Vendor profiles, seller authorization rules (`IsSeller`), and product management dashboards.


* **Milestone 4: Cart & Wishlist System:** Session-based and persistent user carts, cart synchronization, and wishlist persistence.


* **Milestone 5: Checkout Engine & Order Flow:** Atomic order transactions, inventory locking, state transitions, and payment processing integrations.


* **Milestone 6: Customer Profile, Reviews & History:** User settings, address management, order history, and verified purchase product reviews.


* **Milestone 7: Global UI Navigation, Search & Layout:** App layout shells, debounced global search, toast notifications, and responsive navigation.


* **Milestone 8: Hardening, Security, Performance & Launch:** DRF throttling, database indexing, OpenAPI documentation generation, and E2E testing.
