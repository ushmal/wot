#!/bin/make -f

.PHONY: all clean

prefix = lx1r
moddir = res/scripts/client/gui/mods

sources = $(wildcard *.py)
targets = $(sources:.py=.pyc)
wotmods = $(targets:mod_%.pyc=mods/$(prefix).%.wotmod)

all: $(wotmods)

%.pyc: %.py
	python2 -m compileall $<

mods/$(prefix).%.wotmod: mod_%.pyc
	mkdir -p $(moddir)
	cp $< $(moddir)
	zip -0 -r -D -X $@ res
	rm -rf res

clean:
	-rm $(wotmods)

