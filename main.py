from bs4 import BeautifulSoup
import requests

protocal = 'https'
domain_name = 'kmweb.moa.gov.tw'
seasons = ['春季', '夏季', '秋季', '冬季']

def URL_parser(protocal, domain_name, file_path):
  return protocal + '://' + domain_name + '/' + file_path

def get_products(class_name='deepcolor'):
  products = []
  for i in range(4, 5):
    file_path = 'theme_list.php?theme=production_map&season=S' + str(i)
    URL = URL_parser(protocal, domain_name, file_path)
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'lxml')
    product_div_tags = soup.find('div', class_=class_name)
    product_a_tags = product_div_tags.find_all('a', class_='item')
    for product_a_tag in product_a_tags:
      product = {'產季': seasons[i - 1]}
      response = requests.get(URL_parser(protocal, domain_name, product_a_tag['href']))
      soup = BeautifulSoup(response.text, 'lxml')
      product['產名'] = soup.find('h2', class_='articleTitle').text
      td_tags = soup.find_all('td', class_='td')
      product['產期'] = list(map(lambda x: x[:-1], td_tags[0].text.split('，')))
      product['產地'] = td_tags[1].text
      products.append(product)
  return products

# for product in get_products():
#   print(product)
# print('=' * 100)
for product in get_products('bluecolor'):
  print(product)