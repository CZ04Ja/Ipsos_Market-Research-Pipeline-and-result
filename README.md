# Market Research: Data Reconciliation and Reporting

A privacy-preserving portfolio summary of market-research workflow, accompanied by a synthetic SQL/pandas reconciliation exercise. Client workbooks, interview transcripts and internal operating figures are excluded.

## Workflow
Define each metric's unit, period, geography and population before combining sources. Keep a source register and distinguish public statistics from interviews and client-provided figures. Aggregate facts at the intended grain before joining dimension tables. Check unmatched keys, duplicate mappings, missing periods and totals before building the report.

The work reviewed includes regional desk research, channel analysis and marketing-activity planning. The public summary describes the method rather than reproducing client targets or recommendations. No historic SQL or Python program was recovered that independently establishes its use in the original delivery; the runnable code here is a later reconstruction.

## Run and checks
`python src/reproduce.py` uses four synthetic transaction rows and a two-row dealer dimension. It demonstrates aggregation before a LEFT JOIN, preservation of total units, detection of an unmatched dealer and rejection of duplicate dimension keys. SQL and pandas results are compared. These are unit checks, not a measured commercial improvement.

## Deliverables
See `reports/market_research_case_study.md` for a client-free case study and `docs/metric_dictionary.csv` for a reusable metric-definition template. Original presentation decks remain outside this package because some pages contain internal client figures, named contacts or embedded files.
