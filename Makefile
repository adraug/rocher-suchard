SHELL := /bin/sh

# Override this value when packwiz is installed elsewhere, for example:
# make PACKWIZ=/path/to/packwiz export
PACKWIZ ?= packwiz

PACK_NAME := $(shell sed -n 's/^name = "\(.*\)"$$/\1/p' pack.toml)
PACK_VERSION := $(shell sed -n 's/^version = "\(.*\)"$$/\1/p' pack.toml)
DIST_DIR := dist
EXPORT_FILE := $(DIST_DIR)/$(PACK_NAME)-$(PACK_VERSION).mrpack

.PHONY: help refresh export clean pull push status

help:
	@printf '%s\n' \
	  'Available targets:' \
	  '  make refresh  Rebuild index.toml after editing the pack sources.' \
	  '  make export   Refresh and create the Modrinth archive in dist/.' \
	  '  make clean    Remove generated files in dist/.' \
	  '  make pull     Fetch and fast-forward from the tracked Git remote.' \
	  '  make push     Push the current branch to its tracked Git remote.' \
	  '  make status   Show the Git working tree status.'

refresh:
	"$(PACKWIZ)" refresh

export: refresh
	@mkdir -p "$(DIST_DIR)"
	"$(PACKWIZ)" modrinth export --output "$(EXPORT_FILE)"
	@printf 'Created %s\n' "$(EXPORT_FILE)"

clean:
	rm -rf "$(DIST_DIR)"

pull:
	git pull --ff-only

push:
	git push

status:
	git status --short
