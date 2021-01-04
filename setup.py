from setuptools import find_packages
from setuptools import setup

requirements = """
opencv-python
pillow
numpy
"""
setup(name='roro_vision',
      setup_requires=['setuptools_scm'],
      packages=find_packages(),
      install_requires=requirements,
      include_package_data=True,
      scripts=['scripts/roro_run.py'],
      zip_safe=False)
