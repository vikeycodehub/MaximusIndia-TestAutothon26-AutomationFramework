# AbstractQA - Gajab Automation Test Suite - Complete Execution Guide

## Overview
Your framework has **6 test files** with **12+ test cases** covering:
- Authentication (Login with OTP)
- Location & Pincode Selection  
- Home Page Products (Deal of Day, Trending, Just Bargained)
- Product Filtering (Brand, Price Range)
- API Testing
- Data-Driven Testing

---

## Test Files Summary

### 1. **test_01_login_otp.py** - Authentication Flow
**Tests**: 1
- `test_login_with_default_otp` - Login with mobile number and default OTP (123456)

**Status**: ⚠️ **May FAIL** - Gajab website missing OTP input field (`#otp-input-0`)

**Run**: 
```bash
pytest framework/tests/web/gajab/flow_cases/test_01_login_otp.py -v
```

---

### 2. **test_02_location_and_home.py** - Location & Home Page Products
**Tests**: 2
- `test_pincode_is_reflected_in_header` - Set pincode (560037) and verify it appears in header
- `test_home_sections_return_dynamic_products` - Extract Deal of Day, Trending Products, Just Bargained

**Status**: ✅ **Should PASS** (Independent of login)

**Run**:
```bash
pytest framework/tests/web/gajab/flow_cases/test_02_location_and_home.py -v
```

---

