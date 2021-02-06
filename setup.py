from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="libvirt_vmcfg",
    version="0.0.1",
    description="XML builder for libvirt virtual machine configuration",
    long_description=long_description, 
    long_description_content_type="text/markdown", 
    url="https://github.com/Elizafox/libvirt_vmcfg",
    author="Elizabeth Myers",
    author_email="elizabeth.jennifer.myers@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Text Processing :: XML",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="libvirt, virtual machines, xml generator",
    packages=find_packages(),
    python_requires=">=3.8, <4",
    install_requires=["lxml"],
    project_urls={ 
        "Bug Reports": "https://github.com/Elizafox/libvirt_vmcfg/issues",
        "Donations": "https://paypal.me/Elizafox",
        "Say Thanks!": "https://saythanks.io/to/elizabeth.jennifer.myers%40gmail.com",
        "Source": "https://github.com/Elizafox/libvirt_vmcfg",
    }
)
