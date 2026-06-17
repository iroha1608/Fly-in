UV		:= uv
PYTHON	:= python3
RM		:= rm -rf

# Mandatory requirements
# install, run, debug, clean, lint, lint-strict

all: install

# uvのインストール
uv:
	curl -LsSf https://astral.sh/uv/install.sh | sh

# 仮想環境の作成、依存関係のインストール
install:
	$(UV) sync
	wget https://cdn.intra.42.fr/document/document/49241/maps.tar.gz

# 仮想環境のセットアップ
setup:
	$(UV) venv

run:
	$(UV) run $(PYTHON) main.py

debug:
	$(UV) run $(PYTHON) pdb

clean:
	find . -name "*.pyc" -type f -delete -print
	find . -type d -name "__pycache__" -delete -print
	$(RM) .mypy_cache
	$(RM) .pytest_cache
	$(RM) .ruff_cache
	$(RM) data/output/*

fclean: clean
	$(RM) .venv

lint:
	- $(UV) run flake8 .
	- $(UV) run mypy --warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs .
	- $(UV) run ruff check .
# 	- $(UV) run ty check $(SRC_DIR)

lint-strict:
	- $(UV) run flake8 .
	- $(UV) run mypy --strict .


.PHONY: install run debug clean fclean lint lint-strict all uv setup
