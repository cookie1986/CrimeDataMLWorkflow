.PHONY: check duplicate delete

check:
	python utils/file_manager.py --check

duplicate:
	python utils/file_manager.py --duplicate

delete:
	python utils/file_manager.py --delete