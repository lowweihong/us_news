import httpx
import argparse
import pandas as pd
import random
import time
from typing import List, Dict
import logging
from pathlib import Path
from lxml import html
import re
from .constant import *

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def scrape_usnews(region: str, subject: str, max_retries: int = 3, base_delay: float = 2.0) -> pd.DataFrame:
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
    base_url = "https://www.usnews.com/education/best-global-universities/%s?format=json&region=%s"
    results: List[Dict] = []
    
    # Initial request to get total pages
    try:
        with httpx.Client(headers=HEADERS['usnews'], timeout=10.0) as client:
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

def scrape_times(subject: str, max_retries: int = 3, base_delay: float = 2.0, year: int = 2025) -> pd.DataFrame:
    """
    Scrape university rankings data from Times Higher Education (THE) for a given region and subject.
    
    Args:
        year: year in int
        subject: The subject to scrape data for.
        max_retries: Maximum number of retry attempts for failed requests.
        base_delay: Base delay for exponential backoff in seconds.
    
    Returns:
        A pandas DataFrame containing the scraped data.
    """
    # Placeholder URL; update based on actual THE URL structure
    base_url = "https://www.timeshighereducation.com/world-university-rankings/%i/subject-ranking/%s" % (year, subject)
    results: List[Dict] = []

    try:
         with httpx.Client(headers=HEADERS['times'], timeout=10.0) as client:
           
            for attempt in range(max_retries):
                try:
                    response = client.get(base_url)
                    response.raise_for_status()
                    tree = html.fromstring(response.text)
                    pattern = r'"ajax":\{"cache":true,"url":"(.*)","data'
                    
                    url = re.findall(pattern, tree.xpath("//script[@type='text/javascript' and contains(text(), 'pathPrefix')]")[0].text)[0].replace('\/', '/')
                    
                    logger.info(f"Obtained url for subject: {subject} (Times)")
                    response = client.get(url)
                    response.raise_for_status()
                    results = response.json()
                    break
                except (httpx.RequestError, httpx.HTTPStatusError) as e:
                    if attempt == max_retries - 1:
                        logger.error(f"Failed to fetch page {page} for {subject} (TIME): {e}")
                        raise
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 0.1)
                    logger.warning(f"Retry {attempt + 1}/{max_retries} for page {page}: {e}")
                    time.sleep(delay)
    
    except Exception as e:
        logger.error(f"Scraping failed for {subject} (Times): {e}")
        raise

    df = pd.DataFrame(results['data'])
    logger.info(f"Collected {len(df)} records for {subject} (Times)")
        
    return df

