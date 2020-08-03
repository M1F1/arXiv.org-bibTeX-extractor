import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import json
import pyperclip
import collections

def replace_article_id_with_label(exported_citation, label):
    return re.sub(r'^(@ARTICLE{)(.*),', r'\1{},'.format(label), exported_citation)

if __name__ == "__main__":
    browser = webdriver.Firefox()
    browser.maximize_window()

    with open('urls.json') as f:
        urls = json.load(f)

    for label, data in urls.items():

        if data['bib_format'] == None:
            url1 = data['link']

            browser.get(url1)
            element = browser.find_element_by_link_text('NASA ADS')

            url2 = element.get_attribute('href')
            browser.get(url2)

            export_citation_element=browser.find_element_by_css_selector(
                "div#left-column > div:nth-child(1) > nav:nth-child(1) > a:nth-child(10)"
            )
            browser.execute_script("arguments[0].click();", export_citation_element)

            element = WebDriverWait(browser, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Copy to Clipboard')]"))
            ).click()

            bibtext = pyperclip.paste()
            replaced_bibtext_label = replace_article_id_with_label(bibtext, label)

            urls[label]['bib_format'] = replaced_bibtext_label

    od = collections.OrderedDict(sorted(urls.items()))

    with open('literature.bib', 'w') as f:
        for values in od.values():
            f.write("{}\n".format(values['bib_format']))

    with open('urls.json', 'w') as json_file:
        json.dump(od, json_file, indent=4)

