import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

productName = 'book'
page = 2    # 60 rows on page

if __name__ == '__main__':
    # getting webpage with params
    url = f'https://aliexpress.ru/wholesale?page={page}&SearchText={productName}'
    r = requests.get(url)

    # save html to file
    # with open('test.html', 'w', encoding='utf-8') as output_file:
    #    output_file.write(r.text)

    # creating parser instance and loading html to it form raw string
    soup = bs(r.text, features="html.parser")

    # getting all 60 rows with products
    divs = soup.find_all('div', {
        'class': 'SearchProductFeed_HorizontalCard__card__102el SearchProductFeed_Preview__card__3zxie'
    })
    # print(len(divs))  # must be == 60 (depends on aliexpress, but rn it is)

    # creating dataframe with data (name+price) of each product on page
    data = pd.DataFrame(columns=['name', 'price'])

    # filling it
    for d in divs:
        data = data.append({
            'name': d.find_all(
                'div',
                {'class': 'SearchProductFeed_HorizontalCard__info__102el'}
            )[0].find_all('a')[0].text,

            'price': float(d.find_all(
                'span',
                {'class': 'SearchProductFeed_Price__titleWrapper__p1hme'}
            )[0].text.encode('utf-8', 'ignore').decode("ascii", 'ignore').replace('.', '').replace(',', '.'))
        }, ignore_index=True)

    # printing data
    print(data.head())
