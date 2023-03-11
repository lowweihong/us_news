import httpx
import argparse
import pandas as pd
import random
import time

headers = {
    'authority': 'www.usnews.com',
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'referer': 'https://www.usnews.com/',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}


def scrape(region, subject):
               
    base_url = "https://www.usnews.com/education/best-global-universities/%s?format=json&region=%s"

    r = httpx.get(base_url%(subject, region), headers=headers).json()
    
    last_page = r.get('total_pages')

    if last_page == '1':
        results = r.get('items')
    else:
        base_url = "https://www.usnews.com/education/best-global-universities/%s?format=json&region=%s&page=%i"

        results = []

        results += r.get('items')

        for p in range(2, int(last_page)+1):
            
            r = httpx.get(base_url%(subject, region, p), headers=headers).json()

            results += r.get('items')

            time.sleep(random.randint(2,4))

    return pd.DataFrame(results)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A web crawler to crawl Best Global University Ranking on usnews website')
    parser.add_argument(
        '-r', '--region', help='Selecting regions {africa, asia, australia-new-zealand, europe, latin-america', default='africa')
    parser.add_argument(
        '-s', '--subject', help='''Selecting subjects {agricultural-sciences, 
                                arts-and-humanities, biology-biochemistry, 
                                cardiac-cardiovascular, chemistry, civil-engineering, 
                                clinical-medicine, computer-science, economics-business, 
                                electrical-electronic-engineering, engineering, environment-ecology, 
                                geosciences, immunology, materials-science, mathematics, 
                                mechanical-engineering, microbiology, molecular-biology-genetics, 
                                neuroscience-behavior, oncology, pharmacology-toxicology, physics, 
                                plant-animal-science, psychiatry-psychology, 
                                social-sciences-public-health, space-science, surgery''', 
                            default='agricultural-sciences')

    args = parser.parse_args()

    region, subject = args.region, args.subject

    final = scrape(region, subject)

    final.to_csv("%s_%s.csv"%(region, subject), encoding='utf-8-sig', index=False)




