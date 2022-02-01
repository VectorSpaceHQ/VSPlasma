build:
	# Make py file from ui
	pyuic5 ./gui/vsplasma.ui -o ./gui/vsplasma_ui.py
	# Make resource file for icons
	pyrcc5 ./gui/resources.qrc -o ./gui/resources_rc.py

doc:
	# Generate UML diagram
	pyreverse -o pdf -p pyreverse vsplasma
init:
	pip3 install -r ../requirements.txt
test:
	python3 -m pytest tests

flake8:
	flake8 --ignore=E501,F401,E128,E402,E731,F821 vsplasma
