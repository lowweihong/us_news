# US_news Best Global Universities scraper
A simple web crawler to crawl Best Global University Ranking on [US News website](https://www.usnews.com/education/best-global-universities).

Interested to know how I do it? Visit [here](https://towardsdatascience.com/how-to-build-a-simple-web-crawler-66082fc82470) for more info.

# Installation
Install with pip:

`$ pip install us_news`

# Usage

```Python
import us_news
df = us_news.scrape('asia', 'surgery')

```

# Documentations

`us_news.scrape(region, subjects)`

where

Supported regions:
- africa
- asia
- australia-new-zealand
- europe
- latin-america

Supported subjects:
- agricultural-sciences
- arts-and-humanities
- biology-biochemistry
- cardiac-cardiovascular
- chemistry
- civil-engineering
- clinical-medicine
- computer-science
- economics-business
- electrical-electronic-engineering
- engineering
- environment-ecology
- geosciences
- immunology
- materials-science
- mathematics
- mechanical-engineering
- microbiology
- molecular-biology-genetics
- neuroscience-behavior
- oncology
- pharmacology-toxicology
- physics
- plant-animal-science
- psychiatry-psychology
- social-sciences-public-health
- space-science
- surgery


