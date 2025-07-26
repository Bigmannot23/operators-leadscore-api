# Operators Leadscore API

## Elevator pitch
Quickly score leads with a simple, secure API. This FastAPI microservice accepts contact details and returns a quality score to prioritize outreach.

## Usage
1. Clone this repository and install dependencies.
2. Run the FastAPI app using Uvicorn.
3. Request an API key via the provided script or admin endpoint.
4. Call `/score` with your API key and lead data to receive a score.

## Architecture
- Endpoint `/score` accepts lead information (name, company, etc.) and returns a 0–100 score.
- API key management controls access via the `x-api-key` header.
- Integration ready: easy to plug into CRMs or other systems with JSON responses.
- Customizable: swap out the scoring logic for your own model or heuristics.

![Diagram](./assets/diagram.png)

## Results & ROI
- **Improved lead qualification and conversion rates** — evidence: CRM analytics
- **Ability to deploy new scoring models within minutes** — evidence: Deployment logs
- **Secure access with API keys and authentication** — evidence: Security audit

## Part of the Operator Meta Portfolio
- [AI Code Review Bot](../ai_code_review_bot/OPERATOR_README.md)
- [Job Offer Factory](../job_offer_factory_autorun/OPERATOR_README.md)
- [Onboarding Assistant](../Onboarding_Assistant/OPERATOR_README.md)
- [Lexvion Compliance Engine](../lexvion/OPERATOR_README.md)
- [Lexvion Trading Bot](../lexvion_trading_bot_full_auto/OPERATOR_README.md)
- [Operator Metrics Dashboard](../operator_metrics_dashboard/OPERATOR_README.md)
- [Meta Portfolio](../meta_portfolio/README.md)

## Operator principles
Automation first, modularity, operator focus and compounding learning.
