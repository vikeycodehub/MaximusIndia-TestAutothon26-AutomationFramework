# TestAutothon Automation Framework

Ready-to-run **Python + Playwright** framework for the Testautothon Web & Android
Automation challenge. Built tonight so tomorrow you only plug in the real
application under test (AUT) and start writing scenario-specific tests.

## Architecture

```
TestAutothon/
├── conftest.py                  # global fixtures/hooks: env, tracing, screenshots, Allure
├── pytest.ini                   # markers, reporting config
├── requirements.txt
├── .env.example                 # copy to .env, tweak per environment
├── framework/
│   ├── config/
│   │   ├── settings.py          # loads env vars + environments.json -> Settings object
│   │   └── environments.json    # dev/qa/stage base_url + api_base_url
│   ├── core/
│   │   ├── base_page.py         # shared Playwright actions for all Page Objects
│   │   ├── api_client.py        # requests wrapper for API-level checks/setup
│   │   ├── android_driver.py    # adb-based Playwright Android support (mobile Chrome/WebView)
│   │   ├── appium_driver.py     # Appium/UiAutomator2 driver factory (native Android apps)
│   │   ├── base_mobile_page.py  # shared Appium actions for native Android Page Objects
│   │   ├── logger.py            # console + file logging
│   │   └── utils.py             # JSON data loader, retry decorator
│   ├── pages/                   # Page Objects (one class per screen/component)
│   ├── tests/
│   │   ├── web/                 # smoke, regression, data-driven, API examples
│   │   └── mobile/              # mobile-web emulation + Android device example
│   ├── data/                    # JSON test data for data-driven tests
│   ├── bug_quest_templates/     # test strategy, defect report, traceability matrix
│   └── reports/                 # screenshots, videos, traces, logs (generated)
├── scripts/                     # one-liners: setup, run_smoke, run_web, run_mobile, allure
└── .github/workflows/ci.yml     # CI: install, run smoke, upload reports
```

## Quick Start (tonight)

```powershell
cd e:\github_topic\test1\TestAutothon
.\scripts\setup.ps1          # creates venv, installs deps + browsers
copy .env.example .env       # adjust TEST_ENV/BASE_URL if needed
.\scripts\run_smoke.ps1      # proves the whole pipeline works end-to-end
```

Reports land in `reports/html-report/report.html` and `reports/allure-results`
(run `.\scripts\open_allure_report.ps1` if Allure CLI is installed).

## Tomorrow: adapting to the real AUT

1. **Config:** update `framework/config/environments.json` (or `.env`) with the
   real `base_url` / `api_base_url`. No other code changes required.
2. **Page Objects:** add a class per screen under `framework/pages/`, inheriting
   `BasePage`. Keep selectors as class constants; expose intent-based methods
   (`login()`, `add_to_cart()`) — never leak raw selectors into tests.
3. **Tests:** add files under `framework/tests/web/` or `framework/tests/mobile/`.
   Tag every test with `@pytest.mark.smoke/regression/critical` so you can run
   subsets fast under time pressure.
4. **Data-driven cases:** drop JSON into `framework/data/`, load with
   `load_json_data()`, `@pytest.mark.parametrize` over it.
5. **API checks:** use `ApiClient` for backend validation / fast test-data setup
   instead of always going through the UI.
6. **Android:** three tracks are ready — pick based on tomorrow's app type:
   - **Mobile web / responsive site:** `test_mobile_web_example.py` (Playwright device emulation, no device needed).
   - **Hybrid app / WebView / mobile Chrome on a real device or emulator:** `test_android_native_example.py`
     + `android_driver.py` (Playwright over adb).
   - **Fully native Android app:** `test_appium_native_example.py` + `appium_driver.py` +
     `base_mobile_page.py` (Appium/UiAutomator2). Requires:
     1. `npm install -g appium && appium driver install uiautomator2`
     2. Start server: `.\scripts\start_appium_server.ps1`
     3. Android emulator running or real device connected (`adb devices`)
     4. Once the real APK is provided: set `ANDROID_APP_PATH`, `ANDROID_APP_PACKAGE`,
        `ANDROID_APP_ACTIVITY` in `.env`, then write Page Objects under `framework/pages/`
        following `android_settings_home_page.py` as the pattern.
     Run: `.\scripts\run_appium.ps1`

## Execution strategy for the 5-hour event

| Time | Focus |
|---|---|
| 0:00–0:30 | Explore AUT, identify critical user journeys, update config/page objects |
| 0:30–3:00 | Automate: critical smoke flows first, then regression + data-driven, tag everything |
| 3:00–5:00 | Bug Quest in parallel: exploratory testing, log defects (`bug_quest_templates/`), keep traceability matrix updated |

Run `.\scripts\run_smoke.ps1` frequently to catch regressions early; use
`-m critical` before each milestone/demo checkpoint.

## Useful commands

```powershell
pytest -m smoke                          # fast sanity
pytest -m "smoke or critical"            # pre-demo gate
pytest framework/tests/web -n auto       # parallel run
pytest --env=qa                          # override environment for one run
pytest -k "login"                        # run tests matching a keyword
```

## Bug Quest deliverables

Use the templates in `framework/bug_quest_templates/`:
- `test_strategy_template.md` — fill in scope, risk matrix, approach
- `defect_report_template.md` — one copy per bug found
- `traceability_matrix_template.csv` — requirement → test case → defect mapping
