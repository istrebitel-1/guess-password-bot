from setuptools import setup


version = "0.0.1"

setup(
    name="conference-bot-backend",
    version=version,
    description="FastAPI app for conference bot",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    author="Raft",
    author_email="sales@raftds.com",
    include_package_data=True,
    install_requires=[
        "aiogram~=3.13.1",
        "langchain==0.3.1",
        "langchain-core==0.3.8",
        "langchain-openai==0.2.1",
        "langchain-text-splitters==0.3.0",
        "pydantic~=2.9.2",
        "pydantic_settings~=2.5.2",
    ],
    extras_require={
        "code-quality": [
            "black~=23.11.0",
            "flake8~=6.1.0",
            "isort~=5.12.0",
            "mypy~=1.7.1",
            "pylint~=3.0.2",
            "pylint_pydantic~=0.3.0",
            "types-pytz~=2024.1.0.20240203",
            "types-setuptools~=68.2.0.2",
        ],
        "testing": [
            "httpx~=0.26.0",
            "pytest~=7.4.3",
            "pytest_asyncio~=0.23.2",
        ],
    },
    packages=[],
    python_requires=">=3.10",
    keywords="FastAPI backend",
)
