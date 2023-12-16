from bs4 import BeautifulSoup
import requests
import json

website = 'https://www.khanacademy.org/economics-finance-domain/core-finance/interest-tutorial'
result = requests.get(website)
content = result.text

soup = BeautifulSoup(content, 'lxml')
#print(soup.prettify())

box_all = soup.find_all('div', class_='_1lwwhwr')

'''
boxes = {}
links = {}
for box in box_all:
    boxes['title'] = box.find('h2', class_= '_v5zh60p').get_text()
    anchor_tags = box.find_all('a')
    for anchor in anchor_tags:
        boxes['links'] = "https://www.khanacademy.org" + anchor.get("href")
#print(boxes)
'''

result = [
    {'title': box.find('h2', class_='_v5zh60p').get_text(),
     'links': ["https://www.khanacademy.org" + anchor.get("href") for anchor in box.find_all('a')]}
    for box in box_all
]

print(result)

# Save the result to a JSON file
with open('khanacademy.json', 'w') as json_file:
    json.dump(result, json_file, indent=2)

#Get titles
#titles = box_all.find_all('h2', class_= '_v5zh60p')
#for title in titles: 
   #print(title.get_text())

#Get video links
#anchor_tags = box.find_all('a')
#for anchor in anchor_tags: 
    #print("https://www.khanacademy.org" + anchor.get("href"))