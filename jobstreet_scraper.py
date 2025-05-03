import requests
from playwright.sync_api import sync_playwright
import json
from datetime import datetime

def scrape_jobstreet():
    
    url = "https://ph.jobstreet.com/jobs-in-information-communication-technology?daterange=1"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Set user agent and other headers
        page.set_extra_http_headers({
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9,fil;q=0.8",
            "dnt": "1"
        })
        
        try:
            page.goto(url, timeout=60000)
            html = page.content()
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find the script tag containing job data (similar to sample data structure)
            script_tag = soup.find('script', {'data-automation': 'server-state'})
            if not script_tag:
                print("No job data found on page")
                browser.close()
                return None
                
            # Parse the JSON data from the script tag
            data = json.loads(script_tag.string)
        
            # Extract job listings (similar to sample structure)
            jobs = []
            for job in data.get('window', {}).get('SEEK_REDUX_DATA', {}).get('results', {}).get('results', {}).get('jobs', []):
                job_data = {
                    'id': job.get('id'),
                    'title': job.get('title'),
                    'company': job.get('companyName'),
                    'locations': [loc.get('label') for loc in job.get('locations', [])],
                    'listingDate': job.get('listingDate'),
                    'listingDateDisplay': job.get('listingDateDisplay'),
                    'salary': job.get('salaryLabel'),
                    'workTypes': job.get('workTypes', []),
                    'workArrangement': job.get('workArrangements', {}).get('displayText'),
                    'classification': job.get('classifications', [{}])[0].get('classification', {}).get('description'),
                    'subclassification': job.get('classifications', [{}])[0].get('subclassification', {}).get('description'),
                    'teaser': job.get('teaser'),
                    'tags': [tag.get('label') for tag in job.get('tags', [])]
                }
                jobs.append(job_data)
                
            return {
                'scraped_at': datetime.now().isoformat(),
                'total_jobs': len(jobs),
                'jobs': jobs
            }
            
        except Exception as e:
            print(f"Error scraping job listings: {str(e)}")
            browser.close()
            return None
        finally:
            browser.close()

if __name__ == "__main__":
    results = scrape_jobstreet()
    if results:
        with open('jobstreet_jobs.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Successfully scraped {results['total_jobs']} jobs. Saved to jobstreet_jobs.json")