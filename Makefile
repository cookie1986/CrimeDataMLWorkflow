.PHONY: check duplicate delete

check:
	python config/file_manager.py --check

duplicate:
	python config/file_manager.py --duplicate

delete:
	python config/file_manager.py --delete