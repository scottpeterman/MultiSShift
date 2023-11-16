from glob import glob

from setuptools import setup, find_packages

setup(
    name="multisshift",
    version="0.1.0",
    description="A native python SSH multi-tabbed Terminal based on PyQt6 and FastAPI",
    author="Scott Peterman",
    author_email="scottpeterman@gmail.com",
    url="https://github.com/scottpeterman/MultiSShift",
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "annotated-types==0.6.0",
        "anyio==3.7.1",
        "bcrypt==4.0.1",
        "cffi==1.16.0",
        "click==8.1.7",
        "colorama==0.4.6",
        "cryptography==41.0.5",
        "exceptiongroup==1.1.3",
        "fastapi==0.104.1",
        "greenlet==3.0.1",
        "h11==0.14.0",
        "httptools==0.6.1",
        "idna==3.4",
        "Jinja2==3.1.2",
        "MarkupSafe==2.1.3",
        "paramiko==3.3.1",
        "pycparser==2.21",
        "pydantic==2.4.2",
        "pydantic_core==2.10.1",
        "PyNaCl==1.5.0",
        "PyQt6==6.6.0",
        "PyQt6-Qt6==6.6.0",
        "PyQt6-sip==13.6.0",
        "PyQt6-WebEngine==6.6.0",
        "PyQt6-WebEngine-Qt6==6.6.0",
        "python-dotenv==1.0.0",
        "python-multipart==0.0.6",
        "PyYAML==6.0.1",
        "sniffio==1.3.0",
        "SQLAlchemy==2.0.23",
        "starlette==0.27.0",
        "typing_extensions==4.8.0",
        "uvicorn==0.24.0.post1",
        "watchfiles==0.21.0",
        "websockets==12.0",
    ],
    entry_points={
        "console_scripts": [
            "multishift = multisshift.__main__:main"
        ],
    },
)
