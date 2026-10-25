# Corporate Agent Skills Catalog Constitution

## Core Principles

### I. Interoperability First

Skills MUST follow the official Agent Skills specification. Use only its required fields and supported optional fields; do not rely on consumer-specific metadata or tool behavior without documenting the limitation.

### II. One Clear Responsibility

Each skill MUST have one primary capability, a precise activation description, and actionable instructions. Keep essential guidance in `SKILL.md`; load detailed material from explicit, relative references only when needed.

### III. Safe, Reviewable Execution

Scripts MUST be deterministic where practical, document usage and dependencies, handle errors clearly, and use only the access needed for their task. Instructions MUST preserve applicable security, privacy, quality, and compliance requirements.

### IV. Validation Is Necessary, Not Sufficient

Every change MUST pass structural validation and relevant tests. Human review MUST also assess semantic clarity, activation boundaries, correctness, safety, contradictions, and maintainability; passing a validator alone does not establish skill quality.

### V. Traceable, Incremental Evolution

Material changes MUST be specified, planned, tasked, implemented, and reviewed with Spec Kit artifacts. Trivial documentation or metadata corrections MAY use a direct review without a full specification cycle. Do not create placeholder skills or artifacts solely to fill a directory.

## Quality and Compatibility

The catalog contract and commands are documented in `README.md`. Automated checks enforce only documented, deterministic rules; consumer-specific discovery, invocation, and permission behavior MUST be verified for the target agent and MUST NOT be assumed portable.

## Contribution Workflow

For a material change, use the repository's Spec Kit skills to create a specification, plan, and tasks; clarify or analyze when useful; implement and validate; then converge and review. For a trivial change, make the smallest edit, run the relevant checks, and explain the change in review.

## Governance

This constitution guides specifications, plans, implementation, and review. Amend it when the catalog contract or agreed quality principles change, and keep related documentation and templates consistent. Prefer established interoperable standards; document any intentional deviation and its reason.

**Version**: 1.0.0 | **Ratified**: 2026-10-25 | **Last Amended**: 2026-10-25
