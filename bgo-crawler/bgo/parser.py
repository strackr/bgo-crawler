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

        self.driver = webdriver.Firefox()
        self.wait = ui.WebDriverWait(self.driver, 10)

    def __del__(self):
        self.driver.close()
    
    def extract_logs(self):
        self.__login()
         
        page_ids = self.__extract_page_ids()
        
        entries = []        
        for page_id in page_ids:
            entries += self.extract_logs_from_page(page_id)
        
        entries.reverse()
        return entries

    def extract_logs_from_page(self, page_id):
        self.driver.get(self.game_url.format(self.game, page_id))
        self.__wait_for_page_load()
        
        pattern = '<tr>' \
                '<td class="ligneJournalC"><p class="texte">(.+?)</p></td>' \
                '<td class="ligneJournalC"><p style="color:\w+;" class="texte">(.+?)</p></td>' \
                '<td class="ligneJournalC"><p class="texte">(\w+)</p></td>' \
                '<td class="ligneJournalC"><p class="texte">(\d+)</p></td>' \
                '<td class="ligneJournal"><p class="titre3">(.+?)</p><p class="texte">(.*?)</p></td>' \
                '</tr>'
        return re.findall(pattern, self.driver.page_source, re.DOTALL)

    def __login(self):
        self.driver.get(self.login_url)
        elem = self.driver.find_element_by_id('identifiant')
        elem.send_keys(self.user)
        elem = self.driver.find_element_by_id('mot_de_passe')
        elem.send_keys(self.password)
        elem.send_keys(Keys.RETURN)
        
        self.__wait_for_page_load()

    def __extract_page_ids(self):
        self.driver.get(self.game_url.format(self.game, 1))
        self.__wait_for_page_load()
        
        return sorted(set([u'1'] + re.findall(r'&amp;pg=(\d+)&amp;', self.driver.page_source)), key=lambda x:int(x))

    def __wait_for_page_load(self):
        return self.wait.until(lambda driver:driver.find_element_by_id('contenu'))
