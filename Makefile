clean:
	@rm -fr __pycache__
	@rm -fr roro_vision/__pycache__
	@rm -fr roro_vision.egg-info

dev_install:
	@pip install -e .

install:
	@pip install .
