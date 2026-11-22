# The domain taxonomy

The client's Sulfur domains are the same seven groups and 21 domains as Mark's; the Sulfur lines for each (task
types, what makes it deep, domain fit) are at the end of this file and are read first. The task-type keys below are
the ones `fingerprint/vocab.json` enforces; where Sulfur's task-type list differs (Quantitative Finance's eleven
finer types, Physical & Environmental Sciences' eleven, Energy's dispatch and adequacy types, Human Factors' four),
the card takes the nearest vocab key and names the Sulfur task type in its `niche`.

Seven groups, twenty-one client domains, each with its task types; every task type serves one or two of the eight
Axis 1 objectives. A build picks one domain and one task type (the card's `domain` and `subdomain`) and one objective
that task type serves. `fingerprint/vocab.json` (`client_domains`) is the copy the guard enforces.

Objectives: F Forecasting & Predictive Modeling, RC Root-Cause Analysis, AD Anomaly Detection & Diagnostics, EC
Experiment & Causal Analysis, DD Descriptive & Distribution Analysis, ETL Data Extraction & Conformation, OS
Opportunity Sizing & Decision Support, DQ Data Quality Monitoring & Alerting.

Layer 2 patterns per task type: `../../../stumping/references/client/layer2-rigor-patterns.md`. Layer 1 mess per
domain: `../../../dataset-generation/references/layer1-messiness.md`. Three domains (Physical & Environmental Sciences;
Energy Systems & Utilities; Human Factors & Ergonomics) have Layer 1 techniques but no Layer 2 patterns: take the
pitfall from the five Layer 2 families in `../../../stumping/references/client/two-layer-task-design.md`. Quantitative
Finance, Banking and Actuarial Science carry their patterns under the client's finer stumping-page task types, each
mapped in the library to the taxonomy task type the card's `subdomain` takes.

**Close calls.** Biomedical & Clinical Research is study data on treatments and trials; Epidemiology & Public Health
is populations, exposures and surveillance; Pharmacology is drug exposure and safety; Healthcare Delivery & Health
Economics is the system's operations, costs and claims. Economics is macro, labour, trade and fiscal reads, never
corporate finance, markets trading or lending. A platform selling into a sector is Product Analytics with that
sector's data as its market.

**House domains.** The nine domains of the earlier spec stay valid on filed cards; a new draw in one names the client
domain it sits in (the guard warns otherwise). `product-analytics` and `marketing-consumer-research` map to
themselves; `economics` to `economics-econometrics`; `policy-education` to `political-science-public-policy`,
`education-learning-sciences`; `demographic-social-science` to `sociology-demography`,
`survey-research-official-statistics`; `nonprofit-grant-making` to `political-science-public-policy`,
`general-statistics-data-science`; `supply-chain-logistics` to `urban-regional-science`,
`general-statistics-data-science`; `business-operations-analytics` to `general-statistics-data-science`,
`human-factors-ergonomics`, `healthcare-delivery-health-economics`; `accounting-audit-forensic` to
`banking-credit-financial-risk`, `actuarial-science-insurance`, `general-statistics-data-science`.

## Product analytics

### Product Analytics (`product-analytics`)

- `online-experimentation-a-b-test-design-readout`: EC
- `observational-causal-inference`: EC
- `metric-definition-measurement-science`: DD, DQ
- `retention-cohort-lifetime-value-modeling`: F
- `churn-propensity-uplift-modeling`: F, OS
- `funnel-journey-analysis`: DD, RC
- `network-effect-marketplace-experimentation`: EC
- `feature-adoption-diffusion-modeling`: F, DD

### Marketing & Consumer Research (`marketing-consumer-research`)

- `segmentation-market-structure`: DD
- `conjoint-choice-willingness-to-pay-analysis`: OS, F
- `brand-campaign-ad-effectiveness-measurement`: EC
- `customer-satisfaction-driver-analysis`: RC
- `media-reach-frequency-audience-measurement`: DD, F

## Quantitative finance and trading

### Quantitative Finance (`quantitative-finance`)

- `portfolio-construction-risk`: OS
- `factor-return-attribution`: RC
- `strategy-backtesting-evaluation`: F
- `market-microstructure-execution-cost`: DD
- `volatility-derivatives-pricing`: F
- `event-study`: EC

### Banking, Credit & Financial Risk (`banking-credit-financial-risk`)

- `credit-scoring-pd-modeling`: F
- `expected-credit-loss-provisioning`: F, OS
- `stress-testing-capital`: F
- `fraud-aml-detection`: AD
- `deposit-liquidity-behaviour`: F
- `collections-recovery`: OS

### Actuarial Science & Insurance (`actuarial-science-insurance`)

- `reserving-development-triangles`: F
- `pricing-ratemaking-credibility`: OS, F
- `mortality-longevity`: F
- `catastrophe-exposure-accumulation`: OS
- `claims-frequency-severity`: DD, F
- `reinsurance-capital`: OS

## Machine learning research

### General Statistics & Data Science (`general-statistics-data-science`)

- `exploratory-data-analysis-distribution-assessment`: DD, AD
- `regression-classification-model-diagnostics`: F
- `resampling-simulation-monte-carlo-methods`: F, DD
- `bayesian-modeling-posterior-inference`: F
- `missing-data-censoring-measurement-error`: DD, DQ
- `multiple-testing-selective-inference`: AD, EC
- `data-integration-record-linkage-entity-resolution`: ETL
- `benchmarking-and-ablations`: EC
- `scaling-laws`: F
- `robustness-analysis`: DD
- `interpretability`: RC

## Biomedical and health sciences

### Biomedical & Clinical Research (`biomedical-clinical-research`)

- `clinical-trial-design-analysis`: EC
- `survival-time-to-event-analysis`: F, DD
- `diagnostic-biomarker-accuracy`: DD
- `dose-response-pk-pd-modeling`: F
- `genomics-gwas-high-dimensional-association`: AD, DD
- `statistical-genomics`: DD
- `longitudinal-outcomes-repeated-measures`: EC
- `adaptive-platform-basket-trial-methods`: EC
- `real-world-evidence-comparative-effectiveness`: EC
- `medical-imaging-reader-study-evaluation`: DD

### Epidemiology & Public Health (`epidemiology-public-health`)

- `observational-study-design-cohort-case-control`: EC
- `disease-surveillance-outbreak-anomaly-detection`: AD, DQ
- `risk-factor-causal-effect-estimation`: EC
- `screening-diagnostic-policy-evaluation`: OS
- `health-burden-impact-modeling`: OS, F
- `infectious-disease-transmission-modeling`: F
- `cluster-stepped-wedge-community-trials`: EC
- `health-equity-disparity-decomposition`: RC

### Pharmacology, Pharmacoepidemiology & Safety (`pharmacology-pharmacoepidemiology-safety`)

- `population-pharmacokinetics-exposure-response`: F
- `drug-utilization-comparative-safety`: EC
- `safety-signal-detection`: AD
- `benefit-risk-assessment`: OS
- `medication-adherence-persistence`: DD

### Healthcare Delivery & Health Economics (`healthcare-delivery-health-economics`)

- `cost-effectiveness-decision-modeling`: OS
- `utilization-access-demand-forecasting`: F
- `provider-quality-risk-adjustment`: DD, AD
- `patient-flow-beds-workforce-optimization`: OS, F
- `payment-claims-health-plan-analytics`: ETL, AD

## Economics and quantitative social science

### Economics & Econometrics (`economics-econometrics`)

- `causal-identification-did-iv-rd-synthetic-control`: EC
- `structural-equilibrium-modeling`: OS
- `time-series-macro-econometrics`: F
- `panel-data-estimation`: EC, RC
- `elasticity-welfare-policy-impact-estimation`: OS
- `forecasting-forecast-evaluation`: F
- `discrete-choice-limited-dependent-variable-modeling`: F
- `spatial-econometrics-spillover-estimation`: EC

### Political Science & Public Policy (`political-science-public-policy`)

- `election-polling-forecasting`: F
- `policy-evaluation-administrative-data-inference`: EC
- `legislative-behavior-ideal-point-estimation`: DD
- `conflict-protest-event-data-analysis`: AD, DD
- `public-opinion-survey-experimentation`: EC
- `small-area-public-opinion-estimation-mrp`: DD

### Sociology & Demography (`sociology-demography`)

- `population-estimation-demographic-projection`: F
- `social-mobility-inequality-measurement`: DD
- `social-network-peer-effect-analysis`: EC
- `event-history-life-course-analysis`: DD, F
- `neighborhood-segregation-contextual-effects`: DD
- `fertility-mortality-life-table-estimation`: F, DD

### Psychology & Behavioral Science (`psychology-behavioral-science`)

- `experimental-design-power-analysis`: EC
- `psychometric-measurement-scale-validation`: DD, DQ
- `statistical-inference-hypothesis-testing`: EC
- `mediation-moderation-process-modeling`: RC
- `meta-analysis-evidence-synthesis`: EC
- `longitudinal-growth-curve-modeling`: DD
- `decision-making-computational-behavioral-modeling`: F
- `experience-sampling-intensive-longitudinal-analysis`: DD

### Criminology & Justice (`criminology-justice`)

- `crime-incidence-hotspot-analysis`: AD
- `recidivism-risk-assessment`: F
- `sentencing-bail-disparity-analysis`: RC
- `intervention-policing-policy-evaluation`: EC

## Engineering and physical sciences

### Physical & Environmental Sciences (`physical-environmental-sciences`)

- `environmental-monitoring-exceedance`: AD, DQ
- `climate-weather-extremes`: F
- `pollution-source-attribution`: RC
- `sensor-calibration-measurement`: DQ
- `hydrology-flood-frequency`: F
- `emissions-inventory`: ETL, DD

### Energy Systems & Utilities (`energy-systems-utilities`)

- `load-forecasting`: F
- `generation-capacity-planning`: OS
- `grid-reliability-outage-analysis`: RC, AD, ETL (fault and interruption records from relays, SCADA, the outage system and field records conformed to one schema; the platform assigns analysis types apart from task types)
- `tariff-demand-response-evaluation`: EC
- `asset-condition-maintenance`: F, OS
- `efficiency-savings-verification`: EC

### Human Factors & Ergonomics (`human-factors-ergonomics`)

- `usability-task-performance-studies`: EC
- `workload-fatigue-shift-analysis`: RC
- `safety-incident-error-analysis`: RC, AD
- `human-reliability-assessment`: F
- `anthropometric-design-fit`: DD
- `alarm-interface-evaluation`: EC

## Other

### Survey Research & Official Statistics (`survey-research-official-statistics`)

- `sample-design-allocation-weighting`: DD, OS
- `nonresponse-calibration-measurement-error-adjustment`: DD, DQ
- `questionnaire-mode-effects-research`: EC
- `small-area-estimation`: DD
- `census-register-administrative-data-quality`: DQ, ETL
- `seasonal-adjustment-official-time-series-production`: F, ETL
- `complex-survey-estimation-variance`: DD
- `anomaly-detection`: AD

### Urban & Regional Science (`urban-regional-science`)

- `land-use-spatial-development-modeling`: F
- `accessibility-agglomeration-location-analysis`: OS
- `municipal-service-demand-resource-allocation`: OS, F
- `regional-input-output-economic-impact`: OS
- `optimization`: OS
- `forecasting`: F
- `network-analysis`: DD

### Education & Learning Sciences (`education-learning-sciences`)

- `student-growth-value-added-modeling`: DD, EC
- `randomized-quasi-experimental-program-evaluation`: EC
- `item-response-theory-test-equating`: ETL, DD
- `learning-analytics-early-warning-models`: F
- `multilevel-classroom-school-research`: RC
- `psychometrics`: DD
- `text-analysis`: DD

## Sulfur: what makes each subdomain deep, and what domain fit means there

The client's own two lines per subdomain (`guidelines/client/domains.txt`), with its task types. The deep step is drawn from the first line and must satisfy the second. Group names are the client's seven major domains.

### Product Analytics (Product Analytics)

- **Task types:** A/B testing (experiment design, power analysis, variance reduction, readout); Metric design (defining, validating, and instrumenting product KPIs); Cohort and LTV modeling (retention curves, customer lifetime value); Uplift modeling (estimating heterogeneous treatment effects for targeting); Observational causal inference; Churn, propensity & uplift modeling; Funnel & journey analysis; Network-effect & marketplace experimentation; Feature adoption & diffusion modeling.
- **What makes it deep:** Experiment and cohort reads where the simple comparison misleads, such as a lift that fades once novelty wears off, users who interfere with each other across arms, a mix shift across platforms that hides opposite responses, or immature cohorts whose retention has to be projected before options can be compared.
- **Domain fit:** The deciding step is a product measurement judgment (an experiment readout, a retention or LTV projection, a funnel attribution), not a generic ranking that happens to use event logs.

### Marketing & Consumer Research (Product Analytics)

- **Task types:** Segmentation & market structure; Conjoint, choice & willingness-to-pay analysis; Brand, campaign & ad-effectiveness measurement; Customer satisfaction & driver analysis; Media reach, frequency & audience measurement.
- **What makes it deep:** Separating incremental effect from customers who would have bought anyway, handling selection into exposure or a contaminated holdout, and estimating segment-level response or willingness to pay when segments react differently to price or message.
- **Domain fit:** The decision turns on a marketing measurement question such as incrementality, segment response or choice behavior, not on summing spend by campaign name.

### Quantitative Finance (Quantitative Finance and Trading)

- **Task types:** Alpha research (finding and validating return-predictive signals); Backtesting (historical strategy simulation, transaction costs, attribution); Derivative pricing (stochastic models, numerical pricing, calibration); Risk modeling (VaR/ES, stress testing, credit and counterparty risk); Portfolio construction & optimization; Fixed-income & term-structure analysis; Credit / default-risk modeling; Liquidity, funding & balance-sheet risk; Scenario analysis & enterprise stress testing; Market data, curve & surface validation; Counterparty exposure & valuation adjustment.
- **What makes it deep:** Validating a signal or strategy out of sample, recognizing that returns explained by known factor exposures are not alpha, correcting inference for overlapping returns and many tried signals, and sizing realistic costs and capacity before committing capital.
- **Domain fit:** The deciding step is a return, risk or pricing judgment a quant would make, not arithmetic on a price table.

### Banking, Credit & Financial Risk (Quantitative Finance and Trading)

- **Task types:** Credit scoring & underwriting; Expected credit loss & allowance modeling; Fraud, AML & transaction monitoring; Deposit, prepayment & interest-rate behavior; Collections & loss-mitigation strategy.
- **What makes it deep:** Inferring performance for applicants who were never approved, projecting immature loan vintages before comparing them, separating macro conditions from underwriting changes, and finding an uncontaminated comparison when a collections or pricing change rolled out in waves.
- **Domain fit:** The answer depends on credit or financial risk reasoning (default, loss, cure or prepayment behavior), not on a lending policy applied row by row.

### Actuarial Science & Insurance (Quantitative Finance and Trading)

- **Task types:** Frequency-severity & aggregate loss modeling; Pricing, rating & credibility; Loss reserving & claims development; Catastrophe & accumulation risk; Survival, lapse & policyholder behavior; Solvency, capital & reinsurance optimization; Mortality & longevity modeling.
- **What makes it deep:** Projecting immature accident years to ultimate, noticing when a change in claim settlement speed breaks the development pattern, blending own experience with class experience through credibility, and choosing trend and tail factors the data can defend.
- **Domain fit:** The deciding step is an actuarial judgment about loss development, pricing or reserving, not a rate table looked up and multiplied.

### General Statistics & Data Science (Machine Learning Research)

- **Task types:** Benchmarking and ablations (controlled evaluation, isolating component effects); Scaling laws (performance trends across model, data, and compute size); Robustness analysis (distribution shift, out-of-distribution generalization, calibration); Interpretability (feature attribution, probing, mechanistic analysis); Exploratory data analysis & distribution assessment; Regression, classification & model diagnostics; Resampling, simulation & Monte Carlo methods; Bayesian modeling & posterior inference; Missing data, censoring & measurement error; Multiple testing & selective inference; Data integration, record linkage & entity resolution.
- **What makes it deep:** Choosing and justifying a model out of sample rather than by in-sample fit, handling missingness that is not random, accounting for measurement error, controlling for many comparisons, and matching uncertainty to clustered or repeated observations. Shrinkage for sparse groups and checks that a procedure really has the coverage it claims belong here too.
- **Domain fit:** Here the field is the statistical method itself, so the deciding step must be a statistical judgment a careful statistician would defend, not subject-matter arithmetic with a statistics label on it.

### Biomedical & Clinical Research (Biomedical and Health Sciences)

- **Task types:** Clinical trial design (randomization, sample size, adaptive and cluster designs); Survival analysis (Kaplan-Meier, Cox models, competing risks); PK/PD modeling (drug exposure and dose-response relationships); Statistical genomics (GWAS, differential expression, polygenic risk); Diagnostic & biomarker accuracy; Longitudinal outcomes & repeated measures; Adaptive, platform & basket trial methods; Real-world evidence & comparative effectiveness; Medical imaging & reader-study evaluation.
- **What makes it deep:** Time-to-event analysis with censoring and competing risks, hazards that are not proportional over follow-up, dropout that differs by arm, and uncertainty that matches a cluster or stratified randomization. Heterogeneity across prespecified subgroups also counts, as long as it is real and not one of many fishing comparisons.
- **Domain fit:** The deciding step needs clinical trial or biostatistical reasoning about an endpoint, not just patient vocabulary on a generic comparison.

### Epidemiology & Public Health (Biomedical and Health Sciences)

- **Task types:** Observational study design (cohort / case-control); Disease surveillance & outbreak / anomaly detection; Risk-factor & causal effect estimation; Screening & diagnostic-policy evaluation; Health-burden & impact modeling; Infectious-disease transmission modeling; Cluster, stepped-wedge & community trials; Health equity & disparity decomposition.
- **What makes it deep:** Standardizing rates when the population's age structure shifts, correcting for reporting delays before reading a recent trend, smoothing unstable small-area rates, and separating an intervention's effect from a secular trend or a concurrent program.
- **Domain fit:** The decision rests on an epidemiological quantity (a rate, risk, attributable burden or outbreak signal) estimated with the field's methods, not on a list of clinics checked against criteria.

### Pharmacology, Pharmacoepidemiology & Safety (Biomedical and Health Sciences)

- **Task types:** Population pharmacokinetics & exposure response; Drug utilization & comparative safety; Safety-signal detection; Benefit-risk assessment; Medication adherence & persistence.
- **What makes it deep:** Confounding by indication, immortal time from how exposure is defined, choosing a new-user or active-comparator design, defining exposure windows that fit the drug's action, and reading a safety signal against how reporting itself changes.
- **Domain fit:** The deciding step reasons about drug exposure, dose or adverse outcomes the way a pharmacoepidemiologist or pharmacologist would, not just about counts with drug names attached.

### Healthcare Delivery & Health Economics (Biomedical and Health Sciences)

- **Task types:** Cost-effectiveness & decision modeling; Utilization, access & demand forecasting; Provider quality & risk adjustment; Patient flow, beds & workforce optimization; Payment, claims & health-plan analytics.
- **What makes it deep:** Adjusting for case mix, recognizing regression to the mean when sites were picked after a bad stretch, weighting results to the population the decision serves, and carrying cost and outcome uncertainty through a cost-effectiveness or capacity decision.
- **Domain fit:** The answer depends on health services or health economic reasoning (outcomes per resource, case-mix-adjusted performance, value for money), not on a reimbursement rule applied to claims.

### Economics & Econometrics (Economics and Quantitative Social Science)

- **Task types:** Causal identification (DiD, IV, RD, synthetic control); Panel-data modeling (fixed and random effects, multilevel models); Discrete-choice modeling (logit/probit, random utility models); Time-series econometrics (VAR, cointegration, macro forecasting); Structural / equilibrium modeling; Elasticity & welfare / policy-impact estimation; Forecasting & forecast evaluation; Spatial econometrics & spillover estimation.
- **What makes it deep:** Identifying a causal effect when the treatment is endogenous, checking pre-trends in a staggered rollout, letting effects build over time, and weighting heterogeneous effects to match what the decision counts. Forecasts that must hold up through revisions or structural breaks belong here too.
- **Domain fit:** The deciding step is an economic causal or forecasting judgment, not a published series copied into a table.

### Political Science & Public Policy (Economics and Quantitative Social Science)

- **Task types:** Election polling & forecasting; Policy evaluation & administrative-data inference; Legislative behavior & ideal-point estimation; Conflict, protest & event-data analysis; Public opinion & survey experimentation; Small-area public-opinion estimation & MRP.
- **What makes it deep:** Evaluating a policy when places selected themselves into adopting it, building a credible counterfactual such as a synthetic comparison, using an eligibility threshold as a discontinuity, and modeling turnout or opinion from samples that need poststratification.
- **Domain fit:** The decision rests on reasoning about policy effects or political behavior, not on checking which agencies meet a statutory list.

### Sociology & Demography (Economics and Quantitative Social Science)

- **Task types:** Population estimation & demographic projection; Social mobility & inequality measurement; Social network & peer-effect analysis; Event-history & life-course analysis; Neighborhood, segregation & contextual effects; Fertility, mortality & life-table estimation.
- **What makes it deep:** Separating age, period and cohort patterns, decomposing a change into composition and rate effects, and projecting a population while carrying migration and fertility uncertainty through to the decision.
- **Domain fit:** The deciding step uses demographic or sociological reasoning about rates, exposures and cohorts, not head counts sorted by region.

### Psychology & Behavioral Science (Economics and Quantitative Social Science)

- **Task types:** Experimental design & power analysis; Psychometric measurement & scale validation; Statistical inference & hypothesis testing; Mediation, moderation & process modeling; Meta-analysis & evidence synthesis; Longitudinal & growth-curve modeling; Decision-making & computational behavioral modeling; Experience sampling & intensive longitudinal analysis.
- **What makes it deep:** Measurement reliability and whether a scale means the same thing across groups, repeated measures nested in people, order and learning effects, attrition in longitudinal samples, and mediation claims that the design can or cannot support.
- **Domain fit:** The answer depends on psychometric or behavioral research reasoning, not on survey scores averaged and ranked.

### Criminology & Justice (Economics and Quantitative Social Science)

- **Task types:** Crime incidence & hotspot analysis; Recidivism & risk assessment; Sentencing, bail & disparity analysis; Intervention & policing-policy evaluation.
- **What makes it deep:** Displacement and diffusion around place-based interventions, the gap between reported crime and actual incidence, regression to the mean in hot spots chosen after a spike, and recidivism comparisons with different follow-up lengths that need survival methods.
- **Domain fit:** The deciding step reasons about crime, enforcement or justice outcomes the way a criminologist would, not about a sentencing grid applied to cases.

### Physical & Environmental Sciences (Engineering and Physical Sciences)

- **Task types:** Inverse problems (model calibration, data assimilation, uncertainty propagation); Design of experiments (factorial designs, response-surface optimization); Statistical process control (control charts, capability and measurement system analysis); Reliability analysis (life-data analysis, accelerated testing, failure modeling); Geostatistical & spatial-field estimation; Physical-model calibration & data assimilation; Geophysical retrieval from remote-sensing / instrument data; Extreme-value & environmental-hazard (return-period) analysis; Climate & environmental change detection & attribution; Sensor calibration & measurement uncertainty; Spatiotemporal exposure & source apportionment.
- **What makes it deep:** Spatial and temporal autocorrelation that inflates apparent significance, measurements below detection limits that must be treated as censored, separating a trend from natural variability, and estimating return periods for extremes.
- **Domain fit:** The decision rests on physical or environmental reasoning about the measured system, not on site names attached to a generic ranking.

### Energy Systems & Utilities (Engineering and Physical Sciences)

- **Task types:** Load, price & renewable forecasting; Capacity expansion & generation planning; Unit commitment, dispatch & storage optimization; Grid reliability & outage analysis; Energy efficiency & demand response evaluation; Grid resource adequacy analysis.
- **What makes it deep:** Normalizing load for weather before comparing periods, coincidence of peaks across customers or feeders, forecasts of demand or failure validated out of sample, and reliability indices read with and without major events.
- **Domain fit:** The deciding step needs reasoning about load, reliability, dispatch or rates, not a utility's ranking score applied to a list of substations.

### Human Factors & Ergonomics (Engineering and Physical Sciences)

- **Task types:** Usability & task-performance experiments; Workload, vigilance & fatigue modeling; Anthropometry & workspace design; Human reliability & error analysis.
- **What makes it deep:** Within-subject designs with learning and order effects, speed and accuracy traded against each other, small samples of repeated trials that need mixed models, and exposure-response relationships for injury or fatigue.
- **Domain fit:** The answer depends on human performance or ergonomic reasoning, not on incident counts tallied by department.

### Survey Research & Official Statistics (Other)

- **Task types:** Anomaly detection (outliers, fraud, intrusion, change points); Survey sampling (sample design, weighting, small-area estimation); Nonresponse, calibration & measurement-error adjustment; Questionnaire & mode-effects research; Small-area estimation; Census, register & administrative-data quality; Seasonal adjustment & official time-series production; Complex-survey estimation & variance.
- **What makes it deep:** Design-based variance with strata, clusters or replicate weights, nonresponse adjustment, mode changes that break a series, multiple imputation, and estimates from overlapping samples whose errors are correlated across waves.
- **Domain fit:** The deciding step is a survey methodology judgment about how the estimate and its uncertainty are produced, not a published table looked up.

### Urban & Regional Science (Other)

- **Task types:** Spatial statistics (geostatistics, kriging, hotspot and distribution mapping); Optimization (linear/integer programming, scheduling, resource allocation); Forecasting (demand, load, and capacity prediction); Network analysis (centrality, community detection, diffusion modeling); Land-use & spatial-development modeling; Accessibility, agglomeration & location analysis; Municipal service-demand & resource allocation; Regional input-output & economic impact.
- **What makes it deep:** Spillovers across neighboring areas and boundaries, results that change with the spatial unit chosen, accessibility and commuting models, and separating composition change from displacement in a neighborhood.
- **Domain fit:** The decision rests on spatial or regional reasoning about places and flows, not on city names attached to a generic comparison.

### Education & Learning Sciences (Other)

- **Task types:** Psychometrics (scale validation, item response theory, test equating); Text analysis (automated content coding, topic modeling, citation analysis); Student growth & value-added modeling; Randomized & quasi-experimental program evaluation; Learning analytics & early-warning models; Multilevel classroom & school research.
- **What makes it deep:** School or teacher effects with measurement error and real cohort-to-cohort variation beyond sampling noise, uncertainty that matches a design where whole schools were randomized, growth models, and selection into programs.
- **Domain fit:** The deciding step needs education measurement or evaluation reasoning, not an eligibility formula applied to schools.

