#!/bin/make -f

.PHONY: all clean

moddir = res/scripts/client/gui/mods
domain = com.github.ushmal

sources = $(wildcard *.py)
targets = $(sources:.py=.pyc)
wotmods = $(targets:mod_%.pyc=mods/$(domain).%.wotmod)

all: $(wotmods)

%.pyc: %.py
	python2 -m compileall $<

mods/$(domain).%.wotmod: mod_%.pyc
	mkdir -p $(moddir)
	cp $< $(moddir)
	zip -0 -r -D -X $@ res
	rm -rf res

clean:
	-rm $(wotmods)