def scrape_qs(subject: str, max_retries: int = 3, base_delay: float = 2.0) -> pd.DataFrame:
    """
    Scrape university rankings data from QS World University Rankings for a given subject.
    
    Args:
        subject: The subject to scrape data for.
        max_retries: Maximum number of retry attempts for failed requests.
        base_delay: Base delay for exponential backoff in seconds.
    
    Returns:
        A pandas DataFrame containing the scraped data.
    """
    
    base_url = "https://www.topuniversities.com/university-subject-rankings/%s"
    results: List[Dict] = []
     
    # Initial request to get total pages
    try:
        with httpx.Client(headers=HEADERS['qs'], timeout=10.0) as client:
            for attempt in range(max_retries):
                try:
                    response = client.get(base_url % (subject))
                    response.raise_for_status()
                    tree = html.fromstring(response.text)
                    nid = tree.xpath("//article[contains(@about, '/university-subject-rankings')]/@data-history-node-id")[0]
                    paged_url = 'https://www.topuniversities.com/rankings/endpoint?nid=%s&page=%i&items_per_page=30&tab=indicators&region=&countries=&cities=&search=&star=&sort_by=&order_by=&program_type=&scholarship=&fee=&english_score=&academic_score=&mix_student=&loggedincache='
                    response = client.get(paged_url % (nid, 1))
                    response.raise_for_status()
                    data = response.json()
                    break
                except (httpx.RequestError, httpx.HTTPStatusError) as e:
                    if attempt == max_retries - 1:
                        logger.error(f"Failed to fetch initial page for {subject}: {e}")
                        raise
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 0.1)
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after {delay:.2f}s: {e}")
                    time.sleep(delay)
    
            last_page = int(data.get('total_pages', 1))
            results.extend(data.get('score_nodes', []))
            logger.info(f"Found {last_page} pages for {subject}")
    
            # Scrape additional pages if needed
            if last_page > 1:
                for page in range(2, last_page + 1):
                    for attempt in range(max_retries):
                        try:
                            response = client.get(paged_url % (nid, page))
                            response.raise_for_status()
                            data = response.json()
                            results.extend(data.get('score_nodes', []))
                            logger.info(f"Scraped page {page}/{last_page} for {subject}")
                            break
                        except (httpx.RequestError, httpx.HTTPStatusError) as e:
                            if attempt == max_retries - 1:
                                logger.error(f"Failed to fetch page {page} for {subject}: {e}")
                                raise
                            delay = base_delay * (2 ** attempt) + random.uniform(0, 0.1)
                            logger.warning(f"Retry {attempt + 1}/{max_retries} for page {page}: {e}")
                            time.sleep(delay)
                    time.sleep(random.uniform(2, 4))  # Polite delay between pages
    
    except Exception as e:
        logger.error(f"Scraping failed for {subject}: {e}")
        raise
    
    df = pd.DataFrame(results)
    logger.info(f"Collected {len(df)} records for {subject}")
    return df



def main():
    """
    Main function to run the university rankings scraper.

    Supports scraping from US News, THE, and QS websites by region and subject.
    Valid regions and subjects for each source are defined above.
    """
    parser = argparse.ArgumentParser(
        description='A web crawler to scrape university rankings from US News, Times, and QS websites',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '-r', '--region',
        required=False,
        default='',
        help='Select region (see REGIONS in this file for valid regions per source). Ignored for Times Higher Education and QS'
    )
    parser.add_argument(
        '-sub', '--subject',
        default='agricultural-sciences',
        help='Select subject (see SUBJECTS in this file for valid subjects per source)'
    )
    parser.add_argument(
        '-w', '--website',
        choices=VALID_SOURCES,
        default='usnews',
        help=f'Select source: {", ".join(VALID_SOURCES[:-1])}'
    )
    parser.add_argument(
        '-o', '--output-dir',
        default='.',
        help='Output directory for CSV files (default: current directory)'
    )

    args = parser.parse_args()

    try:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Select scraping functions based on source
        scrape_funcs = {
            'usnews': scrape_usnews,
            'times': scrape_times,
            'qs': scrape_qs
        }
        
        logger.info(f"Starting scrape for {args.website}/{args.region}/{args.subject}")

        if (args.website in ['times', 'qs']) and (args.region!=''):
            raise ValueError("Region parameter is not supported for Times Higher Education or QS. Omit the --region argument.")

        if args.subject not in SUBJECTS[args.website]:
            raise ValueError(f"Subject '{args.subject}' is not supported for {args.website}. Valid subjects: {', '.join(SUBJECTS[args.website])}")

        df = scrape_funcs[args.website](args.region, args.subject) if args.website == 'usnews' else scrape_funcs[args.website](args.subject)
        
        # Save to CSV
        file_str = f'{args.website}_{args.region}_{args.subject}'
        if not df.empty:
            output_file = output_dir / f"{file_str}.csv"
            df.to_csv(output_file, encoding='utf-8-sig', index=False)
            logger.info(f"Saved results to {output_file}")
        else:
            logger.warning(f"No data collected for {file_str}")
        
    except Exception as e:
        logger.error(f"Program failed: {e}")
        raise SystemExit(1)

if __name__ == '__main__':
    main()