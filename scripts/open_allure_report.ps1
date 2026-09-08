# Generates and opens the Allure HTML report from the last run.
# Requires Allure commandline: https://github.com/allure-framework/allure2 (or `scoop install allure`)
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
