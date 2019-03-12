import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
import string
#doc thu muc
mypath = "20_newsgroups"
folders = [f for f in listdir(mypath)]
#print(folders)
#tao danh sach luu lai cac tep
file = []

for folder_name in folders:
    folder_path = join(mypath, folder_name)
    file.append([f for f in listdir(folder_path)])

#print(sum(len(file[i]) for i in range(20)))

pathname_list = []
for fo in range(len(folders)):
    for fi in file[fo]:
        pathname_list.append(mypath+"\\"+folders[fo]+"\\"+fi)

#print(len(pathname_list))


def preprocess(words):
   # dua ve dang chu thuong
   words = [word.lower() for word in words]

   # xoa cac so va cac ki tu dac biet
   table = str.maketrans('', '', '\t')
   words = [word.translate(table) for word in words]
   punctuations = (string.punctuation).replace("'", "")
   trans_table = str.maketrans('', '', punctuations)
   stripped_words = [word.translate(trans_table) for word in words]
   words = [str for str in stripped_words if str]
   p_words = []
   for word in words:
        if (word[0] and word[len(word)-1] == "'"):
            word = word[1:len(word)-1]
        elif(word[0] == "'"):
            word = word[1:len(word)]
        else:
            word = word
        p_words.append(word)

   words = p_words.copy()

   table = str.maketrans('', '', '0123456789')
   words = [word.translate(table) for word in words]

   words = [str for str in words if str]
   #xoa cac tu co do dai < 2
   words = [word for word in words if len(word) > 2]

   return words

# nap cac tu stopword


fi = open("stopwords.txt", "r")
if fi.mode == 'r':
    stopwords = []
    data = fi.readlines()
    for line in data:
      stopwords.append(line)
fi.close()

# ham xoa cac tu co trong stopword


def remove_stopwords(words):
    p_words = []
    rem = 0
    tu = 'all'
    for word in words:
        for tu in stopwords:

          if word.strip() == tu.strip():
              rem = 1
        if rem != 1:
          p_words.append(word)
        rem = 0
    words = p_words.copy()
    return words


def sentence(line):
  words = line[0:len(line)].strip().split(" ")
  words = preprocess(words)
  words = remove_stopwords(words)
  return words


def remove_metadata(lines):
    for i in range(len(lines)):
        if(lines[i] == '\n'):
            start = i+1
            break
    new_lines = lines[start:]
    return new_lines


def tokenize(path):
    f = open(path, "r")
    text_lines = f.readlines()

    text_lines = remove_metadata(text_lines)

    doc_words = []

    for line in text_lines:
        words = sentence(line)
        doc_words.append(words)

    return doc_words


def flatten(list):
    new_list = []
    for i in list:
        for j in i:
            new_list.append(j)
    return new_list


count = 0
list_of_words = []
print(len(pathname_list))
vo = open("vocabulary.txt", "w+")
for doc in pathname_list:
    count = count + 1
    list_of_words.append(flatten(tokenize(doc)))
    for lo in flatten(tokenize(doc)):
        vo.write(lo+'\n')
    if count == 20000:
        break

vo.close()
