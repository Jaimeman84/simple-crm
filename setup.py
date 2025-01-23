from setuptools import setup, find_packages

setup(
    name="simple-crm",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'pandas',
        'sqlalchemy',
        'pytest',
        'python-dotenv',
    ],
) 