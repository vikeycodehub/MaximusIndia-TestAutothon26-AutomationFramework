# ✅ GAJAB AUTOMATION TEST SUITE - COMPLETE INVENTORY

## 📊 Test Suite Statistics

- **Total Test Files**: 6
- **Total Test Cases**: 12+
- **Frameworks**: Pytest with Playwright
- **Test Types**: Integration, API, Data-Driven
- **Coverage**: Home page, Filters, Authentication, API

---

## 🧪 Detailed Test Inventory

### TEST SUITE 1: Authentication Flow
**File**: `framework/tests/web/gajab/flow_cases/test_01_login_otp.py`
**Location**: Flow Case 01

| Test Name | Mapping | What It Tests | Status |
|-----------|---------|---------------|--------|
| `test_login_with_default_otp` | GJ-MAN-001 | Login with mobile + OTP (123456) | ⚠️ May Fail |

**Code**:
```python
def test_login_with_default_otp(page):
    mobile_number = "9" + "".join(str(random.randint(0, 9)) for _ in range(9))
    login_page = GajabLoginPage(page).open()
    login_page.login_with_mobile(mobile_number)
    assert login_page.is_logged_in()
```

**Expected**: Login → Request OTP → Enter OTP (123456) → Verify logged in

**Issue**: Gajab website missing `#otp-input-0` field

---

### TEST SUITE 2: Location & Home Page
**File**: `framework/tests/web/gajab/flow_cases/test_02_location_and_home.py`
**Location**: Flow Case 02

| Test Name | Mapping | What It Tests | Status |
|-----------|---------|---------------|--------|
| `test_pincode_is_reflected_in_header` | GJ-MAN-005 | Set pincode (560037) and verify in header | ✅ Should Pass |
| `test_home_sections_return_dynamic_products` | GJ-MAN-007, 008, 010 | Extract Deal of Day, Trending, Just Bargained | ✅ Should Pass |

**Code - Test 1**:
```python
def test_pincode_is_reflected_in_header(page):
    home_page = GajabHomePage(page).open()
    home_page.set_pincode("560037")
    assert "560037" in home_page.current_location_text()
```

**Code - Test 2**:
```python
def test_home_sections_return_dynamic_products(page):
    home_page = GajabHomePage(page).open()
    deal = home_page.deal_of_the_day()
    most_bargained = home_page.most_bargained_trending_product()
    cheapest = home_page.cheapest_just_bargained_product()
    
    assert deal.name and deal.asking_price is not None
    assert most_bargained.name and most_bargained.bargains is not None
    assert cheapest.name and cheapest.asking_price is not None
```

**What It Extracts**:
- Deal of the Day: name, price, image, link
- Most-Bargained Product: name, bargain count, link
- Cheapest Product: name, price, link

---

### TEST SUITE 3: Product Filters & Selection
**File**: `framework/tests/web/gajab/flow_cases/test_03_product_filters.py`
**Location**: Flow Case 03

| Test Name | Mapping | What It Tests | Status |
|-----------|---------|---------------|--------|
| `test_toys_games_filter_and_product_selection` | GJ-MAN-011 to 014 | Navigate → Filter → Select Product | ✅ Should Pass |

**Code**:
```python
def test_toys_games_filter_and_product_selection(page):
    product_list = GajabProductListPage(page).open_toys_and_games()
    product_list.select_brand("SERA'S BASKET")
    product_list.set_price_range(427, 727)
    matching_products = [p for p in product_list.products() 
                        if "Dartboard" in p.name]
    assert matching_products
    product_list.select_product("Classic 15.7 Inch Soft Tip Dartboard Game Set")
    assert "/product-detail/" in page.url
```

**Steps**:
1. Navigate to Toys & Games category
2. Filter by brand: "SERA'S BASKET"
3. Set price range: ₹427 to ₹727
4. Verify "Classic 15.7 Inch Soft Tip Dartboard Game Set" appears
5. Click product → Verify product detail page opens

---

### TEST SUITE 4: Automated Test Matrix
**File**: `framework/tests/web/gajab/test_automated_matrix.py`
**Location**: Main test matrix

| Test Function | Parametrized Cases | Maps To | Status |
|---------------|-------------------|---------|--------|
| `test_automated_authentication_flow` | GJ-MAN-001 | Login | ⚠️ May Fail |
| `test_automated_location_flow` | GJ-MAN-005 | Pincode | ✅ Should Pass |
| `test_automated_dynamic_home_sections` | GJ-MAN-007, 008, 010 | Home products | ✅ Should Pass |
| `test_automated_product_filter_flow` | GJ-MAN-011, 012, 013, 014, 040 | Filters + Product detail | ✅ Should Pass |

**Code Snippet**:
```python
@pytest.mark.parametrize("case_id,pincode", [("GJ-MAN-005", "560037")])
def test_automated_location_flow(page, case_id, pincode):
    home = GajabHomePage(page).open()
    home.set_pincode(pincode)
    assert pincode in home.current_location_text()

@pytest.mark.parametrize("case_id", ["GJ-MAN-007", "GJ-MAN-008", "GJ-MAN-010"])
def test_automated_dynamic_home_sections(page, case_id):
    home = GajabHomePage(page).open()
    if case_id == "GJ-MAN-007":
        product = home.deal_of_the_day()
    elif case_id == "GJ-MAN-008":
        product = home.most_bargained_trending_product()
    else:
        product = home.cheapest_just_bargained_product()
    assert product.name and product.asking_price is not None
```

