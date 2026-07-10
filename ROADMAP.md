# GiftOS Core Roadmap

## Milestone 1: Market Intelligence Engine
**Target: Q3 2026**

- [ ] Price scrapers for Apple, Amazon, Steam, Google Play gift cards
- [ ] Historical price database (PostgreSQL time-series)
- [ ] Spread calculation engine (buy vs sell margins)
- [ ] Basic REST endpoints for price queries
- [ ] Docker compose setup with Postgres + Redis

## Milestone 2: NoOnes Connector
**Target: Q3 2026**

- [ ] OAuth 2.0 client-credentials authentication
- [ ] Offer listing and filtering
- [ ] Trade lifecycle management
- [ ] Wallet balance queries
- [ ] Webhook receiver for trade events
- [ ] Rate limiting and retry logic

## Milestone 3: Dashboard & Visualization
**Target: Q4 2026**

- [ ] Next.js frontend with Tailwind CSS
- [ ] Live price tables with auto-refresh
- [ ] TradingView Lightweight Charts integration
- [ ] Portfolio overview (inventory, PnL)
- [ ] Inventory management UI

## Milestone 4: Automation Layer
**Target: Q4 2026**

- [ ] AI-driven pricing model (fair value estimation)
- [ ] Alert system (price thresholds, spread anomalies)
- [ ] WhatsApp bot integration
- [ ] Telegram bot integration
- [ ] Automated offer posting (with safety limits)

## Milestone 5: Developer Platform
**Target: Q1 2027**

- [ ] Full REST API documentation (OpenAPI 3.0)
- [ ] Python SDK (`giftos-sdk-python`)
- [ ] JavaScript/TypeScript SDK (`giftos-sdk-js`)
- [ ] Webhook management portal
- [ ] API key management with scoped permissions

## Future

- [ ] Additional exchange connectors (Paxful legacy, OTC desks)
- [ ] Enterprise API tier
- [ ] On-chain settlement tracking
- [ ] Multi-signature treasury management
- [ ] Regulatory compliance module (KYC/AML hooks)
