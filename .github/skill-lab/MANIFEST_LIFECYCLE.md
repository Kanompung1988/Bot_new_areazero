# Repository provisioner request manifest lifecycle

The GitHub Actions workflow validates up to 15 requested repositories per batch, and processes existing repositories idempotently. A request manifest is the **current desired provisioning batch** rather than an unbounded archive. Prior snapshots live in `.github/skill-lab/history/`; individual released code provenance and idempotency records live in the public `Kanompung1988/agent-skills/docs/EPISODES.md` and each standalone repository.

**2026-11-01 EP.08:** preserve the original 14-entry manifest unchanged as `history/2026-10-31-requests.json`, then request two new repositories. Do not delete or alter any previously released repository. This procedure preserves auditability while keeping the workflow's bounded request validation intact.

Never publish social posts as part of this workflow. Skill Lab Instagram/Facebook distribution remains OFF until explicit user reauthorization.
