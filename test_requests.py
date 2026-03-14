"""
https://www.wildberries.ru/__internal/u-search/exactmatch/ru/common/v18/search?ab_testing=false&appType=1&curr=rub&dest=-5818883&hide_vflags=4294967296&inheritFilters=false&lang=ru&query="запрос"&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false

https://www.wildberries.ru/__internal/u-search/exactmatch/ru/common/v18/search?ab_testing=false&appType=1&curr=rub&dest=-5818883&hide_vflags=4294967296&lang=ru&page=1&query=пальто из натуральной шерсти&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false

https://www.wildberries.ru/__internal/u-card/cards/v4/detail?appType=1&curr=rub&dest=-5818883&spp=30&hide_vflags=4294967296&ab_testing=false&lang=ru&nm=247002588;444458690;245472202

"""

from DrissionPage import ChromiumPage, ChromiumOptions
import json

# 1. Создаем настройки и включаем режим "без окна"
options = ChromiumOptions()
options.headless(True)  # Это скроет окно браузера

# 2. Передаем настройки в объект страницы
page = ChromiumPage(addr_or_opts=options)

url = "https://www.wildberries.ru/__internal/u-search/exactmatch/ru/common/v18/search?ab_testing=false&appType=1&curr=rub&dest=-5818883&hide_vflags=4294967296&lang=ru&page=1&query=пальто из натуральной шерсти&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false"

try:
    page.get(url)

    items = page.json["products"]

    for item in items:
        print(item)
        break
    
    
finally:
    page.quit()