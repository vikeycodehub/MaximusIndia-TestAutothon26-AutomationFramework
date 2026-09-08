# Command Cheat Sheet

## Setup (once)
```powershell
.\scripts\setup.ps1
copy .env.example .env
```

## Everyday commands
```powershell
.\scripts\run_smoke.ps1        # fast sanity check (web + mobile-web)
.\scripts\run_web.ps1          # full web + API regression, parallel
.\scripts\run_mobile.ps1       # mobile-web + Android(adb) tests
.\scripts\run_appium.ps1       # native Android app tests (needs Appium server)
.\scripts\start_appium_server.ps1   # start Appium server (separate terminal)
.\scripts\open_allure_report.ps1    # view detailed Allure report
```

## Raw pytest (when you need more control)
```powershell
pytest -m smoke                     # only smoke-tagged tests
pytest -m "smoke or critical"       # pre-demo gate
pytest -m regression                # full regression pass
pytest -k "login"                   # tests with "login" in the name
pytest --env=qa                     # override environment for one run
pytest framework/tests/web -n auto  # run web tests in parallel
pytest --headed                     # watch the browser while it runs (debugging)
pytest --tracing=on                 # force trace capture even on pass
```

## Reports (after any run)
- HTML: `reports/html-report/report.html`
- Allure raw results: `reports/allure-results` → `.\scripts\open_allure_report.ps1`
- Screenshots/videos/traces: `reports/screenshots`, `reports/videos`, `reports/traces`
- Logs: `reports/logs/run.log`

## Git (if working as a team on a shared repo)
```powershell
git add .
git commit -m "Add login page automation"
git push
```
