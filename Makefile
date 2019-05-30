# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Copyright (c) 2014 Mozilla Corporation
#

.PHONY:list ## List all make targets
list:
	@echo 'Available make targets:'
	@grep '^[^#[:space:]^\.PHONY.*].*:' Makefile

.PHONY: dependencies ## install all dependencies
dependencies:
	pip install -e .
	pip install -r requirements.txt

.PHONY: tests ## run all unit tests
tests:
	pytest tests/unit-tests/
