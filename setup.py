"""Project setup."""

from setuptools import setup, find_packages

DEPENDENCIES = [
    "Flask-SQLAlchemy==2.5.1",
    "flask==2.0.3",
    "gunicorn==20.1.0",
    "jsonschema==4.4.0",
]

setup(
    name="myapp",
    packages=find_packages(),
    include_package_data=False,
    install_requires=DEPENDENCIES,
    version="1.0.0",
)
