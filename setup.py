from setuptools import setup, find_packages

setup(
    name = 'pyalma',
    packages = find_packages(),
    test_suite="test",
    version = '0.0.1',
    description = 'Python client for ExLibris Alma',
    author = 'Getty Research Institute',
    author_email = 'jgomez@getty.edu',
    url = 'https://stash.getty.edu/projects/GRIIS/repos/pyalma/browse',
    install_requires = ['pymarc', 'requests'],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: pre-Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
