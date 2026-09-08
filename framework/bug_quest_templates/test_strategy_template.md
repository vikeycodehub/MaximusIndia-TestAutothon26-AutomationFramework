# Test Strategy - <App/Module Name>

## 1. Scope
- **In scope:** (features/flows to be tested)
- **Out of scope:** (explicitly excluded, with reason)
- **Platforms:** Web / Android (mobile web / native / hybrid - specify)

## 2. Objectives
- Validate critical user journeys work end-to-end
- Surface high-impact defects within the time-box
- Provide automation coverage for regression-prone areas

## 3. Risk-Based Prioritization
| Feature/Flow | Business Impact (H/M/L) | Likelihood of Defect (H/M/L) | Priority | Notes |
|---|---|---|---|---|
| Login/Auth | H | M | P1 | |
| Checkout/Payment | H | H | P1 | |
| Search | M | M | P2 | |
| Profile settings | L | L | P3 | |

## 4. Test Approach
- **Functional:** manual exploratory + automated smoke/regression
- **API:** contract & data validation where UI depends on backend
- **Cross-browser/device:** Chromium primary, note gaps for Firefox/WebKit/Android
- **Negative/Edge cases:** invalid inputs, boundary values, network failures, empty states
- **Non-functional (time-permitting):** basic performance/console-error checks, accessibility spot-checks

## 5. Test Environment
- Environment/URL:
- Test accounts/data:
- Browsers/devices covered:

## 6. Entry / Exit Criteria
- **Entry:** build deployed & accessible, test accounts provisioned
- **Exit:** all P1 flows executed, defects logged with severity, automation smoke suite green

## 7. Tools
- Automation: Python + Playwright (pytest, Allure)
- Bug tracking: (tool used at event)
- API testing: `requests` via framework ApiClient

## 8. Team & Time Allocation
| Member | Responsibility | Time-box |
|---|---|---|
| | Automation - critical flows | |
| | Exploratory testing / bug hunting | |
| | Reporting & traceability | |

## 9. Deliverables
- Automated test suite (this repo)
- Defect reports (see `defect_report_template.md`)
- Traceability matrix (see `traceability_matrix_template.csv`)
- Summary of coverage, risks, and known gaps
