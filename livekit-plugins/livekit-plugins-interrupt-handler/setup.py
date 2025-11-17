from setuptools import setup, find_packages

setup(
    name="livekit-plugins-interrupt-handler",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "livekit",
        "livekit-agents",
    ],
)
