# Valid sources for the university rankings scraper
VALID_SOURCES = ['usnews', 'times', 'qs']

# Valid regions for each source
REGIONS = {
    'usnews': [
        'africa', 'asia', 'australia-new-zealand', 'europe', 'latin-america'
    ],
}


SUBJECTS = {
    'usnews': ['agricultural-sciences', 'artificial-intelligence','arts-and-humanities',
              'biology-biochemistry', 'biotechnology-applied-microbiology', 'cardiac-cardiovascular',
              'cell-biology', 'chemical-engineering', 'chemistry', 'civil-engineering', 'clinical-medicine',
              'computer-science', 'condensed-matter-physics', 'ecology', 'economics-business', 'education-educational-research',
              'electrical-electronic-engineering', 'endocrinology-metabolism', 'energy-fuels', 'engineering', 'environment-ecology',
              'environmental-engineering', 'food-science-technology', 'gastroenterology-hepatology', 'geosciences',
              'green-sustainable-science-technology', 'immunology', 'infectious-diseases', 'marine-freshwater-biology',
              'materials-science', 'mathematics', 'mechanical-engineering', 'meteorology-atmospheric-sciences', 'microbiology',
              'molecular-biology-genetics', 'nanoscience-nanotechnology', 'neuroscience-behavior', 'oncology', 'optics',
              'pharmacology-toxicology', 'physical-chemistry', 'physics', 'plant-animal-science', 'polymer-science',
              'psychiatry-psychology', 'public-environmental-occupational-health', 'radiology-nuclear-medicine-medical-imaging',
              'social-sciences-public-health', 'space-science', 'surgery', 'water-resources'],
    'times': [
        'arts-and-humanities', 'business-and-economics', 'computer-science', 'education', 'engineering', 'law', 'life-sciences',
        'clinical-pre-clinical-health', 'physical-sciences', 'psychology', 'social-sciences'
    ],

    'qs': ['arts-humanities', 'linguistics', 'music', 'theology-divinity-religious-studies', 'archaeology', 'architecture-built-environment',
           'art-design', 'classics-ancient-history', 'english-language-literature', 'history', 'art-history', 'modern-languages',
           'performing-arts', 'philosophy', 'engineering-technology', 'chemical-engineering', 'civil-structural-engineering',
           'computer-science-information-systems', 'data-science-artificial-intelligence', 'electrical-electronic-engineering',
           'engineering-petroleum', 'mechanical-aeronautical-manufacturing-engineering', 'mineral-mining-engineering', 'life-sciences-medicine',
           'agriculture-forestry', 'anatomy-physiology', 'biological-sciences', 'dentistry', 'medicine', 'nursing', 'pharmacy-pharmacology',
           'psychology', 'veterinary-science', 'natural-sciences', 'chemistry', 'earth-marine-sciences', 'environmental-sciences',
           'geography', 'geology', 'geophysics', 'materials-sciences', 'mathematics', 'physics-astronomy', 'social-sciences-management',
           'accounting-finance', 'anthropology', 'business-management-studies', 'communication-media-studies', 'development-studies',
           'economics-econometrics', 'education-training', 'hospitality-leisure-management', 'law-legal-studies','library-information-management',
           'marketing', 'politics', 'social-policy-administration', 'sports-related-subjects', 'statistics-operational-research']
}

# Headers for HTTP requests
HEADERS = {
    'usnews': {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'priority': 'u=1, i',
        'referer': 'https://www.usnews.com/',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    },
    'times': {
        'sec-ch-ua-platform': '"macOS"',
        'Referer': 'https://www.timeshighereducation.com/world-university-rankings/2025/subject-ranking/business-and-economics',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
    },
    'qs': {
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
      'priority': 'u=0, i',
      'referer': 'https://www.topuniversities.com/university-subject-rankings/arts-humanities',
      'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"macOS"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'same-origin',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
  }
}