### 3. **test_03_product_filters.py** - Category & Filtering
**Tests**: 1
- `test_toys_games_filter_and_product_selection` - Navigate Toys & Games, filter by brand (SERA'S BASKET), price range (427-727), select dartboard product

**Status**: ✅ **Should PASS** (Independent of login)

**Run**:
```bash
pytest framework/tests/web/gajab/flow_cases/test_03_product_filters.py -v
```

---

### 4. **test_automated_matrix.py** - Test Matrix (Parametrized)
**Tests**: 4 parametrized test functions covering:
- `test_automated_authentication_flow` - GJ-MAN-001 (Login)
- `test_automated_location_flow` - GJ-MAN-005 (Pincode)
- `test_automated_dynamic_home_sections` - GJ-MAN-007, GJ-MAN-008, GJ-MAN-010 (Products)
- `test_automated_product_filter_flow` - GJ-MAN-011 to 014 (Filters & Product)

**Status**: 
- Login: ⚠️ May fail
- Others: ✅ Should pass

**Run**:
```bash
pytest framework/tests/web/gajab/test_automated_matrix.py -v
```

---

### 5. **test_api_example.py** - API Tests (Independent)
**Tests**: 2
- `test_get_single_post_returns_expected_shape` - GET /posts/1
- `test_create_post_returns_201` - POST /posts

**Status**: ✅ **Should PASS** (No Gajab dependency)

**Run**:
```bash
pytest framework/tests/web/test_api_example.py -v
```

---

### 6. **test_data_driven_example.py** - Data-Driven Tests
**Tests**: Parametrized with search terms from JSON

**Status**: ✅ **Should PASS** (Uses playwright.dev, not Gajab)

**Run**:
```bash
pytest framework/tests/web/test_data_driven_example.py -v
```

---

## Complete Test Execution Commands

### Run All Gajab Tests
```bash
pytest framework/tests/web/gajab/ -v --html=reports/gajab-complete.html --self-contained-html
```

### Run Only Tests Likely to PASS
```bash
pytest framework/tests/web/gajab/flow_cases/test_02_location_and_home.py framework/tests/web/gajab/flow_cases/test_03_product_filters.py -v
```

### Run All Tests (Including API & Data-Driven)
```bash
pytest framework/tests/web/ -v --html=reports/complete-report.html --self-contained-html
```

### Run Tests with Specific Marker
```bash
pytest framework/tests/web/gajab/ -v -m critical
pytest framework/tests/web/gajab/ -v -m smoke
```

### Run with Verbose Output & Screenshots
```bash
pytest framework/tests/web/gajab/ -v -s --tb=short
```

### Run Single Test
```bash
pytest framework/tests/web/gajab/flow_cases/test_02_location_and_home.py::test_home_sections_return_dynamic_products -v
```

---

## Expected Test Results

### Likely to PASS ✅
1. `test_pincode_is_reflected_in_header` - Pincode selection
2. `test_home_sections_return_dynamic_products` - Home products extraction
3. `test_toys_games_filter_and_product_selection` - Category & filters
4. `test_automated_location_flow` - Pincode (GJ-MAN-005)
5. `test_automated_dynamic_home_sections` - Home products (GJ-MAN-007, 008, 010)
6. `test_automated_product_filter_flow` - Filters & product (GJ-MAN-011-014)
7. API tests - Independent tests
8. Data-driven tests - Independent tests

### Likely to FAIL ❌
1. `test_login_with_default_otp` - OTP field doesn't exist on website
2. `test_automated_authentication_flow` - Same login issue (GJ-MAN-001)

---

## Test Case Mapping to Hackathon Requirements

| Hackathon Step | Test Case | File | Status |
|---|---|---|---|
| 1. Navigate | Implicit in all tests | flow_cases | ✅ |
| 2-4. Login/OTP | `test_login_with_default_otp` | test_01 | ⚠️ Website bug |
| 5. Pincode | `test_pincode_is_reflected_in_header` | test_02 | ✅ |
| 6. Deal of Day | `test_home_sections_return_dynamic_products` | test_02 | ✅ |
| 7. Email | Manual/Out of scope | - | - |
| 8-10. Home Products | `test_home_sections_return_dynamic_products` | test_02 | ✅ |
| 11. Categories | `test_toys_games_filter_and_product_selection` | test_03 | ✅ |
| 12-14. Filters | `test_toys_games_filter_and_product_selection` | test_03 | ✅ |
| 15-22. Bargaining/Payment/Orders | Manual | - | - |

---

## How to Get Better Results

### If Login Tests Fail (Expected)
1. Skip login tests: `pytest framework/tests/web/gajab/ -v -k "not login"`
2. Focus on non-login features (pincode, products, filters)
3. Document as "Known Limitation: Website OTP field missing"

### If Selector Tests Fail
1. Run diagnostic: `python check_selectors.py`
2. Update selectors in page objects based on live site
3. Re-run tests

### To Generate Execution Report
```bash
pytest framework/tests/web/gajab/ -v --html=reports/execution-report.html --self-contained-html --alluredir=reports/allure-results
```

### View Reports
- HTML Report: Open `reports/execution-report.html` in browser
- Allure Report: `allure serve reports/allure-results`
- Screenshots: Check `reports/screenshots/` directory
- Traces: Check `reports/traces/` directory

---

## Test Execution Timeline

For 5-hour hackathon with ~3 hours for automation:

1. **Setup (5 min)**
   - Verify selectors work
   - Set environment variables

2. **Run Core Tests (30 min)**
   - All gajab tests: `pytest framework/tests/web/gajab/ -v`
   - Generate report

3. **Fix Failing Tests (60 min)**
   - If login fails: skip and document
   - If selectors fail: update and re-run
   - Run API/data-driven tests (should pass)

4. **Report & Documentation (25 min)**
   - Capture HTML reports
   - Add screenshots to submission
   - Document known limitations
   - Create execution summary

---

## Quick Start Command

```bash
# Run all tests and generate report (30-45 minutes)
pytest framework/tests/web/gajab/ -v --html=reports/gajab-test-run.html --self-contained-html -k "not login" 2>&1 | tee test-execution.log

# Then run API tests
pytest framework/tests/web/test_api_example.py framework/tests/web/test_data_driven_example.py -v

# View results
type reports/gajab-test-run.html
```

---

## Notes for Hackathon Submission

✅ **Include in submission:**
- Test execution reports (HTML)
- Screenshot of passing tests
- Known limitations document
- Selectors verification report

❌ **Do NOT submit:**
- API keys in repo
- Credentials in screenshots
- Uncommitted changes

✅ **Document:**
- Which tests ran successfully
- Which tests failed and why
- Workarounds implemented
- Time spent on automation vs bug quest
