# Day-Of Pre-Flight Checklist

Run through this BEFORE the event clock starts, so the first 5 hours aren't
wasted debugging the framework instead of the app.

## 1. Machine setup (do this the night before, again in the morning)
- [ ] `git pull` latest changes (if working from a shared repo)
- [ ] `.\scripts\setup.ps1` runs clean (installs deps + Playwright browsers)
- [ ] `copy .env.example .env` exists and has correct defaults
- [ ] `.\scripts\run_smoke.ps1` passes (proves web + mobile-web tracks work)

## 2. If Android native app automation may be needed
- [ ] Node.js + Appium installed: `npm install -g appium`
- [ ] UiAutomator2 driver installed: `appium driver install uiautomator2`
- [ ] Android SDK platform-tools installed, `adb` on PATH
- [ ] Emulator running OR real device connected with USB debugging ON
- [ ] `adb devices` shows the device as `device` (not `unauthorized`/`offline`)
- [ ] `.\scripts\start_appium_server.ps1` starts without errors
- [ ] `.\scripts\run_appium.ps1` passes against the Settings app (sanity check)

## 3. Once tomorrow's real AUT is announced (first 15-20 minutes)
- [ ] Identify app type: website / mobile-web-hybrid / native Android
- [ ] Update `framework/config/environments.json` (or `.env`) with real base_url
- [ ] If native Android: set `ANDROID_APP_PACKAGE`, `ANDROID_APP_ACTIVITY`,
      `ANDROID_APP_PATH` in `.env`
- [ ] List the 3-5 most critical user journeys - automate these first
- [ ] Assign owners: who automates, who does exploratory/bug-hunting

## 4. Before every demo / milestone checkpoint
- [ ] Run `pytest -m critical` - must be all green
- [ ] Run `.\scripts\run_smoke.ps1` - must be all green
- [ ] Check `reports/html-report/report.html` for any unexpected failures

## 5. Bug Quest parallel track
- [ ] Test strategy doc started from `framework/bug_quest_templates/test_strategy_template.md`
- [ ] Defect reports logged as found using `defect_report_template.md`
- [ ] Traceability matrix (`traceability_matrix_template.csv`) updated as scenarios are covered

## 6. Before final submission
- [ ] Full suite run one last time, reports generated
- [ ] Commit + push all code and reports
- [ ] Test strategy + defect reports + traceability matrix finalized and attached
