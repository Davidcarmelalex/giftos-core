# GiftOS Core Architecture

## Overview

GiftOS Core is a modular, event-driven platform built around a central message bus. Each module is independently deployable and communicates via async message queues and REST APIs.

## System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         GiftOS Core                              │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Market     │  │   Trading    │  │     Analytics        │  │
│  │ Intelligence │  │   Engine     │  │     & Reports        │  │
│  │              │  │              │  │                      │  │
│  │ • Scrapers   │  │ • Order Mgmt │  │ • Time-series DB     │  │
│  │ • Price DB   │  │ • Risk Mgmt  │  │ • Dashboard API      │  │
│  │ • Spread Eng │  │ • Execution  │  │ • Export (CSV/PDF)   │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────────────────┘  │
│         │                 │                                      │
│  ┌──────▼───────┐  ┌──────▼───────┐                             │
│  │  AI Pricing  │  │  Portfolio   │                             │
│  │              │  │   Engine     │                             │
│  │ • Fair Value │  │              │                             │
│  │ • Trend Pred │  │ • Inventory  │                             │
│  │ • Anomaly Det│  │ • PnL Calc   │                             │
│  └──────────────┘  └──────┬───────┘                             │
│                           │                                      │
│         ┌─────────────────┼─────────────────┐                  │
│         │                 │                 │                  │
│  ┌──────▼──────┐  ┌───────▼───────┐  ┌──────▼──────┐            │
│  │   NoOnes    │  │  Future: OTC  │  │  Future:    │            │
│  │  Connector  │  │   Desks       │  │ Enterprise  │            │
│  │             │  │               │  │   APIs      │            │
│  │ • OAuth 2.0 │  │               │  │             │            │
│  │ • Offers    │  │               │  │             │            │
│  │ • Trades    │  │               │  │             │            │
│  │ • Wallet    │  │               │  │             │            │
│  │ • Webhooks  │  │               │  │             │            │
│  └─────────────┘  └───────────────┘  └─────────────┘            │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Infrastructure Layer                         │   │
│  │  PostgreSQL  │  Redis  │  Celery  │  FastAPI  │  Docker   │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Module Descriptions

### Market Intelligence
- **Scrapers**: Async workers that poll gift card marketplaces and public price feeds
- **Price DB**: Time-series storage in PostgreSQL with TimescaleDB extension
- **Spread Engine**: Calculates real-time buy/sell spreads and arbitrage opportunities

### Trading Engine
- **Order Management**: Abstracts offer creation, trade lifecycle, and settlement
- **Risk Management**: Position limits, exposure caps, and automated circuit breakers
- **Execution**: Smart order routing across connected exchanges

### AI Pricing
- **Fair Value Model**: Statistical regression on historical price data
- **Trend Prediction**: Lightweight time-series forecasting (Prophet / ARIMA)
- **Anomaly Detection**: Flags unusual price movements for manual review

### Portfolio Engine
- **Inventory**: Real-time tracking of gift card holdings across brands
- **PnL Calculation**: Realized and unrealized profit/loss with cost-basis methods
- **Rebalancing**: Suggestions for portfolio optimization

### Analytics & Reports
- **Time-series DB**: Aggregated metrics for dashboard visualization
- **Dashboard API**: REST endpoints powering the Next.js frontend
- **Export**: CSV/PDF generation for accounting and tax reporting

## Data Flow

```
External Sources          GiftOS Core                  Consumers
     │                         │                           │
     ▼                         ▼                           ▼
┌─────────┐            ┌─────────────┐            ┌─────────────┐
│ NoOnes  │───────────▶│  Connectors │───────────▶│  Portfolio  │
│  API    │            │  (Adapter)  │            │   Engine    │
└─────────┘            └─────────────┘            └─────────────┘
     │                         │                           │
┌─────────┐            ┌─────────────┐            ┌─────────────┐
│ Scrapers│───────────▶│   Market    │───────────▶│  Analytics  │
│ (Web)   │            │ Intelligence│            │   & Reports │
└─────────┘            └─────────────┘            └─────────────┘
                              │
                              ▼
                       ┌─────────────┐
                       │  AI Pricing │
                       │   Engine    │
                       └─────────────┘
```

## Technology Choices

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| API Framework | FastAPI | Async-native, OpenAPI auto-generation, Python ecosystem |
| Database | PostgreSQL + TimescaleDB | ACID compliance, time-series optimization |
| Cache | Redis | Session store, rate limiting, pub/sub for real-time updates |
| Task Queue | Celery + Redis | Background jobs, scheduled scrapers, webhook retries |
| Frontend | Next.js + Tailwind | SSR for SEO, component-based UI, rapid development |
| Charts | TradingView Lightweight | Professional-grade financial charting, free tier |
| Containers | Docker + Compose | Reproducible environments, easy onboarding |
| CI/CD | GitHub Actions | Native GitHub integration, matrix testing |

## Security Model

- **API Authentication**: JWT tokens with scoped permissions
- **Webhook Verification**: HMAC-SHA256 signature validation
- **Secrets Management**: Environment variables only; no secrets in code
- **Rate Limiting**: Per-API-key limits via Redis
- **Audit Logging**: Immutable log of all sensitive operations
- **Input Validation**: Pydantic models for all request/response schemas

## Scalability Considerations

- **Horizontal Scaling**: Stateless API servers behind a load balancer
- **Database**: Read replicas for analytics queries; write-optimized primary
- **Caching**: Aggressive Redis caching for price feeds (TTL: 30s)
- **Workers**: Celery workers can be scaled independently based on queue depth
- **Webhooks**: Async processing with exponential backoff and dead-letter queues
