.PHONE: fix

fix:
	black tasks_watcher/
	isort tasks_watcher/

check:
	mypy tasks_watcher/
