#    Copyright (C) 2012-2014  Octets - octets.etsmtl.ca
#
#    This file is part of SeaGoatVision.
#
#    SeaGoatVision is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This Makefile manage filter in cpp situate in folder filters.
# Build is done into directory build
.PHONY : filter third_party clean_python clean_third_party clean doc test

all: third_party filter

doc:
	make -C doc html

view_doc: doc
	firefox doc/build/html/index.html

# the test include make the plateform
test:
	if [ -a .coverage ]; then rm .coverage; fi;
	python2 -m flake8 --ignore="E721" --exclude="SeaGoatVision/server/cpp/cpp_code.py,SeaGoatVision/server/cpp/create_module.py" SeaGoatVision
	python2 -m nose2 --with-coverage
	coverage2 combine

view_test: test
	firefox htmlcov/index.html

filter:
	./filters/build_cpp_filter.py

third_party:
	-make -C thirdparty

clean_python:
	find . -type f -name '*.pyc' -exec rm {} \;

clean_third_party:
	-make -C thirdparty clean

clean: clean_python clean_third_party
	-rm -Rf ./build
