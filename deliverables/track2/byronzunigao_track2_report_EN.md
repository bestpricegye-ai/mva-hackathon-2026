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
4. **Stop-codon readthrough (ataluren / aminoglycosides, investigative/off-label)** — the stop-gained
   allele (p.Leu737Ter) is a *theoretically* addressable premature termination codon (PTC): agents that
   promote ribosomal readthrough of a PTC could restore full-length BUBR1 from the mutant allele,
   complementing the missense allele in trans. It is ranked last because the mechanism is
   **controversial and unproven** for BUBR1 (see evidence table in section 11): PTC124/ataluren has shown
   no demonstrable readthrough in several independent reporter assays, and **no readthrough drug is FDA
   approved**. It is a hypothesis-for-follow-up, not a recommendation.

**Explicitly contraindicated — two distinct guardrails (do not conflate):**

- **(A) Critical (active disease):** spindle-poisons already used in the rhabdomyosarcoma backbone
  (**vincristine**, part of VAC) collapse the SAC in *dividing* tumor and host cells. Because the
  child's tumor is already SAC-defective, we deliberately avoid drawing a causal link between
  vincristine exposure and aneuploidy burden; rather, the haploinsufficient SAC is the *rationale*
  for close aneuploidy/PCR monitoring during treatment with standard vincristine-based regimens
  (VAC, VAC/VTC, or VAC/VA — the established pediatric backbones; Chen et al. PMC8586416;
  Arndt 19770373; Walterhouse ARST0331).
- **(B) Experimental (not clinical drugs):** direct anti-SAC pharmacological inhibitors
  (MPS1/TTK inhibitors such as reversine, BAY-1161909) are **contraindicated** as interventions
  because they collapse an already-defective checkpoint and would worsen aneuploidy severity — a
  negative/guardrail result and itself a clinically useful deliverable.

The distinction matters: vincristine is an *unavoidable component of standard-of-care oncology
therapy* whose SAC interaction is secondary, while TTK/MPS1 inhibitors would be *deliberate* SAC
sabotage with no therapeutic justification in this child.

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
management; a fourth, exploratory option (**stop-codon readthrough** targeting the Leu737Ter PTC) is
ranked last because the mechanism is unproven. We explicitly flag TTK/MPS1 SAC inhibitors as
**contraindicated** because they further destabilize an already-defective checkpoint, while distinguishing
these from vincristine, an unavoidable component of the standard rhabdomyosarcoma backbone.

**Strengths:** mechanism-first (not label-first); candidates track the actual protein affected; includes a
clinically actionable negative (contraindication list); integrates oncology surveillance, growth
management, and reproductive recurrence counseling into one care plan; fully public data.

**Limitations:**

- **Not approved / experimental:** NMN/NAD+ and senolytics are **not approved for this indication** and are
  hypothesis-for-follow-up, not evidence of efficacy.
- **Partial molecular rescue:** BUBR1-level restoration is only partially characterized (SIRT2 deacetylation
  did not fully rescue BUBR1 in vivo).
- **Active malignancy constrains mitotic-altering agents:** the patient's active rhabdomyosarcoma limits any
  agent that perturbs mitosis, proliferation, or the SAC.

**Oncological-safety caveats (specific to a pediatric cancer patient):**

- **NAD+/SIRT2 axis:** raising NAD+ is a *double-edged sword* in an active-malignancy context. NAMPT (the
  rate-limiting NAD+-synthesis enzyme, whose direct product is NMN) is overexpressed in many cancers, and
  preclinical models show NAD+ precursors can accelerate growth of pre-existing tumors (e.g. NMN accelerating
  breast-tumor xenograft growth; Nacarelli et al., Nat Cell Biol 2019). A 2026 Case Western Reserve study in
  *Cancer Letters* reports common vitamin-B3-derived NAD+ supplements may help pancreatic cancer cells
  survive and resist treatment (ecancer 27985). Because the SAC is already defective and the child has active
  rhabdomyosarcoma, any NAD+ precursor must be treated as an **experimental, oncology-supervised** intervention
  with explicit tumor-surveillance — never a casual supplement.
- **Growth hormone (GH):** the GH/IGF-I axis has well-documented pro-proliferative, angiogenic and
  anti-apoptotic properties and is implicated in tumor progression (Boguszewski & Boguszewski, *Endocrine
  Reviews* 40(2):558-574). The GRS/ESE consensus (2022, PMC9066587) deems GH safe in low-risk children but
  requires individualized decision-making and surveillance in patients with cancer-predisposing conditions or
  prior malignancy. With an active sarcoma plus a constitutional CIN-predisposition (BUB1B), GH for growth
  failure should be initiated only with pediatric-oncology sign-off and IGF-1 monitoring — flagged here as a
  risk, not a blanket prohibition.

**Parental segregation:** remains pending (in-trans compound-heterozygosity not yet formally closed).

### Evidence table (by candidate)

| Candidate | Mechanism | In-vivo / clinical support | Key caveat | Level of evidence |
|---|---|---|---|---|
| **NMN / NAD+** | SIRT2 deacetylation raises BUBR1 (K668) | Restores BUBR1 in hypomorphic mice; extends lifespan, reduces aneuploidy/cancer | Not approved; NAD+ may fuel pre-existing tumors (Nacarelli 2019; ecancer 27985) | Preclinical (mouse) |
| **Senolytics (dasatinib + quercetin)** | Clear BUBR1-insufficiency-driven senescence | Attenuates muscle/fat/lens degeneration in progeroid models | Sensitive cancer context — oncology-only | Preclinical |
| **Growth hormone** | Standard growth-failure management (Orphanet #1052) | Approved; standard-of-care | GH/IGF-I oncogenic signaling risk; individualized/surveillance in predisposed (PMC9066587) | Clinical (approved, off-label use) |
| **Stop-codon readthrough (ataluren / aminoglycosides)** | Ribosomal PTC readthrough restores full-length BUBR1 | EU-conditional approval of ataluren in nmDMD; CF trials show partial effect (Sermet-Gaudelus 21233271) | No FDA-approved drug; PTC124 lacks readthrough in multiple reporter assays (McElroy, PMC3692445); context-dependent | Investigational / controversial |

*Pro side:* a PTC-readthrough drug is the *only* candidate that directly repairs the mutant Leu737Ter allele
in trans, and ataluren has conditional EU approval for nonsense-mutation DMD. *Con side:* independent assays
(McElroy 2013) found no PTC124 readthrough in several systems, efficacy is mutation/context-dependent, and
conflicting CF phase-3 results limit confidence. This is why readthrough is ranked 4th (hypothesis-for-follow-up).

### Methodological transparency note

Every claim above was checked against the peer-reviewed primary literature cited (PubMed IDs / PMCID / DOIs
listed throughout); where a mechanism is controversial (readthrough) or a clinical risk exists (GH, NAD+ in
cancer), both the supporting and the cautionary evidence are shown rather than a one-sided selection. Candidate
scores/ranking are our own synthesis of in-vivo/ex-vivo mechanistic support and clinical availability, not a
validated quantitative algorithm.

**Scalability:** the mechanism-first repurposing framework (map LoF haploinsufficient gene → identify
dosage/level-restoring axis → safety-gate the pathway) generalizes to other haploinsufficiency and
chromosomal-instability disorders.
