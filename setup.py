import setuptools


with open('README.md', 'r') as fp:
    long_description = fp.read()


setuptools.setup(
    name="common-captcha",
    version="0.0.1",
    author="lei.wang",
    author_email="1061379682@qq.com",
    description="package for common common_captcha",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
        'redis',
        'pillow',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
