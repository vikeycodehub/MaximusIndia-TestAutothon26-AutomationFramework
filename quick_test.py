#!/usr/bin/env python
"""Quick diagnostic script to test framework setup."""
import sys
from pathlib import Path

# Add framework to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("TESTING FRAMEWORK SETUP")
print("=" * 60)

# Test 1: Import settings
try:
    from framework.config.settings import settings
    print("✓ Settings imported successfully")
    print(f"  - Base URL: {settings.base_url}")
    print(f"  - Environment: {settings.env}")
    print(f"  - Headless: {settings.headless}")
except Exception as e:
    print(f"✗ Settings import failed: {e}")
    sys.exit(1)

# Test 2: Import AI modules
try:
    from framework.ai.llm_client import get_client
    print("✓ AI LLM client imported successfully")
    client = get_client()
    print(f"  - Provider: {client.provider if client else 'None'}")
    print(f"  - Model: {client.model if client else 'None'}")
except Exception as e:
    print(f"✗ AI client import failed: {e}")
    sys.exit(1)

# Test 3: Import page objects
try:
    from framework.pages.gajab.login_page import GajabLoginPage
    from framework.pages.gajab.home_page import GajabHomePage
    from framework.pages.gajab.product_list_page import GajabProductListPage
    print("✓ Gajab page objects imported successfully")
    print(f"  - GajabLoginPage: {GajabLoginPage.__name__}")
    print(f"  - GajabHomePage: {GajabHomePage.__name__}")
    print(f"  - GajabProductListPage: {GajabProductListPage.__name__}")
except Exception as e:
    print(f"✗ Page objects import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Check if OpenAI API key is set
try:
    import os
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("✓ OpenAI API key found (masked)")
        print(f"  - Key preview: {api_key[:20]}...{api_key[-10:]}")
    else:
        print("⚠ OpenAI API key NOT set in .env")
except Exception as e:
    print(f"✗ Environment check failed: {e}")

print("\n" + "=" * 60)
print("FRAMEWORK DIAGNOSTIC COMPLETE")
print("=" * 60)
