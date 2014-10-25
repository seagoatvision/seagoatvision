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
.PHONY : doc view_doc test view_test filter third_party clean_python clean_third_party clean_coverage clean_doc clean

all: third_party filter

doc:
	make -C doc html

view_doc:
	firefox doc/build/html/index.html

# the test include make the plateform
test: third_party test_flake8
	if [ -a .coverage ]; then rm .coverage; fi;
	@echo "Nose2 test"
	python2 -m nose2 --with-coverage -v
	# move and combine all coverage
	mv doc/.coverage.* .
	coverage2 combine

test_flake8:
	@echo "Flake 8 test"
	python2 -m flake8 --ignore="E721" --exclude="SeaGoatVision/server/cpp/cpp_code.py,SeaGoatVision/server/cpp/create_module.py" SeaGoatVision
	python2 -m flake8 tests
	python2 -m flake8 thirdparty/update.py

view_test:
	coverage html -d doc/build/htmlcov
	firefox doc/build/htmlcov/index.html

filter:
	./filters/build_cpp_filter.py

third_party:
	-make -C thirdparty

clean_python:
	-find . -type f -name '*.pyc' -exec rm {} \;
	-find . -type d -name '__pycache__' -exec rm -R {} \;

clean_third_party:
	-make -C thirdparty clean

clean_coverage:
	-rm .coverage
	-rm -R doc/build/htmlcov

clean_doc:
	-rm -R doc/build

clean: clean_python clean_third_party clean_coverage clean_doc
	-rm -Rf ./build
