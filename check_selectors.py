#!/usr/bin/env python
"""Diagnostic script to verify selectors on live Gajab site."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import sync_playwright
from framework.config.settings import settings

BASE_URL = settings.base_url

def check_selectors():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print(f"Navigating to {BASE_URL}...")
        page.goto(BASE_URL, wait_until="domcontentloaded")
        
        selectors = {
            "Login Link": "a[href='/auth/signin']",
            "Location Menu Button": "#location-desktop-menu-btn",
            "Location Menu Text": "#location-desktop-menu-text",
            "Pincode Input": "#location-desktop-search-input",
            "Pincode Suggestion": "#location-desktop-suggestion-item-0",
        }
        
        print("\n" + "="*60)
        print("SELECTOR CHECK - HOME PAGE")
        print("="*60 + "\n")
        
        for name, selector in selectors.items():
            try:
                count = page.locator(selector).count()
                is_visible = page.locator(selector).first.is_visible() if count > 0 else False
                status = "✓ FOUND" if count > 0 else "✗ NOT FOUND"
                visible_str = f" (visible: {is_visible})" if count > 0 else ""
                print(f"{name:25} {status:15} Count: {count}{visible_str}")
            except Exception as e:
                print(f"{name:25} ✗ ERROR: {e}")
        
        # Try clicking login link
        print("\n" + "="*60)
        print("LOGIN FLOW CHECK")
        print("="*60 + "\n")
        
        try:
            login_link = page.locator("a[href='/auth/signin']").first
            if login_link.count():
                print("✓ Login link found, clicking...")
                login_link.click(force=True, timeout=5000)
                page.wait_for_timeout(2000)
                
                # Check OTP field
                otp_field = page.locator("#otp-input-0")
                if otp_field.count():
                    print("✓ OTP field #otp-input-0 FOUND")
                else:
                    print("✗ OTP field #otp-input-0 NOT FOUND")
                    # Try to find any OTP inputs
                    all_otp = page.locator("input[id*='otp']")
                    if all_otp.count():
                        print(f"  Found {all_otp.count()} OTP-related inputs")
                        for i in range(min(3, all_otp.count())):
                            otp_id = all_otp.nth(i).get_attribute("id")
                            print(f"    - {otp_id}")
            else:
                print("✗ Login link not found")
        except Exception as e:
            print(f"✗ Error during login flow: {e}")
        
        browser.close()

if __name__ == "__main__":
    try:
        check_selectors()
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
