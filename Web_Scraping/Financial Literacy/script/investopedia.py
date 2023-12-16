from bs4 import BeautifulSoup
import requests
import json

website = 'https://www.investopedia.com/personal-finance-4427760'
result = requests.get(website)
content = result.text

soup = BeautifulSoup(content, 'lxml')

card_contents = soup.find_all('div', class_='card__content')
anchor = soup.find_all('a', class_= 'comp mntl-card-list-items mntl-document-card mntl-card card card--no-image')

result_list = []
for card_content, anchor in zip(card_contents, anchor):

    category = card_content['data-tag']
    title = card_content.find('span', class_='card__title-text').get_text()
    author = card_content.find('div', class_='byline--simple__author').get_text()
    date = card_content.find('div', class_='displayed-date').get_text()[8:]
    link = anchor.get("href")
    # Create a dictionary and append to the result list
    result_list.append({'category': category, 'title': title, 'author': author, 'date': date, 'link': link})

#for a in anchor:
#    result_list.append({'links': [a.get("href")]})
    
# Print or use the result_list as needed
print(result_list)


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


# Save the result to a JSON file
#with open('investopedia.json', 'w') as json_file:
#    json.dump(result_list, json_file, indent=2)

#Get titles
#titles = box_all.find('span', class_= 'card__title-text')
#for title in titles: 
#   print(title.get_text())

#Get video links
#anchor_tags = box.find_all('a')
#for anchor in anchor_tags: 
    #print("https://www.khanacademy.org" + anchor.get("href"))


#comp mntl-card-list-items mntl-document-card mntl-card card card--no-image