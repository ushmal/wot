#!/bin/make -f

.PHONY: all clean install 

wotdir = c:/games/WOT
wotver = $(shell ls $(wotdir)/mods/ | grep "^1\." | tail -n1)
moddir = res/scripts/client/gui/mods
domain = com.github.ushmal

sources = $(wildcard *.py)
targets = $(sources:.py=.pyc)
wotmods = $(targets:mod_%.pyc=mods/$(domain).%.wotmod)

all: $(wotmods)

%.pyc: %.py
	python -m compileall $<

mods/$(domain).%.wotmod: mod_%.pyc
	mkdir -p $(moddir)
	cp $< $(moddir)
	zip -0 -r -D -X $@ res
	rm -rf res

clean:
	-rm $(wotmods)

install: all
	cp -f $(wotmods) "$(wotdir)/mods/$(wotver)"

