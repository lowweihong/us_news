# University Subject Ranking Best Global Universities scraper
A web crawler to scrape university rankings from US News, Times Higher Education, and QS websites.

Interested to know how I do it? Visit [here](https://towardsdatascience.com/how-to-build-a-simple-web-crawler-66082fc82470) for more info.

# Installation
Install with pip:

`$ pip install university_ranking_scraper`

# Usage

```Python
import university_ranking_scraper

# usnews, https://www.usnews.com/education/best-global-universities/surgery?region=asia
df = university_ranking_scraper.scrape_usnews('asia', 'surgery')

# timeshighereducation, https://www.timeshighereducation.com/world-university-rankings/2025/subject-ranking/arts-and-humanities
df = university_ranking_scraper.scrape_times('arts-and-humanities')

# qs, https://www.topuniversities.com/university-subject-rankings/linguistics
df = university_ranking_scraper.scrape_qs('linguistics')
```



