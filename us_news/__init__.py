import httpx
import argparse
import pandas as pd
import random
import time

def scrape(region, subject):
    base_url = "https://www.usnews.com/education/best-global-universities/search?region=%s&subject=%s&format=json"

    r = httpx.get(base_url%(region, subject)).json()

    last_page = r.get('pagination')['last_page']

    if last_page == '1':
        results = r.get('results')
    else:
        base_url = 'https://www.usnews.com/education/best-global-universities/search?region=%s&subject=%s&page=%i&format=json'

        results = []

        results += r.get('results')

        for p in range(2, int(last_page)+1):
            
            r = httpx.get(base_url%(region, subject, p)).json()

            results += r.get('results')

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




