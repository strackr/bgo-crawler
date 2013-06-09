from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import selenium.webdriver.support.ui as ui


class LogParser:
    
    login_url = 'http://www.boardgaming-online.com/'
    game_url = 'http://www.boardgaming-online.com/index.php?cnt=52&pl={}&pg={}'
    
    def __init__(self, user, password, game):
        self.user = user
        self.password = password
        self.game = game
    
    def extract_logs(self):
        driver = webdriver.Firefox()
        wait = ui.WebDriverWait(driver, 10)
         
        driver.get(self.login_url)
        elem = driver.find_element_by_id('identifiant')
        elem.send_keys(self.user)
        elem = driver.find_element_by_id('mot_de_passe')
        elem.send_keys(self.password)
        elem.send_keys(Keys.RETURN)
        wait.until(lambda driver: driver.find_element_by_id('contenu'))
         
        driver.get(self.game_url.format(self.game, 1))
        wait.until(lambda driver: driver.find_element_by_id('contenu'))
         
        pages = sorted(set([u'1'] + re.findall(r'&amp;pg=(\d+)&amp;', driver.page_source)), key=lambda x: int(x))
        entries = []        
        for page in pages:
            entries += self.extract_page_logs(driver, page)
        
        driver.close()
        entries.reverse()
        return entries

    def extract_page_logs(self, driver, page_id):
        driver.get(self.game_url.format(self.game, page_id))
        
        pattern = '<tr>' \
                '<td class="ligneJournalC"><p class="texte">(.+?)</p></td>' \
                '<td class="ligneJournalC"><p style="color:\w+;" class="texte">(.+?)</p></td>' \
                '<td class="ligneJournalC"><p class="texte">(\w+)</p></td>' \
                '<td class="ligneJournalC"><p class="texte">(\d+)</p></td>' \
                '<td class="ligneJournal"><p class="titre3">(.+?)</p><p class="texte">(.*?)</p></td>' \
                '</tr>'
        return re.findall(pattern, driver.page_source, re.DOTALL)
