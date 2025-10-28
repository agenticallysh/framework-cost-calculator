#!/usr/bin/env python3
"""
Setup script for Framework Cost Calculator
Makes the calculator available as a command-line tool and Python package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="framework-cost-calculator",
    version="1.0.0",
    author="Agentically",
    author_email="team@agentically.sh",
    description="Real-time cost estimation for AI agent frameworks with 2025 pricing data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/agenticallysh/framework-cost-calculator",
    py_modules=["cost_calculator", "api", "examples"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    extras_require={
        "web": ["flask>=3.0.0", "requests>=2.31.0"],
        "analytics": ["pandas>=2.1.0", "matplotlib>=3.7.0"],
        "dev": ["pytest>=7.0.0", "black>=23.0.0", "flake8>=6.0.0"],
    },
    entry_points={
        "console_scripts": [
            "framework-cost-calculator=cost_calculator:main",
            "framework-cost-api=api:run_server",
            "framework-cost-examples=examples:main",
        ],
    },
    keywords=[
        "ai",
        "agent",
        "framework",
        "cost",
        "calculator",
        "llm",
        "openai",
        "anthropic",
        "pricing",
        "autogen",
        "crewai",
        "langchain",
        "langgraph",
    ],
    project_urls={
        "Bug Reports": "https://github.com/agenticallysh/framework-cost-calculator/issues",
        "Source": "https://github.com/agenticallysh/framework-cost-calculator",
        "Documentation": "https://www.agentically.sh/ai-agentic-frameworks/cost-calculator/",
        "Interactive Calculator": "https://www.agentically.sh/ai-agentic-frameworks/cost-calculator/",
    },
)