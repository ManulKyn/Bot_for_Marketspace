import requests
from bs4 import BeautifulSoup as BS

# URL = 'https://www.citilink.ru/product/videokarta-asus-pci-e-4-0-rog-strix-rtx3060-o12g-v2-gaming-lhr-nv-rtx3-1548317/'
# URL = 'https://www.citilink.ru/product/videokarta-msi-pci-e-4-0-rtx-3070-ti-ventus-3x-8g-oc-ru-nv-rtx3070ti-8-1625374/'


def get_data(url):
    try:
        page = requests.get(url)
        if page.status_code == 404:
            raise NameError('Странница не найдена')
        else:
            soup = BS(page.content, "html.parser")
            Name = soup.select("h1.Heading.Heading_level_1.ProductHeader__title")
            Price = soup.select("span.ProductHeader__price-default_current-price")
            Available = soup.select("h2.ProductHeader__not-available-header")

            goods_name = " ".join(Name[0].text.split())
            goods_price = " ".join(Price[0].text.split())
            # goods_available = " ".join(Available[0].text.split())
            goods_info = {'goods_name': goods_name, 'goods_price': goods_price}

            return goods_info

    except IndexError:
        return 'Ничего не найдено'



