# 7. Single AWS region: us-east-1

- Status: Accepted
- Date: 2026-11-26

## Context
Launch markets: Brazil, United States and Europe. Cognito user pools cannot be moved between regions, so the region must be chosen before real users exist.

## Decision
Run the whole backend in **us-east-1 (N. Virginia)**.

## Rationale
- The look engine runs on device; the app makes only a few backend calls on launch, so the extra latency from Brazil (~120–150 ms) and Europe (~80–100 ms) is not noticeable.
- Lowest cost and the widest choice of services and Bedrock models.
- One region means one deployment, one user pool and one database for a solo developer.
- LGPD and GDPR allow the international transfer with disclosure and contractual safeguards (AWS DPA with standard contractual clauses; EU-US Data Privacy Framework).

## Consequences
- The privacy policy (en, pt-BR) must disclose that data is stored in the United States and what is sent to the LLM (garment attributes and locale — never photos or the selfie).
- Photos are cached on device; a CDN (CloudFront) can be added when traffic grows.
- If a market or enterprise customer requires in-region data, the same infrastructure code can be deployed to an EU region.
- Risk: the EU-US Data Privacy Framework may be challenged in court; standard contractual clauses remain the fallback.
