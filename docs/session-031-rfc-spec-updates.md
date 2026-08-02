# Session 031 — RFC-CDP-030/031 Spec Updates

Status: implementation complete (documentation-only, no code changes),
confirmed passing in CI (`RFC Index Integrity` run `30747550527` and
`CDP CI` run `30747550523`, both on head commit `28c42ef`, see §5). Not
yet reviewed/merged (PR #47). This file documents what already exists in
the working tree, not a plan for future work.

Scope: bring RFC-CDP-030 (Identify Protocol) and RFC-CDP-031 (Attest
Protocol) up to date with what four development sessions (027-030) have
actually built against their minimal requirements, and fix a stale
internal header both files carried since before they were renumbered
into the 030-039 identity band. Requested directly as the fifth of the
five follow-up items named in review of PR #41's evidence layer
("RFC-CDP-030/031 updates").

## 1. Scope note (read this first)

This is documentation-only. No file under `cdp/`, `db/ddl/`, or `tests/`
changed in this session -- only `rfc/RFC-CDP-030-Identify-Protocol.md`
and `rfc/RFC-CDP-031-Attest-Protocol.md`. Nothing about the running
system's behavior changes; this session brings the specification text
into alignment with code that already exists (sessions 027-030), and
does not itself authorize or imply any new implementation work.

## 2. What this slice does

### 2.1 Fixes the stale header (a real, previously-flagged gap)

Both files' first line read `# RFC-CDP-012 — Identify Protocol` and
`# RFC-CDP-011 — Attest Protocol` respectively -- their numbers from
before the identity band was renumbered to 030-039. `scripts/verify_rfc_index.py`
was already flagging this exact drift as a non-fatal `WARN`:

```
WARN: legacy RFC number remains in header: RFC-CDP-030-Identify-Protocol.md manifest=030, header=012
WARN: legacy RFC number remains in header: RFC-CDP-031-Attest-Protocol.md manifest=031, header=011
```

Both headers are now corrected to `# RFC-CDP-030 — Identify Protocol`
and `# RFC-CDP-031 — Attest Protocol`. Running the check again after
this change confirms both `legacy RFC number` warnings for these two
files are gone (see §5).

### 2.2 Adds an Implementation Status section to each RFC

Both RFCs are bumped to Draft v0.4 (from v0.3), with `Updates: RFC-CDP-0NN v0.3`
and `Related:` header fields added, matching the convention already
established by RFC-CDP-041's own Draft v0.4 promotion. §§1-5 (Identify)
and §§1-6 (Attest) are otherwise **unchanged** from Draft v0.3 -- they
remain the forward-looking specification text. A new final section is
added to each (§6 for Identify, §7 for Attest) documenting what the real
implementation has built, explicitly cross-referenced against the
original spec's own required elements, and explicitly honest about what
is *not* met:

- **RFC-CDP-030 §6** documents `cdp_core.actor` (session 027) against §2/§3,
  the Identity Claim recognition state machine (session 027) and its
  session-030 optional registry/decision-class scope, and clarifies that
  §1's "how identity links to authority" is answered by RFC-CDP-032, not
  by this RFC -- Identity Claim recognition itself does not grant
  authority.
- **RFC-CDP-031 §7** documents `cdp_core.attestation_record` (session 027)
  against §3, and states plainly that **§4's cryptographic verification
  requirements are not implemented** -- "verification" in the running
  system means the actor is active and holds a recognized, in-scope
  Identity Claim, not a checked signature. `attestation_method:
  cryptographic_signature` is an accepted vocabulary value that triggers
  no different verification path than any other method. It also
  documents §2's "all mutating acts MUST be attested" against the five
  governed act types actually covered as of session 029
  (`decision_created`, `challenge_raised`, `challenge_adjudicated`,
  `execution_authorized`, `execution_recorded`), and names what's
  excluded (Test/Legitimize/Learn -- no service function exists;
  Identity/Attestation/Authority's own mutations -- deliberately
  excluded as circular).

## 3. Objects added

None. No schema, table, route, or service function changed.

## 4. Files changed

- `rfc/RFC-CDP-030-Identify-Protocol.md`
- `rfc/RFC-CDP-031-Attest-Protocol.md`

## 5. Verification

`python3 scripts/verify_rfc_index.py` run before and after this change:

- **Before**: 4 warnings for these two files (2× `legacy RFC number
  remains in header`, 2× `manifest/header status drift`).
- **After**: 2 warnings for these two files (the `legacy RFC number`
  warnings are gone; `manifest/header status drift` remains, since
  `rfc/index/rfc-manifest.json` records status as the generic string
  `"Draft"` for both entries, not a minor-version-specific string, and
  updating that manifest field granularity for all 46 entries is out of
  scope for this session -- see §7).
- Exit code both times: `0` ("RFC index verification passed") -- this
  check has never treated either warning class as fatal (see
  `evidence/003-known-gaps.md`'s "RFC index/manifest verification"
  section).

No `cdp/` code changed, so `ruff check cdp` and the full local test
suite are unaffected; not re-run for this session since there is nothing
in this diff for them to exercise.

**GitHub Actions:** confirmed. The relevant CI check for this session is
`.github/workflows/rfc-index-integrity.yml` (triggers on any push/PR
touching `rfc/**`), not `cdp-ci.yml`'s `full-cdp-slice-tests` (no
Postgres/API-touching change exists to run, and it correctly did not
run since this PR carries no `run-full-ci` label). Both checks passed on
the first run: `RFC Index Integrity` run `30747550527` and `CDP CI`
(`pr-guard` only) run `30747550523`, both on head commit `28c42ef`,
2026-08-02T12:18:29Z, conclusion `success`.

## 6. Evidence level reached

Not applicable in the E0-E5 sense `evidence/000-current-state.md` uses --
that scale rates governed-act *capabilities*, and this session adds none.
The relevant evidence-layer change is narrower: `003-known-gaps.md`'s
existing "RFC-CDP-030 and RFC-CDP-031 remain underspecified relative to
the implemented schema" bullet is updated to note the stale-header
portion of that gap is now closed, while the schema-still-not-directly-
specified-by-the-RFC-text portion remains (necessarily -- these RFCs
still specify no persistence schema in their original §§1-5/1-6, by
design; §6/§7 document an interpretation, not a promotion of that
interpretation into the RFC's own normative requirements).

## 7. Known limitations

- **`rfc/index/rfc-manifest.json` still shows generic `"Draft"` status**
  for both entries, not `"Draft v0.4"` -- this is the same
  manifest-granularity drift already documented across ~15 other RFCs in
  `evidence/003-known-gaps.md`'s "RFC index/manifest verification"
  section, not something newly introduced or newly fixed here.
- **§7.1's cryptographic-verification gap is now documented, not
  closed.** This session makes the RFC text honest about the
  implementation; it does not implement RFC-CDP-031 §4.
- **This is a specification-alignment pass, not a specification
  revision.** §§1-5 (Identify) and §§1-6 (Attest) -- the original
  forward-looking requirements -- are untouched. Nothing here narrows or
  loosens what those RFCs ask of a future, fuller implementation.

## 8. Explicit non-goals (all held to)

Not implemented by this slice: any code change, real cryptographic
verification (RFC-CDP-031 §4), real caller authentication, RFC-manifest
version-granularity reconciliation across the wider corpus, revision of
the original forward-looking requirement sections.

## 9. Context-plane note

This file follows the pattern set by `docs/session-030-identity-claim-scope.md`:
written before staging/committing, so the working tree's actual state is
recorded before it potentially changes. See `docs/SESSION-INDEX.md` for
where this fits in the implementation-session sequence.
