import httpx
import argparse
import pandas as pd
import random
import time
from typing import List, Dict
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Valid regions and subjects for validation
VALID_REGIONS = [
    'africa', 'asia', 'australia-new-zealand', 'europe', 'latin-america'
]
VALID_SUBJECTS = ['agricultural-sciences', 'artificial-intelligence','arts-and-humanities',
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
                  'social-sciences-public-health', 'space-science', 'surgery', 'water-resources']

# Headers for HTTP requests
HEADERS = {
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
}

def validate_inputs(region: str, subject: str) -> None:
    """Validate region and subject inputs."""
    if region not in VALID_REGIONS:
        raise ValueError(f"Invalid region: {region}. Must be one of {VALID_REGIONS}")
    if subject not in VALID_SUBJECTS:
        raise ValueError(f"Invalid subject: {subject}. Must be one of {VALID_SUBJECTS}")

def scrape(region: str, subject: str, max_retries: int = 3, base_delay: float = 2.0) -> pd.DataFrame:
    """
    Scrape university rankings data from US News for a given region and subject.
    
    Args:
        region: The region to scrape data for.
        subject: The subject to scrape data for.
        max_retries: Maximum number of retry attempts for failed requests.
        base_delay: Base delay for exponential backoff in seconds.
    
    Returns:
        A pandas DataFrame containing the scraped data.
    """
    validate_inputs(region, subject)
    base_url = "https://www.usnews.com/education/best-global-universities/%s?format=json&region=%s"
    results: List[Dict] = []
    
    # Initial request to get total pages
    try:
        with httpx.Client(headers=HEADERS, timeout=10.0) as client:
            for attempt in range(max_retries):
                try:
                    response = client.get(base_url % (subject, region))
                    response.raise_for_status()
                    data = response.json()
                    break
                except (httpx.RequestError, httpx.HTTPStatusError) as e:
                    if attempt == max_retries - 1:
                        logger.error(f"Failed to fetch initial page for {region}/{subject}: {e}")
                        raise
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 0.1)
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after {delay:.2f}s: {e}")
                    time.sleep(delay)
    
            last_page = int(data.get('total_pages', 1))
            results.extend(data.get('items', []))
            logger.info(f"Found {last_page} pages for {region}/{subject}")
    
            # Scrape additional pages if needed
            if last_page > 1:
                paged_url = base_url + "&page=%i"
                for page in range(2, last_page + 1):
                    for attempt in range(max_retries):
                        try:
                            response = client.get(paged_url % (subject, region, page))
                            response.raise_for_status()
                            data = response.json()
                            results.extend(data.get('items', []))
                            logger.info(f"Scraped page {page}/{last_page} for {region}/{subject}")
                            break
                        except (httpx.RequestError, httpx.HTTPStatusError) as e:
                            if attempt == max_retries - 1:
                                logger.error(f"Failed to fetch page {page} for {region}/{subject}: {e}")
                                raise
                            delay = base_delay * (2 ** attempt) + random.uniform(0, 0.1)
                            logger.warning(f"Retry {attempt + 1}/{max_retries} for page {page}: {e}")
                            time.sleep(delay)
                    time.sleep(random.uniform(2, 4))  # Polite delay between pages
    
    except Exception as e:
        logger.error(f"Scraping failed for {region}/{subject}: {e}")
        raise
    
    df = pd.DataFrame(results)
    logger.info(f"Collected {len(df)} records for {region}/{subject}")
    return df

def main():
    """Main function to run the scraper."""
    parser = argparse.ArgumentParser(
        description='A web crawler to crawl Best Global University Rankings from US News website',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '-r', '--region',
        choices=VALID_REGIONS,
        default='africa',
        help=f'Select region: {", ".join(VALID_REGIONS)}'
    )
    parser.add_argument(
        '-s', '--subject',
        choices=VALID_SUBJECTS,
        default='agricultural-sciences',
        help=f'Select subject: {", ".join(VALID_SUBJECTS)}'
    )
    parser.add_argument(
        '-o', '--output-dir',
        default='.',
        help='Output directory for CSV file (default: current directory)'
    )

    args = parser.parse_args()

    try:
        # Scrape data
        df = scrape(args.region, args.subject)
        
        # Save to CSV
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{args.region}_{args.subject}.csv"
        df.to_csv(output_file, encoding='utf-8-sig', index=False)
        logger.info(f"Saved results to {output_file}")
        
    except Exception as e:
        logger.error(f"Program failed: {e}")
        raise SystemExit(1)

if __name__ == '__main__':
    main()