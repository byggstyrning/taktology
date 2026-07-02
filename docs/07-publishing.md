# Publishing — making `https://w3id.org/taktology#` resolve

The namespace is minted but unregistered: today no `takt:` IRI dereferences.
This doc is the path from placeholder to permanent identifier — what the
w3id.org registration needs, what it redirects to, how versions stay
resolvable, and the interim option until the PR lands. The ready-to-submit
w3id payload lives in [`w3id/taktology/`](../w3id/taktology/) in this repo.

## 1. The w3id.org registration PR

[w3id.org](https://w3id.org) is a community-run permanent-identifier service:
a redirect farm maintained as a GitHub repo, one directory per identifier.
Registration is a pull request:

1. **Fork** [`github.com/perma-id/w3id.org`](https://github.com/perma-id/w3id.org).
2. **Add a directory** `taktology/` containing exactly two files:
   - `taktology/.htaccess` — the Apache redirect rules (content negotiation);
   - `taktology/README.md` — what the identifier is for and **a named contact**
     (person + email + GitHub handle). The w3id maintainers require this; the
     contact is who they ping when a redirect target dies.
3. **Open the PR.** Maintainers usually merge small, well-formed redirect
   additions within days. Once merged, `https://w3id.org/taktology` is live —
   and permanent: w3id policy is that identifiers are never deleted, only
   re-targeted.

Both files are prepared in [`w3id/taktology/`](../w3id/taktology/) — copy the
directory into the fork verbatim.

## 2. Content negotiation — the `.htaccess`

The namespace is a **hash namespace** (`…/taktology#TaktTask`), so every term
IRI dereferences to the same document — one set of rules covers the whole
vocabulary. The rules, in order (first match wins):

```apache
# https://w3id.org/taktology — taktology ontology redirects
Options +FollowSymLinks
RewriteEngine on

# 1. Version-IRI snapshots: /taktology/X.Y.Z -> the git-tagged takt.ttl
RewriteRule ^([0-9]+\.[0-9]+\.[0-9]+)/?$ https://raw.githubusercontent.com/byggstyrning/taktology/v$1/ontology/takt.ttl [R=302,L]

# 2. JSON-LD context for developers: /taktology/context
RewriteRule ^context/?$ https://raw.githubusercontent.com/byggstyrning/taktology/main/contexts/takt.context.jsonld [R=302,L]

# 3. Turtle for machines (the namespace IRI and every takt: term)
RewriteCond %{HTTP_ACCEPT} text/turtle [OR]
RewriteCond %{HTTP_ACCEPT} application/x-turtle
RewriteRule ^$ https://raw.githubusercontent.com/byggstyrning/taktology/main/ontology/takt.ttl [R=302,L]

# 4. Everything else (browsers): human-readable documentation
RewriteRule ^ https://github.com/byggstyrning/taktology [R=302,L]
```

Design notes:

- **Rule order matters.** The version rule sits *ahead* of the catch-all so
  `https://w3id.org/taktology/0.5.0` is not swallowed by the HTML fallback.
- **The HTML target is a placeholder.** The repo front page is the
  human-readable documentation until a proper docs page exists (pyLODE/WIDOCO
  render, or GitHub Pages — see §4). Re-targeting later is a one-line w3id PR.
- **No `application/ld+json` arm yet** — there is no JSON-LD *serialization*
  of the ontology committed (the `contexts/` file is a context, not the
  ontology). Add the arm only once `ontology/takt.jsonld` exists
  (`Graph().parse("ontology/takt.ttl").serialize(format="json-ld")`);
  a conneg rule pointing at a nonexistent file redirects to a 404.
- **Known limitation:** `raw.githubusercontent.com` serves Turtle as
  `text/plain`, not `text/turtle`. Every RDF library copes (they parse by
  explicit format, not response header), and w3id-registered ontologies do
  this in practice — but GitHub Pages serves `.ttl` with the correct MIME
  type, so once Pages is enabled (§4), re-point rules 1–3 at the Pages host.

## 3. Version-IRI policy

- **Unversioned IRI = latest.** `https://w3id.org/taktology` (and every
  `…#Term`) always resolves to the current `main` ontology.
- **Versioned IRI = immutable snapshot.** Each release declares
  `owl:versionIRI <https://w3id.org/taktology/X.Y.Z>`, which resolves via
  rule 1 to the **git tag** `vX.Y.Z` — no per-version file copies to
  maintain; the tag *is* the snapshot. This only works if every release is
  tagged (checklist, §5).
- `owl:priorVersion` points at the previous release's version IRI, giving a
  machine-walkable version chain.
- What warrants which bump is defined in [`CHANGELOG.md`](../CHANGELOG.md)
  (pre-1.0: MINOR = semantics-affecting, PATCH = annotations/docs only).

## 4. Interim serving — GitHub Pages, until (and after) w3id lands

TopologicPy is the model: `w3id.org/topologicpy` 302-redirects to a GitHub
Pages host serving the raw TTL. The same setup here:

1. Repo → Settings → Pages → deploy from branch `main`, root `/`.
2. `ontology/takt.ttl` becomes fetchable at
   `https://byggstyrning.github.io/taktology/ontology/takt.ttl`
   — with `Content-Type: text/turtle`, which raw GitHub does not provide.
3. Link that URL from the README as the interim namespace document until the
   w3id PR merges; afterwards it is the better redirect *target* for §2's
   rules 1–3 (and the repo README or a docs page for rule 4).

This costs nothing and requires no PR to anyone — it can be done today.

## 5. Release checklist

Cut a release in this order (the diagram script keys its output filename off
`owl:versionInfo` — bump it first or the previous version's PNG is silently
overwritten):

1. **Bump the ontology header** in `ontology/takt.ttl`, all three together:
   - `owl:versionInfo "X.Y.Z"`
   - `owl:versionIRI <https://w3id.org/taktology/X.Y.Z>`
   - `owl:priorVersion <https://w3id.org/taktology/[previous]>`
   - and refresh `dcterms:modified`.
2. **CHANGELOG.md** — add the `[X.Y.Z]` entry (Added / Changed / Removed /
   Fixed; call out BREAKING changes and migration steps).
3. **Validate** — `python scripts/validate.py` green (parse, SHACL, term
   consistency, upstream pins in `ontology/alignments.lock.json`).
4. **Regenerate the diagram** — `python scripts/generate_ontology_diagram.py`
   (emits `docs/diagrams/taktology-vX.Y.Z.png`; history kept, one per version).
5. **Commit and tag** — `git tag vX.Y.Z && git push --tags`. The tag is what
   the version IRI resolves to (§3) — an untagged release breaks its own
   `owl:versionIRI`.
