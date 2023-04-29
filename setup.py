from setuptools import setup,find_packages
print(find_packages())
setup(
    name='python-discord-bot',
    version='1.0.0',
    packages=find_packages(exclude=("tests",)),
    url='',
    license='',
    author='Patrik',
    author_email='',
    description='',
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    python_requires=">=3.10",
    install_requires=["aiohttp==3.8.4",
        "aiosignal==1.3.1",
        "async-timeout==4.0.2",
        "attrs==22.2.0",
        "certifi==2022.12.7",
        "charset-normalizer==3.1.0",
        "discord==2.2.2",
        "discord.py==2.2.2",
        "frozenlist==1.3.3",
        "idna==3.4",
        "multidict==6.0.4",
        "requests==2.28.2",
        "urllib3==1.26.15",
        "yarl==1.8.2"
        ],
)
