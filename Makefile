.PHONE: fix

fix:
	black tasks_watcher/
	isort tasks_watcher/

check:
	mypy tasks_watcher/
	pylint tasks_watcher/
	black --check tasks_watcher/
	isort --check tasks_watcher/
