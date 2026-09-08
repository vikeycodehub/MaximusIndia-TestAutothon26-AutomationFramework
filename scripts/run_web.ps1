# Runs the full web regression suite in parallel.
pytest framework/tests/web -m "web or api" -n auto
