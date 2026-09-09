#!/usr/bin/env python
"""Direct import and error check."""
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

try:
    # Step 1: Check environment
    print("Step 1: Loading environment...")
    from dotenv import load_dotenv
    import os
    load_dotenv()
    print("✓ Environment loaded")
    
    # Step 2: Check settings
    print("\nStep 2: Loading settings...")
    from framework.config.settings import settings
    print(f"✓ Settings loaded (env={settings.env}, base_url={settings.base_url})")
    
    # Step 3: Check AI client
    print("\nStep 3: Loading AI client...")
    from framework.ai.llm_client import get_client
    client = get_client()
    if client:
        print(f"✓ AI client loaded (provider={client.provider}, model={client.model})")
    else:
        print("⚠ AI client is None (API key might be missing)")
    
    # Step 4: Check home page import
    print("\nStep 4: Loading GajabHomePage...")
    from framework.pages.gajab.home_page import GajabHomePage
    print("✓ GajabHomePage imported")
    
    # Step 5: Test Playwright import
    print("\nStep 5: Loading Playwright...")
    from playwright.sync_api import sync_playwright
    print("✓ Playwright loaded")
    
    print("\n" + "="*60)
    print("ALL IMPORTS SUCCESSFUL")
    print("="*60)
    
except Exception as e:
    print(f"\n✗ ERROR: {type(e).__name__}: {e}")
    traceback.print_exc()
    sys.exit(1)
