#!/bin/make -f

.PHONY: all clean install 

wotver = 1.6.0.2
wotdir = c:/games/WOT
wotmod = res_mods/$(wotver)/scripts/client/gui/mods

all:
	python -m compileall mod_*.py

clean:
	rm *.pyc

install: all
	mkdir -p "$(wotdir)/$(wotmod)"
	cp -f *.pyc "$(wotdir)/$(wotmod)"

