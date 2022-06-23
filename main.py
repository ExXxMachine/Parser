import requests
from bs4 import BeautifulSoup
import openpyxl
import os
req = requests.get("https://www.irisk.ru/catalog/")

book = openpyxl.Workbook()
sheet = book.active

name = input("Введите название файла: ")
stran = input("Введите номер страницы (all - все страницы ,раздел - меню парсинга раздела): ")
top_stran = ' '
if stran == "раздел":
    top_stran = input("Введите название верхнего раздела: ")
    stran = input("Введите название раздела: ")

pgn = BeautifulSoup(req.content, 'html.parser')
all_pagen = pgn.find_all(class_="bx-pagination-container")


pagen = ' '

cartname = []
price = []
art = []
nal = []
url_more = []
description = []
image_numder = 0

if stran == "all":
    if not os.path.isdir(str(stran) + "_images"):
        os.mkdir(str(stran) + "_images")
    for item in all_pagen:
        pagen = item.text.split("\n")
    for i in range (1,int(max(pagen))):
        print ("Страниц " + str(i) + " / " + str(max(pagen)))
        url = requests.get("https://www.irisk.ru/catalog/?PAGEN_1=" + str(i))

        soup = BeautifulSoup(url.content, 'html.parser')

        all_cartname = soup.find_all(class_="cartname")
        all_nal = soup.find_all(class_="art-brend")
        all_price = soup.find_all(class_="price-bt")
        all_art = soup.find_all(class_="art")

        t = "Ожидается"

        for item in all_cartname:
            cartname.append(item.text)
            url_more.append(item.select_one('a').get('href'))

        for item in all_price:
            price.append(item.text)

        for item in all_nal:
            if t in str(item):
                nal.append("Нет в наличии")
            else:
                nal.append("В наличии")

        for item in all_art:
            art.append(item.text)

        for item in url_more:
            url = requests.get("https://www.irisk.ru" + item).text
            new_soup = BeautifulSoup(url, 'html.parser')
            all_description = new_soup.find_all(class_="tovar_text")
            all_images_block = new_soup.find_all('div', class_='catalog_element_image')

            for image in all_images_block:
                image_link = image.find('a').get('href')

                image_bytes = requests.get(f'https://www.irisk.ru{image_link}').content
                with open(f'{str(stran)}_images/{image_numder}.jpg', 'wb') as file:
                    file.write(image_bytes)
                image_numder = image_numder + 1
            for i in all_description:
                description.append(i.text)
else:
    if stran.isdigit() == True:
            if not os.path.isdir("Стр " + str(stran) + "_images"):
                os.mkdir("Стр " + str(stran) + "_images")
            url = requests.get("https://www.irisk.ru/catalog/?PAGEN_1=" + str(stran))

            soup = BeautifulSoup(url.content, 'html.parser')

            all_cartname = soup.find_all(class_="cartname")
            all_nal = soup.find_all(class_="art-brend")
            all_price = soup.find_all(class_="price-bt")
            all_art = soup.find_all(class_="art")
            t = "Ожидается"
            for item in all_cartname:
                cartname.append(item.text)
                url_more.append(item.select_one('a').get('href'))

            for item in all_price:
                price.append(item.text)

            for item in all_nal:
                if t in str(item):
                    nal.append("Нет в наличии")
                else:
                    nal.append("В наличии")

            for item in all_art:
                art.append(item.text)
            for item in url_more:
                url = requests.get("https://www.irisk.ru" + item).text
                new_soup = BeautifulSoup(url, 'html.parser')
                all_description = new_soup.find_all(class_="tovar_text")
                all_images_block = new_soup.find_all('div',class_='catalog_element_image')

                for image in all_images_block:
                    image_link = image.find('a').get('href')

                    image_bytes = requests.get(f'https://www.irisk.ru{image_link}').content
                    with open(f'Стр {str(stran)}_images/{image_numder}.jpg','wb') as file:
                        file.write(image_bytes)
                    image_numder = image_numder + 1
                for i in all_description:
                    description.append(i.text)
    else:
            if not os.path.isdir(str(top_stran) + "_" + str(stran) + "_images"):
                os.mkdir(str(top_stran) + "_" + str(stran) + "_images")

            all_chapter = pgn.find_all(class_="sub-items")

            top_url = ''
            for item in all_chapter:
                if str(top_stran.lower()) in item.text.lower():
                    top_url = top_url + str(item)
            soup = BeautifulSoup(top_url, 'html.parser')
            chapter = soup.find_all('li')

            url2 =[]
            for item in chapter:
                if str(stran.lower()) in item.text.lower():
                    url2.append(item.select_one('a').get('href'))

            url = requests.get("https://www.irisk.ru" + str(url2[0]) + "?PAGEN_1=1")
            url_chapter = BeautifulSoup(url.content, 'html.parser')
            all_page = url_chapter.find_all(class_="bx-pagination-container")
            page = ''
            for item in all_page:
                page = item.text.split("\n")

            for i in range(1, int(max(page)) + 1):
                print("Страниц " + str(i) + " / " + str(max(page)))
                url = requests.get("https://www.irisk.ru" + str(url2[0]) + "?PAGEN_1=" + str(i))

                soup = BeautifulSoup(url.content, 'html.parser')

                all_cartname = soup.find_all(class_="cartname")
                all_nal = soup.find_all(class_="art-brend")
                all_price = soup.find_all(class_="price-bt")
                all_art = soup.find_all(class_="art")

                t = "Ожидается"

                for item in all_cartname:
                    cartname.append(item.text)
                    url_more.append(item.select_one('a').get('href'))

                for item in all_price:
                    price.append(item.text)

                for item in all_nal:
                    if t in str(item):
                        nal.append("Нет в наличии")
                    else:
                        nal.append("В наличии")

                for item in all_art:
                    art.append(item.text)

                for item in url_more:
                    url = requests.get("https://www.irisk.ru" + item)
                    new_soup = BeautifulSoup(url.content, 'html.parser')
                    all_description = new_soup.find_all(class_="tovar_text")
                    all_images_block = new_soup.find_all('div', class_='catalog_element_image')
                    all_images2 = new_soup.find(class_='product-img-trumbs MagicScroll MagicScroll-arrows-outside MagicScroll-horizontal')
                    all_images = all_images2.find_all("a")


                    image_link = []
                    print(all_images)
                    for image in all_images:
                        image_link.append(image.find('a').get('href'))

                    print(image_link)
                    for link in image_link:
                            image_bytes = requests.get(f'https://www.irisk.ru{link}').content
                            with open(f'{str(top_stran)}_{str(stran)}_images/{image_numder}.jpg', 'wb') as file:
                                file.write(image_bytes)
                            image_numder = image_numder + 1
                            for i in all_description:
                                description.append(i.text)



sheet['A1'] = "Товар"
sheet['B1'] = "Цена"
sheet['C1'] = "Артикул"
sheet['D1'] = "Наличие"
sheet['E1'] = "Описание"

for i in range (2,len(cartname) + 2):
    sheet['A' + str(i)] = cartname[i - 2]
    sheet['B' + str(i)] = price[i - 2].strip()
    sheet['C' + str(i)] = art[i - 2]
    sheet['D' + str(i)] = nal[i - 2]
    sheet['E' + str(i)] = description[i - 2]
    book.save(str(name) + ".xlsx")

print("Сompleted")

book.close()
