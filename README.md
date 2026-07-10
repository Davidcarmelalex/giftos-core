# GiftOS Core

> **The Operating System for Digital Gift Card Markets.**

GiftOS Core is the foundational engine of the GiftOS ecosystem — an open infrastructure platform for building gift card trading systems, market intelligence, automation, and treasury management.

## Vision

Become the **Bloomberg Terminal for Digital Gift Cards**.

## Features

| Module | Status | Description |
|--------|--------|-------------|
| Market Intelligence | 🚧 In Progress | Real-time price tracking across Apple, Amazon, Steam, Google Play |
| AI Pricing | 📋 Planned | ML-driven fair value estimation |
| Portfolio Engine | 📋 Planned | Multi-account inventory & PnL tracking |
| Analytics | 📋 Planned | Time-series dashboards & trade analytics |
| Exchange Connectors | 🚧 In Progress | NoOnes API integration (OAuth, Offers, Trades, Wallet, Webhooks) |
| REST API | 📋 Planned | Full-featured developer API |
| Automation | 📋 Planned | Alerts, WhatsApp, Telegram bots |

## Architecture

```
                    ┌─────────────────────────────────┐
                    │           GiftOS Core           │
                    └──────────────┬──────────────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
   ┌──────▼──────┐        ┌────────▼────────┐      ┌───────▼──────┐
   │   Market    │        │    Trading      │      │   Analytics  │
   │ Intelligence│        │     Engine      │      │   & Reports  │
   └──────┬──────┘        └────────┬────────┘      └──────────────┘
          │                        │
   ┌──────▼──────┐        ┌────────▼────────┐
   │  AI Pricing │        │ Portfolio Engine│
   └─────────────┘        └──────┬──────────┘
                                │
                    ┌───────────┴───────────┐
                    │  Exchange Connectors  │
                    │  NoOnes · OTC · Ent.  │
                    └───────────────────────┘
```

## Quick Start

```bash
# Clone
git clone https://github.com/giftos/giftos-core.git
cd giftos-core

# Environment
cp .env.example .env
# Edit .env with your credentials

# Run with Docker
docker-compose up --build

# Or local development
pip install -e ".[dev]"
uvicorn giftos.main:app --reload
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Roadmap

| Milestone | Target | Deliverable |
|-----------|--------|-------------|
| M1 | Q3 2026 | Market Intelligence (Apple, Amazon, Steam, Google Play) |
| M2 | Q3 2026 | NoOnes Connector (OAuth, Offers, Trades, Wallet, Webhooks) |
| M3 | Q4 2026 | Dashboard — Live Prices, Charts, Portfolio, Inventory |
| M4 | Q4 2026 | Automation — AI Pricing, Alerts, WhatsApp, Telegram |
| M5 | Q1 2027 | Developer Platform — REST API, Python SDK, JS SDK |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| API Framework | FastAPI (async) |
| Database | PostgreSQL + TimescaleDB |
| Cache | Redis |
| Task Queue | Celery + Redis |
| Frontend | Next.js + Tailwind CSS |
| Charts | TradingView Lightweight Charts |
| Containers | Docker + Compose |
| CI/CD | GitHub Actions |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Security

See [SECURITY.md](SECURITY.md) for vulnerability reporting.

## License

Apache-2.0 — See [LICENSE](LICENSE) for details.

---

**GiftOS** — Open infrastructure for digital gift card markets.
