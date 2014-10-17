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
.PHONY : pep8 execution cli

all: pep8 doc execution cli

pep8:
	@echo ""
	@echo "Test pep8"
	@echo ""
	cd ..; python2 -m flake8 --ignore="E721" --exclude="SeaGoatVision/server/cpp/cpp_code.py,SeaGoatVision/server/cpp/create_module.py" SeaGoatVision
	python2 -m flake8 .

execution:
	@echo ""
	@echo "Python test - execution"
	@echo ""
	python2 -m nose2 test_execution --with-coverage

cli:
	@echo ""
	@echo "Python test - cli"
	@echo ""
	python2 -m nose2 test_cli --with-coverage

doc:
	@echo ""
	@echo "Python test - doc"
	@echo ""
	python2 -m nose2 test_doc --with-coverage
