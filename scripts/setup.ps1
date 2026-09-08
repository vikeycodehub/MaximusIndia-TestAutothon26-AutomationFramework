# Installs deps + Playwright browsers. Run this first.
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
playwright install --with-deps
Write-Host "Setup complete. Copy .env.example to .env and adjust if needed." -ForegroundColor Green
