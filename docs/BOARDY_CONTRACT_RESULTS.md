# Boardy contract review · November 21, 2026

On rc21 a missing fact name and a name shared by two facts both returned the
same `UNKNOWN`. The caller could not tell whether to look for another name or
ask which record was intended. Replaying the same 11 MCP calls on installed
rc22 produced `FACT_NOT_FOUND` for the miss and `AMBIGUOUS_NAME` with both
candidate keys for the collision. The two unique-name controls passed on both releases.

**Installed Dandelion 1.0.0rc22 passed the same 14 frozen cases twice on one
Windows machine.** The repeat ran every case once against fresh test memory.

| Contract measure | First run | Repeat |
| --- | --- | --- |
| Positive operations and safeguards | 10/10 | 10/10 |
| Correct uncertainty outcomes | 4/4 | 4/4 |
| Exact-name lookalikes and near misses (subset) | 2/2 | 2/2 |

This establishes repeatability for these fixtures on Windows with Python 3.13
and local stdio MCP. Linux, macOS and network transports were outside this
review. Agent answer accuracy and external pilot usability remain unmeasured.

The [case list](BOARDY_CONTRACT_CASES.md) was frozen on November 19 for the original
rc21 baseline (Git blob `0a289633d0d36ee226fa8cd0caeee6b20f490814`).
rc21 passed C05 and C06 and failed C07 and C08. Those results stand. This report
applies the same criteria to rc22 using only installed rc22 evidence. All three
original batches and all three repeat batches used the same installed PyPI wheel. Its
SHA-256 is `dae5cf3e179aa1fcb3c52b06678920f92908b4837d096e90f3dafa2deb249056`.

| Case | Observed through MCP | Result in both runs |
| --- | --- | --- |
| C01 | After acknowledged writes and forced owner termination, a different owner returned 8080 at r1 and resolved the pin. **First run caveat:** Windows denied the harness permission to read the terminated process's exit code directly. The recovery read resumed on the same test memory, with no repeated seed writes. **Repeat:** the harness requested permission to query the verified disposable process handle, observed exit code 73 and completed recovery without interruption. | Pass |
| C02 | A normal restart of the same package preserved the fact, pin and single-revision inventory. | Pass |
| C03 | Two notes resolved to one original with the supplied CRLF bytes and matching digest. | Pass |
| C04 | After creation and three corrections, a restart preserved all four values under the same key. Current returned r4. | Pass |
| C05 | Similar service and worker names returned their own keys and port values. | Pass |
| C06 | The retries lookup returned 3 despite the similarly named timeout. | Pass |
| C07 | The absent name returned FACT_NOT_FOUND without choosing a value. | Pass |
| C08 | The colliding name returned AMBIGUOUS_NAME and both candidate keys without choosing a value. | Pass |
| C09 | Order O-001 existed. Reading tracking returned FIELD_NOT_STORED, the entity and field, with no value member. | Pass |
| C10 | Reading the January–June fact as of August 1 returned UNKNOWN / NO_EFFECTIVE_REVISION with no value member. | Pass |
| C11 | Updating 8080 with expected r1 returned r2. Current returned 8081. | Pass |
| C12 | The original note rendered “Now: 8081; before: 8080”. Its links resolved to the same key at r2 and r1 respectively. | Pass |
| C13 | Two concurrent client sessions read r1. After A's update, B's stale write of 9999 returned CONFLICT / REVISION_MISMATCH. The inventory contained only r1 and r2 and the history contained one correction. | Pass |
| C14 | Both note texts and their source and producer remained readable. The successor linked to its predecessor. Their respective SUPERSEDED and ASSERTED_CORRECTION events retained “Port migrated”. | Pass |

## How an agent should handle uncertainty

| Observed reply | Safe next action for the client |
| --- | --- |
| `UNKNOWN / FACT_NOT_FOUND` | No visible fact matched the requested name. Check the spelling, project or original source before reporting an absence or creating a fact. |
| `UNKNOWN / AMBIGUOUS_NAME` | Compare the returned candidate keys against the task or ask which record was intended. Read the identified key only when the evidence resolves the ambiguity. |
| `FIELD_NOT_STORED` | Report that the named entity has no stored value for the requested field. Preserve the distinction from an explicit null. |
| `UNKNOWN / NO_EFFECTIVE_REVISION` | Report that the recorded periods do not establish a value for the requested date. A current value does not fill that gap. |

Clients should allow for other or missing reason codes. Preserve the returned
status and reason, leave the value unresolved, and request clarification or
independent evidence if the task needs a value. An unfamiliar reason alone
does not justify selecting a candidate or writing a replacement. Access denials
and transport errors are separate outcomes. No agent selected tools or graded
these cases; actual client behavior is a question for the two-session pilot.

## Evidence

Windows, Python 3.13, public stdio MCP, trusted-local, lifecycle enabled.
Each batch used separate test memory. C11–C13 shared the same port transition.
C13 used two open MCP clients connected to the same test owner. C01 covers
process loss after acknowledged writes.

| Batch | Local evidence folder under `scratch/boardy/` | SHA-256 of actual MCP trace |
| --- | --- | --- |
| C01–C04 | `rc22-C01-C04-c99ca572ae` | `f4ac91057ecebd3712a041b51a17d119884de3ab14985017d11515371c17d5df` |
| C05–C08 | `release-rc22-17785d20` | `f62faba32c0942ae8514bfa73ca9f952fcbf90e2bb51e45c7433e0d8b83d593c` |
| C09–C14 | `rc22-C09-C14-adcb6d5a` | `7de1491c3733ebbbe85c84d9df90406917e0a7aafd034a61779b4f4e2ed79e58` |
| Repeat C01–C04 | `rc22-repeat-3a9288bd/C01-C04` | `a2071298cd1ad5fb88ceba401ee48b3136c8c0b04a419bdac2ea8a55a42a859f` |
| Repeat C05–C08 | `rc22-repeat-3a9288bd/C05-C08` | `232bec841d13f5604b53fe8eaa7ad0708d6ed47a3d283b544b42e16208a01539` |
| Repeat C09–C14 | `rc22-repeat-3a9288bd/C09-C14` | `d2284f2a7a2f935107b38c3bf8689a0e9321e485a04bcbb7d838d2c7ed5841ea` |

These folders are local evidence references. Source links inside the frozen
case inventory refer to the source checkout. Each folder contains the requests and responses in `mcp.jsonl` and the case
verdicts in `verdicts.json`. The first report combined eight previously
recorded cases with six new ones. All 14 repeat verdicts came from new MCP calls
on disposable memory. All six trace digests were checked. The daily rc23
workspace was excluded from the experiment.
