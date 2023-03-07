import os

from setuptools import find_packages, setup


def parse_requirements(file):
    with open(os.path.join(os.path.dirname(__file__), file), mode="r", encoding="ascii") as req_file:
        return [line.strip() for line in req_file if "/" not in line]


setup(
    name="app",
    python_requires=">=3.11",
    version="0.0.1",
    description="Basic BS4 crawler",
    url="https://github.com/mpecovnik/predict-leads",
    author="Matic Pečovnik",
    author_email="matic.pecovnik@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=parse_requirements("requirements.txt"),
    zip_safe=False,
)
