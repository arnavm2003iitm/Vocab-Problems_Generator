import csv
import numpy as np
import requests 
import json
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

ques_per_word = int(input("Number of problems per word: "))

problem_list = []
no_sentences = []
word_list = []
misspelled = []

# Fetch word definition

def fetch_definition(search_word):
    url = 'https://api.dictionaryapi.dev/api/v2/entries/en/' + search_word
    response = requests.get(url)

    json_data = json.loads(response.text)

    return json_data


# Fetch sentences and sort them according to votes 

def fetch_sentences(search_word):
    url = 'https://sentence.yourdictionary.com/' + search_word
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html')

    sentences_bs = soup.find_all('p', class_='sentence-item__text')
    votes_bs = soup.find_all('span', class_='votes__amount text-black text-xs font-semibold')

    votes_list = []
    for votes_html in votes_bs:
        votes = votes_html.text
        votes_list.append(int(votes)) 


    votep_list = []
    i = 0
    while(i < len(votes_list)):
        up_votes = votes_list[i]
        i += 1
        down_votes = votes_list[i]
        i += 1

        try:
            votep_list.append(up_votes/(up_votes + down_votes))
        except:
            votep_list.append(0)


    sentence_list = []
    for sentence_html in sentences_bs:
        sentence = sentence_html.text
        sentence_list.append(sentence)


    zipped_pairs = zip(votep_list, sentence_list)
    sentence_list_sorted = [pair for _, pair in sorted(zipped_pairs, reverse=True)]
    return sentence_list_sorted


# Load all the words

with open("words.csv", "r") as csv_file:
    file_contents = csv.reader(csv_file)
    
    for word in file_contents:
        word_list.append(word[0].strip())

file = open("Data/problems_created.txt", "r")
start = int(file.read())
file.close()

complete_word_list = word_list
word_list = word_list[start+1:]

file = open("Data/problems_created.txt", "w")
file.write(str(len(complete_word_list) - 1))
file.close()

print(word_list)
# print(complete_word_list)


for word in word_list:

    try:
        title = fetch_definition(word)['title']
    except:
        title = 'exists'
    
    if (title == 'No Definitions Found'):
        
        misspelled.append(word)
        continue

if (len(misspelled) != 0):
    print(misspelled)

# word_list = word_list[0:5]

for word in word_list:

    sentence_list = fetch_sentences(word)

    if (len(sentence_list) == 0):
        no_sentences.append(word)
    
    i = 0
    while(i < min(ques_per_word, len(sentence_list))):
        sentence = sentence_list[i]
        sentence = sentence.replace(word, '____')
        sentence = sentence.replace(word.capitalize(), '____')
        
        options = [word]
        while(word in options):
            options = random.sample(complete_word_list, 3)
        
        options.append(word)
        random.shuffle(options)

        problem_list.append([sentence, options[0], options[1], options[2], options[3], word])
        i += 1

random.shuffle(problem_list)        


with open('Data/problems.csv', 'a', newline='') as file:
    writer = csv.writer(file)

    for row in problem_list:
        writer.writerow(row)

if(len(no_sentences) != 0):
    print("No sentences found for words: ", no_sentences)

file = open("Data/no_sentence_words.txt", "a")

for i in range(len(no_sentences)):
    add_word = no_sentences[i]  + "\n"
    file.write(add_word)

file.close()