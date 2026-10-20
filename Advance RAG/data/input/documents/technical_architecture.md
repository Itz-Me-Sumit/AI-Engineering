# TechNova Platform Technical Notes

Public API endpoints use HTTPS and JSON. OAuth 2.0 client credentials is
recommended for server integrations. API keys are supported for legacy
clients but cannot be created after June 30, 2026. Access tokens expire
after 60 minutes.

The default API rate limit is 600 requests per minute per tenant. A
`429` response includes `Retry-After`; clients should use exponential
backoff with jitter. Idempotency keys are retained for 24 hours on
supported POST endpoints.

Webhooks are signed with HMAC-SHA256. Consumers must verify the
`X-TechNova-Signature` header against the raw request body and reject
timestamps older than five minutes. Delivery is attempted six times
over 24 hours. Event IDs should be stored to prevent duplicate work.

Production runs in isolated tenant namespaces across US and EU regions.
Nightly encrypted backups are retained for 35 days. The published
recovery point objective is 24 hours and recovery time objective is
8 hours for the core platform.