**Comprehensive product filter test**:
```python
def test_automated_product_filter_flow(page):
    product_list = GajabProductListPage(page).open_toys_and_games()
    product_list.select_brand("SERA'S BASKET")
    product_list.set_price_range(427, 727)
    products = [p for p in product_list.products() 
               if REQUIRED_PRODUCT.lower() in p.name.lower()]
    assert products and all(427 <= p.price <= 727 for p in products)
    product_list.select_product(REQUIRED_PRODUCT)
    assert "/product-detail/" in page.url
```

---

### TEST SUITE 5: API Testing
**File**: `framework/tests/web/test_api_example.py`

| Test Name | Endpoint | Status |
|-----------|----------|--------|
| `test_get_single_post_returns_expected_shape` | GET /posts/1 | ✅ Should Pass |
| `test_create_post_returns_201` | POST /posts | ✅ Should Pass |

**Code**:
```python
def test_get_single_post_returns_expected_shape():
    client = ApiClient()
    response = client.get("/posts/1")
    assert response.status_code == 200
    body = response.json()
    assert set(["userId", "id", "title", "body"]).issubset(body.keys())

def test_create_post_returns_201():
    client = ApiClient()
    response = client.post("/posts", json={"title": "foo", "body": "bar", "userId": 1})
    assert response.status_code == 201
    assert response.json()["title"] == "foo"
```

**Note**: Uses jsonplaceholder.typicode.com (no Gajab dependency)

---

### TEST SUITE 6: Data-Driven Testing
**File**: `framework/tests/web/test_data_driven_example.py`

| Test Name | Data Source | Status |
|-----------|------------|--------|
| `test_search_term_data_driven` | search_terms.json | ✅ Should Pass |

**Code**:
```python
@pytest.mark.parametrize("case", search_cases, ids=[c["search_term"] for c in search_cases])
def test_search_term_data_driven(page, case):
    home = PlaywrightDevHomePage(page).open()
    home.search(case["search_term"])
    result_text = home.first_result_text()
    assert case["expect_contains"].lower() in result_text.lower()
```

**Data**: Loaded from `framework/data/search_terms.json`

**Note**: Uses playwright.dev (no Gajab dependency)

---

## 🎯 Test Execution Plan

### Command 1: Run All Gajab Tests
```bash
pytest framework/tests/web/gajab/ -v --html=reports/gajab-complete.html --self-contained-html
```
**Expected**: 7-8 tests total
- ✅ ~6-7 passing (location, home, filters)
- ❌ ~1 failing (login OTP)

### Command 2: Run API & Data-Driven Tests
```bash
pytest framework/tests/web/test_api_example.py framework/tests/web/test_data_driven_example.py -v
```
**Expected**: ✅ All passing (independent tests)

### Command 3: Skip Login Tests
```bash
pytest framework/tests/web/gajab/ -v -k "not login"
```
**Expected**: ✅ All passing

### Command 4: Run with Markers
```bash
pytest framework/tests/web/gajab/ -v -m critical
pytest framework/tests/web/gajab/ -v -m smoke
```

### Command 5: Generate Full Report
```bash
pytest framework/tests/ -v --html=reports/full-test-run.html --self-contained-html --alluredir=reports/allure-results 2>&1 | tee test-execution.log
```

---

## 📈 Pass/Fail Prediction

| Test Category | Count | Predicted Status |
|---------------|-------|------------------|
| Login Tests | 2 | ❌ FAIL (website bug) |
| Location & Home | 5 | ✅ PASS |
| Filters & Products | 3+ | ✅ PASS |
| API Tests | 2 | ✅ PASS |
| Data-Driven | 1+ | ✅ PASS |
| **TOTAL** | **13+** | **~11 PASS / ~2 FAIL** |

**Success Rate**: ~85% expected (only login failing due to website)

---

## 🚀 How to Run Everything

### Option 1: PowerShell Script
```powershell
.\run_all_tests.ps1
```

### Option 2: Individual Commands
```bash
# Gajab tests
pytest framework/tests/web/gajab/ -v

# Skip login (if failing)
pytest framework/tests/web/gajab/ -v -k "not login"

# API tests
pytest framework/tests/web/test_api_example.py -v

# Data-driven tests
pytest framework/tests/web/test_data_driven_example.py -v
```

### Option 3: Generate Reports
```bash
pytest framework/tests/ -v \
  --html=reports/complete-run.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  --tb=short 2>&1 | tee test-run.log
```

---

## 📋 Checklist for Hackathon

- [ ] Run all tests: `pytest framework/tests/web/gajab/ -v`
- [ ] Check results in reports/
- [ ] If login fails, skip and document: `-k "not login"`
- [ ] Generate HTML report
- [ ] Add screenshots to submission
- [ ] Document test results in README
- [ ] Include "Known Limitations" section
- [ ] Commit to GitHub with sample reports

---

## 📞 Summary

**You have a well-built automation test suite!**

✅ **Ready to Run**:
- Location selection (pincode)
- Home page products extraction
- Category navigation & filters
- API tests
- Data-driven tests

⚠️ **May Fail**:
- Login tests (Gajab website bug, not your code)

**Next Step**: Run `pytest framework/tests/web/gajab/ -v` and check reports!
