
import os

def get_keywords():
    with open('../res/keywords.txt', 'r', encoding='UTF-8') as f1:
        keywords = f1.readlines()
    for i in range(0, len(keywords)):
        keywords[i] = keywords[i].rstrip('\n')
    return keywords

if __name__ == '__main__':
    keywords = get_keywords()
    for query_word in keywords:
        os.system("scrapy crawl weixin -a category=" + query_word)