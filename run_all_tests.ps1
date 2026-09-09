#!/usr/bin/env powershell
# Run all Gajab automation tests and generate reports

Write-Host "========================================"
Write-Host "AbstractQA - Gajab Automation Test Suite"
Write-Host "========================================"
Write-Host ""

$testDir = "d:\omkar hackathon\AbstractQA"
Set-Location $testDir

Write-Host "1. Running Gajab Test Suite (All Tests)"
Write-Host "----------------------------------------"
python -m pytest framework/tests/web/gajab/ -v --html=reports/gajab-complete-report.html --self-contained-html --tb=short

Write-Host ""
Write-Host "2. Running API Tests"
Write-Host "----------------------------------------"
python -m pytest framework/tests/web/test_api_example.py -v --html=reports/api-tests-report.html --self-contained-html

Write-Host ""
Write-Host "3. Running Data-Driven Tests"
Write-Host "----------------------------------------"
python -m pytest framework/tests/web/test_data_driven_example.py -v --html=reports/data-driven-report.html --self-contained-html

Write-Host ""
Write-Host "========================================"
Write-Host "Test Execution Complete!"
Write-Host "========================================"
Write-Host ""
Write-Host "Reports generated in: reports/ directory"
Write-Host "Open HTML reports in your browser to view results"
Write-Host ""
Write-Host "Key reports:"
Write-Host "  - gajab-complete-report.html (All Gajab tests)"
Write-Host "  - api-tests-report.html (API tests)"
Write-Host "  - data-driven-report.html (Data-driven tests)"
