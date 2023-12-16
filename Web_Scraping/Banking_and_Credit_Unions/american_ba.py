from bs4 import BeautifulSoup
import requests
import json

website = 'https://www.cuna.org/events.html?r=1&sortBy=date&t=business-areas%3Acuna-org%2Fcompliance---risk'
result = requests.get(website)
content = result.text

soup = BeautifulSoup(content, 'lxml')

card_contents = soup.find_all('div', class_='search-card')


#Get titles
titles = soup.find_all('h4', class_= 'search-card__title')
for title in titles: 
    print(title.get_text())

"""
result_list = []
for card_content in card_contents:

    category = card_content.find('p', class_ = 'search-card__content').get_text()
    title = card_content.find('h4', class_='search-card__content').get_text()
    desc = card_content.find('div', class_='txt search-card__description').get_text()
    link = card_content.get("href")

    result_list.append({'category': category, 'title': title, 'desc': desc, 'link': link})

print(result_list)

"""

"""

# Initialize an empty list to store the results
result_list = []

# Loop through each result 
for result in results:
    # Extract information
    category = result.find('p', class_='txt txt--eyebrow').span.get_text(strip=True)
    title = result.find('h4', class_='search-card__title').get_text(strip=True)
    desc = result.find('div', class_='txt search-card__description').get_text(strip=True)
    link = result.find('a', class_='search-card__link link link--arrow')['href']

    # Create a dictionary and append to the result list
    result_list.append({'category': category, 'title': title, 'link': link, 'description': desc})

# Print or use the result_list as needed
print(result_list)


# Save the result to a JSON file
#with open('investopedia.json', 'w') as json_file:
#    json.dump(result_list, json_file, indent=2)

"""

