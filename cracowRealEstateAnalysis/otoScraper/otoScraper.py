from bs4 import BeautifulSoup
import requests
import re

class OtoScraper:

    page_url_template="https://www.otodom.pl/sprzedaz/mieszkanie/krakow/?search%5Bfilter_float_m%3Afrom%5D=25&search%5Bregion_id%5D=6&search%5Bcity_id%5D=38&search%5Bpaidads_listing%5D=1&nrAdsPerPage=72&page={}"
    
    def get_all_offer_links(self, n):
        pageId = 1
        offerLinks = []
        
        response = requests.get(self.page_url_template.format(pageId))
        
        while response.status_code == 200 and pageId<n:
            offerLinks += self.get_page_offer_links(response)
            pageId+=1
            response = requests.get(self.page_url_template.format(pageId))
            
        print(len(offerLinks))
        print(len(set(offerLinks)))
    
    
    def get_page_offer_links(self, httpResponse):
        html_soup = BeautifulSoup(httpResponse.content, 'html.parser')
        offerSections = html_soup.find_all(attrs={"data-url" : re.compile(r".*")})
        links = self.get_links_from_articles(offerSections)
        print(links)
        return links 
        
    
    def get_links_from_articles(self, offerSections):
        links = []
        for offer in offerSections:
            links.append(offer['data-url'])
        return links
    
    def get_data_from_offer_links(self, offerLinks):
        for link in offerLinks:
            response = requests.get(link)
            html_soup = BeautifulSoup(response.content, 'html.parser')
            print(html_soup)
            
    
if __name__ == "__main__":
    otoScraper = OtoScraper()
    links = otoScraper.get_all_offer_links(4)
    otoScraper.get_data_from_offer_links(links)
