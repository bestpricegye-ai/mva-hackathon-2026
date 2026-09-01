# Track 2 Report — Drug Repurposing for MVA1 (BUB1B)

**Team:** byronzunigao
**Proband:** PROBAND01 (WGS_EX2312012, MVA1, OMIM #257300)
**Date:** 2026-08-31

---

## 1. Team name
byronzunigao

## 2. Approach: from variant/mechanism to candidate medication(s)

**Context (from Track 1):** the child carries a **compound-heterozygous (biallelic) BUB1B** genotype —
a stop-gained LoF (p.Leu737Ter) plus a novel, likely-pathogenic missense (p.Asn1002Lys, kinase-domain C-terminus,
AlphaMissense 0.923). BUB1B encodes **BUBR1**, a kinase that is **haploinsufficient**: the canonical MVA1
mechanism is **loss-of-function** of the Spindle Assembly Checkpoint (SAC), impairing inhibition of
APC/C-Cdc20 and causing chromosome mis-segregation (mosaic variegated aneuploidy).

**Repurposing logic.** We started from the *mechanism of the affected protein*, not from a disease label:
because BUBR1's defect is **loss of function via reduced protein levels/activity**, the intervention that
restores the protein's *dosage/function* — not its defective sequence — is the most rational repurposing
candidate. We then applied a safety gate: any agent that **further weakens the SAC** is contraindicated.
Candidates were tiered by evidence quality (in-vivo/ex-vivo mechanistic support) and clinical availability.

**Final candidates (ranked):**

1. **NMN / NAD+ precursor (off-label/experimental)** — SIRT2 deacetylates BUBR1 (K668), and restoring
   NAD+ raises BUBR1 levels *in vivo* in hypomorphic mice, increasing median lifespan and reducing
   aneuploidy/cancer. *The only published strategy that directly raises the affected protein's levels.*
2. **Senolytics (dasatinib + quercetin, investigational)** — cellular senescence (p16/p19/p21/p53)
   mediates the progeroid tissue degeneration of BUBR1 insufficiency; clearing senescent cells attenuates
   muscle/fat/lens degeneration. Use **only** under oncology given the rhabdomyosarcoma.
3. **Growth hormone (approved, standard-of-care)** — standard management of the growth failure / short
   stature in MVA (Orphanet #1052). Not a repurposing novelty — supportive care.

**Explicitly contraindicated:** anti-mitotic / SAC-weakening drugs (taxanes, vincristine, MPS1/TTK
inhibitors such as reversine, BAY-1161909) — these collapse an already-defective checkpoint and worsen
aneuploidy. This is a negative/guardrail result and itself a clinically useful deliverable.

**Integrated plan:** 3-monthly oncology surveillance; standard pediatric rhabdomyosarcoma regimen; growth
hormone for growth; NMN/NAD+ as a monitored experimental rescue of BUBR1 levels; senolytics only under
oncology with demonstrated senescence burden; **parental segregation genotyping** to close the in-trans
diagnosis and enable recurrence counseling (25% per-pregnancy risk if both parents are carriers).

## 3. Generative-AI / LLM disclosure *(required)*

- **Provider / model:** Anthropic API, Claude (commercial terms), used for literature synthesis and
  hypothesis organization of the drug-repurposing rationale.
- **Plan / tier:** commercial API terms; no training on customer content.
- **Data handling:** no patient-identifying data beyond the challenge clinical text; data deleted within
  30 days of close.
- All candidate mechanisms are grounded in the **peer-reviewed primary literature cited below** (Baker et
  al. Nat Cell Biol 2013; North et al. EMBO J 2014), not fabricated by the LLM.

## 4 / 5. Automated vs. manual curation

Candidate identification was a **hybrid: LLM-assisted search + expert manual curation of primary
literature**. We explicitly screened the RDCRN repurposing framework review (Lumsden & Urv 2023) and
confirmed it contains **no MVA1-specific drug**; our candidates derive from the functional BUBR1 pathway
evidence, not from that article — documented for honesty.

## 6 / 7 / 8. Data sources (public only)

- **Public:** OMIM (MVA1 #257300), PubMed (Baker NCB 2008/2013, ncb2643; North EMBO J 2014, PMC4194088),
  Orphanet #1052, ClinVar. **No proprietary drug/target databases used.**

## 9. Variant mechanism characterization

- **Type:** compound-heterozygous LoF (PVS1) + likely-pathogenic missense.
- **Pathway disrupted:** Spindle Assembly Checkpoint → reduced inhibition of APC/C-Cdc20 → premature
  chromatid separation / aneuploidy.
- **Downstream consequence:** chromosome instability (CIN), cancer predisposition, progeroid/senescence
  tissue degeneration, growth failure.

## 10. Effort estimate

~2–4 h including literature verification and the negative-screen (anti-mitotic guardrail).

## 11. Method abstract (≤500 words)

We characterized the mechanism of the confirmed BUB1B (MVA1) variant pair and derived drug-repurposing
candidates from the biology of the affected protein rather than from a disease label. The key insight is
that BUB1B/BUBR1 is haploinsufficient and its defect is loss of function; therefore the rational rescue is
to **restore BUBR1 levels/activity** — supported by in-vivo data that BUBR1 overexpression protects against
aneuploidy, cancer, and extends healthy lifespan, while SIRT2-mediated deacetylation of K668 raises BUBR1
in hypomorphic mice.

This gives our top repurposing candidate, **NMN/NAD+** (a commercial dietary supplement that raises BUBR1
levels through the SIRT2 axis) as an experimental, IRB-supervised rescue. Secondary candidates include
**senolytics** to clear BUBR1-insufficiency-driven senescence and **growth hormone** as standard growth
management. We explicitly flag anti-mitotic / MPS1-TTK inhibitors as **contraindicated** because they
further destabilize the SAC.

**Strengths:** mechanism-first (not label-first); candidates track the actual protein affected; includes a
clinically actionable negative (contraindication list); integrates oncology surveillance, growth
management, and reproductive recurrence counseling into one care plan; fully public data.

**Limitations:** NMN/NAD+ and senolytics are **not approved for this indication** and are hypothesis-for-
follow-up, not evidence of efficacy; BUBR1-level restoration is only partially characterized (SIRT2 did not
fully rescue); the patient's active rhabdomyosarcoma constrains the use of any pro-mitotic-altering agent;
parental segregation remains pending.

**Scalability:** the mechanism-first repurposing framework (map LoF haploinsufficient gene → identify
dosage/level-restoring axis → safety-gate the pathway) generalizes to other haploinsufficiency and
chromosomal-instability disorders.
