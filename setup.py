from setuptools import setup, find_packages

setup(
    name="amr_dashboard",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.0",
        "pandas",
        "sqlalchemy",
        "st-aggrid",
    ],
    include_package_data=True,  # includes amr.db if you add MANIFEST.in
    entry_points={
        "console_scripts": [
            "amr-dashboard=amr_dashboard.app:main",  # optional
        ],
    },
)
