# Information Security Policy (Version 4.2)

TechNova requires phishing-resistant multi-factor authentication for
administrators and employees accessing production. Customer accounts
support SAML SSO on qualifying plans. Production access follows least
privilege and is reviewed quarterly by the Security team.

Data is encrypted with AES-256 at rest and TLS 1.2 or later in transit.
Customer content is not used to train shared machine-learning models
without explicit written opt-in. Security logs are retained for 400
days; application logs are retained for 90 days.

Suspected security incidents must be reported to security@technova.example
immediately. Security acknowledges validated customer reports within one
business day. TechNova targets customer notification within 72 hours of
confirming an incident that affects customer data, subject to applicable
law and investigation constraints.

Secrets must be stored in the approved secrets manager, never in source
code, tickets, or chat. Critical vulnerabilities have a 7-day remediation
target; high vulnerabilities have a 30-day target.
