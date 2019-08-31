#!/bin/make -f

.PHONY: all clean install 

wotdir = c:/games/WOT
wotver = $(shell ls $(wotdir)/res_mods/ | grep "^1\." | tail -n1)
wotmod = res_mods/$(wotver)/scripts/client/gui/mods

all:
	python -m compileall mod_*.py

clean:
	rm *.pyc

install: all
	mkdir -p "$(wotdir)/$(wotmod)"
	cp -f *.pyc "$(wotdir)/$(wotmod)"

