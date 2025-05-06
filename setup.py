import setuptools

with open("README.md", "r") as f:
    readme = f.read()

# with open("requirements.txt", "r") as f:
#     reqs = [lib.strip() for lib in f if lib]

setuptools.setup(
    name="university_ranking_scraper",
    version="0.0.1",
    description="A web crawler to crawl Best Global University Ranking on usnews, Times Higher Education, and QS websites",
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Low Wei Hong',
    author_email='M140042@e.ntu.edu.sg',
    url="https://github.com/lowweihong/university_ranking_scraper",
    packages=setuptools.find_packages(),
    keywords=["university_rankings", "usnews", "times_higher_education", "qs"],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=['pandas', 'httpx', 'lxml']
)
