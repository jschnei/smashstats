import bs4
import sys
import urllib2

def scrape_url(url):
    html = urllib2.urlopen(url).read()
    soup = bs4.BeautifulSoup(html)

    tds = [td for td in soup.find_all('td') if 'match' in td.get('id','')]
    
    def get_wl(td):
        halves = [td.find('div', 'match_top_half'), td.find('div', 'match_bottom_half')]
        players = [half.find('div','inner_content').get_text().strip() for half in halves]
        winners = [(not half.find('div', 'winner') is None) for half in halves]
        if (None in players) or set(winners)!=set([True, False]):
           return 
    
        edge = dict(zip(winners, players))
        return (edge[True], edge[False])
    
    wls = [get_wl(td) for td in tds]
    wls = [wl for wl in wls if wl]
    return wls
    
if __name__ == "__main__":
#    url = 'http://princetonsmash.challonge.com/princetonweekly2'
    print scrape_url(sys.argv[1])