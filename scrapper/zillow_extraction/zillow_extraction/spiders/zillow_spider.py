import scrapy
import json
import random

class ZillowSpider(scrapy.Spider):
    name = "zillow_spider"
    allowed_domains = ["zillow.com"]
    # url = "https://www.zillow.com/homes/New-york,-NY_rb/"
    url = "https://www.zillow.com/new-york-ny/10_p"
    # url = "https://www.zillow.com/homedetails/850-E-39th-St-1-Brooklyn-NY-11210/452245036_zpid/"
    
    page_count = 0
    max_pages = 10
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,  # Delay 2 detik antar request
        'RANDOMIZE_DOWNLOAD_DELAY': 0.5,  # Random delay 1.5-2.5 detik
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    }
    
    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse, meta={'page_number': 1})

    def parse(self, response):
        page_number = response.meta.get('page_number', 1)
        self.logger.info(f"Scraping page {page_number}")
        
        scripted_data = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        
        if not scripted_data:
            self.logger.error(f"No script data found on page {page_number}")
            return
        
        data_json = json.loads(scripted_data)
        search_results = data_json.get('props', {}).get('pageProps', {}).get('searchPageState', {}).get('cat1', {}).get('searchResults', {})
        list_homes = search_results.get('listResults', [])
        
        for home in list_homes:
            if not home.get('isUndisclosedAddress', True):
                # Safe access untuk nested data
                hdp_data = home.get('hdpData', {}).get('homeInfo', {})
                
                home_data = {
                    'page_number': page_number,
                    'zpid': home.get('zpid'),
                    'url': home.get('detailUrl'),
                    'imgHouse': home.get('imgSrc'),
                    'address': home.get('address'),
                    'price': home.get('price'),
                    'unformattedPrice': home.get('unformattedPrice'),
                    'latLong': home.get('latLong'),
                    'isHomeRecomendation': home.get('isHomeRec'),
                    'brokerName': home.get('brokerName'),
                    'homeType': hdp_data.get('homeType'),
                    'beds': home.get('beds'),
                    'baths': home.get('baths'),
                    'areas': home.get('area'),
                    'livingArea': hdp_data.get('livingArea'),
                    'taxAssessedValue': hdp_data.get('taxAssessedValue'),
                    'lotAreaValue': hdp_data.get('lotAreaValue'),
                    'lotAreaUnit': hdp_data.get('lotAreaUnit'),
                    'daysOnZillow': hdp_data.get('daysOnZillow'),
                    'zestimate': hdp_data.get('zestimate'),
                    'statusType': home.get('statusType'),
                    'homeStatus': hdp_data.get('homeStatus'),
                }
                yield home_data

        # Check for next page
        search_list = data_json.get('props', {}).get('pageProps', {}).get('searchPageState', {}).get('cat1', {}).get('searchList', {})
        pagination = search_list.get('pagination', {})
        next_url = pagination.get('nextUrl')
        
        self.logger.info(f"Next URL found: {next_url}")
        
        # Continue to next page if exists and within limit
        if next_url and page_number < self.max_pages:
            next_page_number = page_number + 1
            self.logger.info(f"Moving to page {next_page_number}")
            
            # Human behavior: random delay between pages
            delay = random.uniform(3, 7)  # Random delay 3-7 seconds
            self.logger.info(f"Waiting {delay:.2f} seconds before next page...")
            
            # Build full URL if relative
            if next_url.startswith('/'):
                next_full_url = 'https://www.zillow.com' + next_url
            else:
                next_full_url = next_url
                
            self.logger.info(f"Next full URL: {next_full_url}")
            
            # Make request dengan header dari settings + referer
            yield scrapy.Request(
                url=next_full_url,
                headers={'Referer': response.url},  # Hanya tambah referer
                callback=self.parse,
                meta={
                    'page_number': next_page_number,
                    'download_delay': delay
                },
                dont_filter=True
            )
        else:
            if page_number >= self.max_pages:
                self.logger.info(f"Reached maximum pages limit: {self.max_pages}")
            else:
                self.logger.info("No more pages available")