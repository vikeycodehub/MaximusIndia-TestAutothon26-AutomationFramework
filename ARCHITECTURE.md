# Framework Architecture - Explained Simply

Use this page to explain the framework to your team in plain words - no diagrams needed.

## 1. What this framework is

It's a ready-made structure that lets us test **any web app or Android app** without
rebuilding automation from scratch. Tomorrow we just plug in the real app's details.
Everything else - reporting, logging, retries, tagging - already works.

## 2. The 6 layers, explained like a building

Think of the framework as a building with floors. Each floor depends on the floor below it.

**Floor 1 - Config (the settings)**
This is where we store the app's URL, environment name (dev/qa/stage), timeouts,
and Android app details. If tomorrow's app changes, we only edit one file here -
nobody touches the actual test code.

**Floor 2 - Core (the toolbox)**
Shared reusable code everybody uses: how to click/type/wait on web, how to
tap/type on Android, how to call APIs, how to log messages, how to retry a
flaky step. Nobody writes this twice - they just use it.

**Floor 3 - Page Objects (one file per screen)**
For every screen in the app (Login screen, Home screen, Checkout screen), we
create one file that knows where the buttons/fields are and what actions you
can do on that screen. Example: `login_page.py` knows the username field,
password field, and has a method `login(username, password)`.

**Floor 4 - Tests (the actual test cases)**
This is where we write "what should happen." Example: "when I login with
correct details, I should see the dashboard." Tests use Page Objects - they
never touch raw button locators directly. This keeps tests short and easy to
read even for non-technical reviewers.

**Floor 5 - Test Data**
Instead of hardcoding usernames/search terms inside the test, we keep them in
a simple JSON file. This lets one test run with 5 different inputs without
copy-pasting the test 5 times.

**Floor 6 - Reporting**
Every time a test fails, the framework automatically takes a screenshot,
saves a video/trace, and records logs - so we don't need to manually
reproduce the bug to write a report. A clean HTML report and a detailed
Allure report are generated after every run.

## 3. Three ways we can test tomorrow's app

We don't know yet if tomorrow's challenge app is a website, a mobile website,
or a full native Android app - so we prepared all three, ready to use:

- **If it's a normal website:** we use Playwright (already working).
- **If it's a mobile website or a hybrid app opened inside Chrome/WebView on
  Android:** we use Playwright connected to the Android device.
- **If it's a fully native Android app** (built with native Android buttons/screens,
  not a website inside the app): we use Appium, a different tool made specifically
  for native app automation.

In the first 15-20 minutes tomorrow, we look at the app, decide which of these
three it is, and only work on that track - the other two stay unused but ready.

## 4. What happens when someone runs a test (step by step)

1. We type one command to run the tests.
2. The framework reads the config (which app, which environment).
3. It opens the browser or connects to the Android device/app.
4. The test calls the Page Object (e.g. "login page, please log in").
5. The Page Object performs the actual clicks/typing.
6. If everything works, the test passes. If something breaks, a screenshot,
   video, and log are saved automatically.
7. At the end, a report is generated showing what passed, what failed, and why.

## 5. Simple rules for the team to follow

- **Never hardcode data in a test** - put it in the JSON data file instead.
- **Never write clicks/selectors directly in a test** - put them in a Page Object.
- **Always tag your test** as smoke / regression / critical, so we can run just
  the important ones quickly when time is short.
- **If config changes (new app URL, new environment), edit the config file only**
  - never touch test files for that.
- **Trust the reports** - don't manually re-run a failed test to "see what
  happened," the screenshot/video is already saved for you.

## 6. Why this matters for the competition

- We save time tomorrow because the "plumbing" (setup, reporting, structure)
  is already done - the team only writes app-specific logic.
- Judges can see a clean, organized framework, not a pile of scripts.
- Anyone on the team, technical or not, can look at a test file and understand
  what it's checking, because it reads like plain English.
