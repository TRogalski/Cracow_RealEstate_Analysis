from bs4 import BeautifulSoup
import requests
import re

class OtoScraper:

    page_url_template="https://www.otodom.pl/sprzedaz/mieszkanie/krakow/?search%5Bfilter_float_m%3Afrom%5D=25&search%5Bregion_id%5D=6&search%5Bcity_id%5D=38&search%5Bpaidads_listing%5D=1&nrAdsPerPage=72&page={}"
    
    def get_all_offer_links(self, n):
        page_id = 1
        offer_links = []
        
        response = requests.get(self.page_url_template.format(page_id))
        
        while response.status_code == 200 and page_id<n:
            offer_links += self.get_page_offer_links(response)
            page_id+=1
            response = requests.get(self.page_url_template.format(page_id))
        return offer_links
    
    
    def get_page_offer_links(self, http_response):
        html_soup = BeautifulSoup(http_response.content, 'html.parser')
        offer_sections = html_soup.find_all(attrs={"data-url" : re.compile(r".*")})
        links = self.get_links_from_articles(offer_sections)
        return links 
        
    
    def get_links_from_articles(self, offer_sections):
        links = []
        for offer in offer_sections:
            links.append(offer['data-url'])
        return links
    
    
    def get_data_from_offer_links(self, offer_links):
        offer_data = {}
        for link in offer_links:
            response = requests.get(link)
            html_soup = BeautifulSoup(response.content, 'html.parser')
            offer_details_section = html_soup.find(class_ = "section-overview")
            details_list = offer_details_section.find_all('li')
            offer_data[link] = self.format_offer_details(details_list)
            print(offer_data)
    
    def format_offer_details(self, details_list):
        formatted_details = {}
        for detail in details_list:
            k, v = detail.text.split(':')
            formatted_details[k] = v
        return formatted_details
    
if __name__ == "__main__":
    otoScraper = OtoScraper()
    links = otoScraper.get_all_offer_links(4)
    otoScraper.get_data_from_offer_links(links)
