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
- artificial-intelligence
- arts-and-humanities
- biology-biochemistry
- biotechnology-applied-microbiology
- cardiac-cardiovascular
- cell-biology
- chemical-engineering
- chemistry
- civil-engineering
- clinical-medicine
- computer-science
- condensed-matter-physics
- ecology
- economics-business
- education-educational-research
- electrical-electronic-engineering
- endocrinology-metabolism
- energy-fuels
- engineering
- environment-ecology
- environmental-engineering
- food-science-technology
- gastroenterology-hepatology
- geosciences
- green-sustainable-science-technology
- immunology
- infectious-diseases
- marine-freshwater-biology
- materials-science
- mathematics
- mechanical-engineering
- meteorology-atmospheric-sciences
- microbiology
- molecular-biology-genetics
- nanoscience-nanotechnology
- neuroscience-behavior
- oncology
- optics
- pharmacology-toxicology
- physical-chemistry
- physics
- plant-animal-science
- polymer-science
- psychiatry-psychology
- public-environmental-occupational-health
- radiology-nuclear-medicine-medical-imaging
- social-sciences-public-health
- space-science
- surgery
- water-resources


