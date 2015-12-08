import re
import random
import operator
from nltk import pos_tag, word_tokenize

#chorus???
#rhymme???
#title???

prior_probs_dict = {} #number of occurrences for each prior prior probability pair
total_pos = {} #total number of occurrences for each pos
pos_dict = {} #dict of dicts that contains each part of speech, the words that make up those parts of speech, and number of each occurrence for each word
word_dict = {} #dictionary of words and occurrences of each corresponding pos
subsequent_dict = {} #dictionary of probabilities. showcases the likelihood of a given pos following another pos
count = 0
pos_count = 0
pos_count_2 = 0

def main():
  #use nltk to determine parts of speech for old songs, write to "oldsong.pos"
  pos_lyrics("oldsong.txt")

  input_file = open("oldsong.pos", "r")
  text = input_file.read()
  line = text.split()

  #establish the probabilites in "oldsong.pos"
  probabilities(line)
  #add each word in lyrics lyrics to a list
  the_song = lyrics()
  print_lyrics(the_song) #you know what to do

def pos_lyrics(input_file):
  f_read = open(input_file, "r")
  f_write = open("oldsong.pos", "w")
  text = f_read.read()
  list_of_pos = pos_tag(word_tokenize(text))
  for word in list_of_pos:
      f_write.write(word[0] + "  " + word[1] + "\n")
  f_read.close()
  f_write.close()

def probabilities(line):
  pos_count = 0
  pos_count_2 = 0
  hmm_count = 0
  count = 0
  #find prior probabilities and add to a dictionary
  for word in range(len(line)/2-1):
    word = line[count + 1] + " "
    following_word = line[count + 3] + " "
    word_combo = word + "-> " + following_word
    # check if word_combo exists in prior_probs_dict dictionary
    if word_combo in prior_probs_dict:
      #add to count
      prior_probs_dict[word_combo] += 1
    else:
      #create key and add to count
      prior_probs_dict[word_combo] = 1
    count += 2
    if len(line) == count:
      count = 0
      break

  #find total number of occurrences for each pos
  for word in range(len(line)/2-1):
    #total up each pos in total_pos dictionary
    pos = line[pos_count +1] + " "
    if pos in total_pos:
      total_pos[pos] += 1
    else:
      total_pos[pos] = 1
    pos_count += 2

  for pos in total_pos:
    subsequent_dict[pos] = {}
    for word_combo in prior_probs_dict:
        if word_combo.startswith(pos):
          #probability is the number of word_combos/total occurrences of pos
          occurrences_of_word_combo = prior_probs_dict[word_combo]
          occurrences_of_pos = total_pos[pos]
          probability = (occurrences_of_word_combo)/float(occurrences_of_pos)
          subsequent_dict[pos][word_combo] = probability

  #have a dictionary of dictionaries that contains each part of speech, the words that make up those parts of speech, and number of each occurrence for each word
  for word in range(len(line)):
    word = line[pos_count_2]
    pos = line[pos_count_2 +1]
    #check if pos exists in dictionary
    #POS DICT-------------------------------
    if pos in pos_dict:
        #check to see if word is already in nested dict. if not, add
        if word in pos_dict[pos]:
          pos_dict[pos][word] += 1
        else:
          pos_dict[pos][word] = 1
    else:
        #add that pos to the dict, add add word to nested dict
        pos_dict[pos] = {}
        pos_dict[pos][word] = 1
    #WORD DICT-------------------------------
    if word in word_dict:
        #check to see if word is already in nested dict. if not, add
        if pos in word_dict[word]:
          word_dict[word][pos] += 1
        else:
          word_dict[word][pos] = 1
    else:
        #add that pos to the dict, add add word to nested dict
        word_dict[word] = {}
        word_dict[word][pos] = 1
    pos_count_2 += 2
    if len(line) == pos_count_2:
      pos_count_2 = 0
      break
def lyrics():
  lyrics = []
  total_words = 0 #no more than 250 words/song
  count = 0
  #hardcode it so that first word is a noun, yolo
  for word in pos_dict:
    if word == "NN":
      count += 1
      for words in pos_dict[word]:
        #randomly pick some common Drake noun
        add_word = random.choice(pos_dict[word].keys())
        lyrics.append(add_word)
        if (count ==1):
          count = 0
          break
  while total_words != 250:
    pick = []
    #based on the first word, come up with the other words!
    
    #determine POS for current word
    current_word = lyrics[total_words]
    pos_of_current_word = max(word_dict[current_word].iteritems(), key=operator.itemgetter(1))[0] + " "
    
    #determine top two possible POS for subsequent word
    pos_options = dict(sorted(subsequent_dict[pos_of_current_word].iteritems(), key=operator.itemgetter(1), reverse=True)[:2])
    #pick one at random
    full_pos = random.choice(pos_options.keys())
    length_of_old_pos = len(pos_of_current_word) + 3
    pos_of_next_word = split(full_pos, length_of_old_pos)
    
    #generate a random word from the list of words for that given part of speech
    for word in pos_dict:
      if (word + " ") == pos_of_next_word:
        count += 1
        for words in pos_dict[word]:
          #randomly pick some common Drake word
          add_word = random.choice(pos_dict[word].keys())
          lyrics.append(add_word)
          if (count ==1):
            count = 0
            break
    total_words += 1
  return lyrics

def print_lyrics(lyrics):
  output = open("newsong.txt", "w")
  count = 0
  #hardcode title to be first three words
  title = lyrics[:3]
  #hardcode chorus to be next 50 words
  chorus = lyrics[3:53]
  #hardcode verses to be remaining
  verses = lyrics[53:]
  output.write("TITLE:")
  for words in title:
    output.write(words + " ")
  output.write("\n\n")
  print_chorus(chorus, output)
  for words in lyrics:
    output.write(words + " ")
    count += 1
    if count % 10 ==0:
      output.write("\n")
    elif count % 83 == 0:
      output.write("\n\n")
      print_chorus(chorus, output)
  output.close()


def print_chorus(words_in_chorus, output):
  count = 0
  output.write("CHORUS:")
  for words in words_in_chorus:
    output.write(words + " ")
    count += 1
    if count % 10 ==0:
      output.write("\n")

def split(s, n):
  return s[n:]

if __name__ == "__main__":
      main()
