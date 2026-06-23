# dlouhy-2016-three-level

- **Title:** Three-Level Method of Takt Planning and Takt Control – A New Approach for Designing Production Systems in Construction
- **Authors / Year:** Dlouhy, J.; Binninger, M.; Oprach, S.; Haghsheno, S. — 2016
- **Venue:** IGLC 24, Boston, USA · [landing](https://iglc.net/Papers/Details/1350) · OA [PDF](https://iglc.net/Papers/Details/1350/pdf)
- **Status:** adopted · **Cluster:** takt-foundations · **Verified:** ✔

## Summary
Introduces the Karlsruhe (KIT) three-level hierarchy for defining takt and its
workspaces — macro / normal (functional) / micro levels — giving managers
transparency and controllability across phases. Case study: 11→5 month duration via
interlinked phases.

## Key takeaways
- Takt zones are not flat: a macro area decomposes into normal zones, which decompose
  into micro work areas. A planning construct, not a fixed storey/room.
- Multi-scale structure is directly modellable as a layered zoning.

## Distinct contribution
The standardization backbone for structuring takt at multiple levels of detail.

## Overlap / what it is NOT
The **zone hierarchy** paper — distinct from same-author `haghsheno-2016-history`
(theory) and `binninger-2017-technical-takt` (control). Its extensions ("Mastering
Complexity" 2018, etc.) build on this.

## How it shapes taktology (intertwine)
Supports modelling `takt:TaktZone` as a `top:FunctionalZone` (the "normal/functional"
level) that can nest finer zones — see
[`docs/02-vocabulary.md`](../../docs/02-vocabulary.md) and the FunctionalZone choice in
[`docs/01-architecture.md`](../../docs/01-architecture.md). Confirms a takt zone is a
programme construct, justifying the `top:FunctionalZone` subclass over a structural zone.
