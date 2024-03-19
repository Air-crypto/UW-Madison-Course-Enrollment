run:
	@if command -v python3 &>/dev/null; then \
		echo "Using python3"; \
		python3 courseSelectionV5.py; \
	elif command -v python &>/dev/null; then \
		echo "Using python"; \
		python courseSelectionV5.py; \
	else \
		echo "Python is not installed"; \
		exit 1; \
	fi


installReqs:
	@if command -v python3 &>/dev/null; then \
		echo "Using python3"; \
		python3 -m pip install -r requirements.txt; \
	elif command -v python &>/dev/null; then \
		echo "Using python"; \
		python -m pip install -r requirements.txt; \
	else \
		echo "Python is not installed"; \
		exit 1; \
	fi
