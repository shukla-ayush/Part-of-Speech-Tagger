from collections import Counter
import glob
import os
import fileinput
import re
import random
import operator
import collections

dict_word_tag = dict()
dict_tag_unigram = dict()
dict_words_for_tag = dict()
dict_tags_for_tag = dict()
dict_transition_probabilities = dict()
dict_emission_probabilities = dict()
dict_tag_bigram = dict()
lists_of_sentences = list()
random_sentence_list = list()
tag_list = list()
dict_words = dict()
pos_tagged_list = list()

path_of_training_file = input("Enter path of folder where training files are present - ")
path_of_test_file = input("Enter path of folder where test file is present - ")

def create_word_tag():
    for file in glob.glob(path_of_training_file + "/" + "*"):
        if file != 'FrequencyCounts.py':
            rf = open(file, "r")
            lines = rf.readlines()
            for l in lines:
                if l.strip():
                    newl = re.sub('  +', '', l)
                    newl2 = newl.replace('\t', '')
                    newl3 = newl2.replace('\n', '')
                    lists_of_sentences.append(newl3.split(" "))

    for list in lists_of_sentences:
        list.insert(0, "/start")
        list.insert(len(list), "/end")
        # print(list)
        for wordtag in list:
            if wordtag in dict_word_tag:
                dict_word_tag[wordtag] = dict_word_tag[wordtag] + 1
            else:
                dict_word_tag[wordtag] = 1

    x = ''
    if x in dict_word_tag:
        del dict_word_tag[x]
    print("word-tag created")


def replace_less_freq_with_unk():
    red_freq_list = list()
    for key, value in list(dict_word_tag.items()):
        if key.count('/') > 1:
            lastdelimiter = key.rfind('/')
            word = key[:lastdelimiter]
            tag = key[lastdelimiter+1:]
        else:
            word,tag = key.split("/")
        if word in dict_words:
            dict_words[word] += 1
        else:
            dict_words[word] = 1

    for key, value in dict_word_tag.items():
        if key.count('/') > 1:
            lastdelimiter = key.rfind('/')
            word = key[:lastdelimiter]
            tag = key[lastdelimiter+1:]
        else:
            word,tag = key.split("/")
        if dict_words[word] == 1:
            red_freq_list.append(key)
            if ("UNK/" + str(tag)) in dict_word_tag:
                 dict_word_tag["UNK/" + str(tag)] += 1
            else:
                dict_word_tag["UNK/" + str(tag)] = 1

    for k in red_freq_list:
        if k in dict_word_tag:
            del dict_word_tag[k]

    for key, value in list(dict_word_tag.items()):
        if key.count('/') > 1:
            lastdelimiter = key.rfind('/')
            word = key[:lastdelimiter]
            tag = key[lastdelimiter+1:]
        else:
            word,tag = key.split("/")
        if tag in dict_words_for_tag:
            dict_words_for_tag[tag].append(word)
        else:
            dict_words_for_tag[tag] = [word]


def create_tag_unigram():
    for list in lists_of_sentences:
        x = ''
        if x in list:
            list.remove(x)
        for wordtag in list:
            word = ""
            tag = ""
            index = 0
            if wordtag.count('/') > 1:
                lastdelimiter = wordtag.rfind('/')
                # word = wordtag[:lastdelimiter]
                tag = wordtag[lastdelimiter+1:]
            else:
                word,tag = wordtag.split("/")
            if tag in dict_tag_unigram:
                dict_tag_unigram[tag] = dict_tag_unigram[tag] + 1
            else:
                dict_tag_unigram[tag] = 1
    print("tag-unigram created and words for tag dict created")


def create_tag_bigram():
    for list in lists_of_sentences:
        for j in range(len(list) - 1):
            tag1 = ""
            tag2 = ""
            if list[j].count('/') > 1:
                x = str(list[j])
                lastdelimiter = x.rfind('/')
                tag1 = x[lastdelimiter+1:]
            else:
                word,tag1 = list[j].split("/")

            if list[j+1].count('/') > 1:
                x = str(list[j+1])
                lastdelimiter = x.rfind('/')
                tag2 = x[lastdelimiter+1:]
            else:
                word2,tag2 = list[j+1].split("/")

            bigram_tag = tag1+" "+tag2
            if tag1 in dict_tags_for_tag:
                dict_tags_for_tag[tag1].append(tag2)
            else:
                dict_tags_for_tag[tag1] = [tag2]
            if bigram_tag in dict_tag_bigram:
                dict_tag_bigram[bigram_tag] = dict_tag_bigram[bigram_tag] + 1
            else:
                dict_tag_bigram[bigram_tag] = 1
    print("tag-bigram created")


def find_transition_probability():
    tag_list = dict_tag_unigram.keys()
    for k1,v1 in dict_tag_unigram.items():
        for k2, v2 in dict_tag_unigram.items():
            bigram_tag = str(k1) + " " + str(k2)
            if bigram_tag in dict_tag_bigram:
                dict_transition_probabilities[bigram_tag] = float(dict_tag_bigram[bigram_tag] + 1)/float(dict_tag_unigram[k1] + len(tag_list))
            else:
                dict_transition_probabilities[bigram_tag] = 1.0/len(tag_list)


def find_emission_probability():
    tag_list = dict_tag_unigram.keys()
    for key, value in list(dict_word_tag.items()):
        # print(key, wordtag)
        if key.count('/') > 1:
            lastdelimiter = key.rfind('/')
            word = key[:lastdelimiter]
            tag = key[lastdelimiter+1:]
        else:
            word,tag = key.split("/")
        dict_emission_probabilities[str(key)] = float(dict_word_tag[str(key)] + 1)/float(dict_tag_unigram[str(tag)] + len(tag_list))
    print("emission_probability calculated")


def generate_random_sentecnces():
    tag_list = dict_tag_unigram.keys()
    iterator = 0
    while (iterator < 5):
        sentence = ""
        current_tag = "start"
        probability = 1
        while current_tag != "end":

            current_word = str(random.choice(dict_words_for_tag[current_tag]))
            current_wordtag = current_word + "/" + current_tag
            if current_wordtag in dict_emission_probabilities:
                probability = probability * dict_emission_probabilities[current_wordtag]
            else:
                probability = probability * (1.0/len(tag_list))
            future_tag = random.choice(dict_tags_for_tag[current_tag])
            current_bigramtag = current_tag + " " + future_tag
            probability = probability * dict_transition_probabilities[current_bigramtag]

            sentence = sentence + " " + current_wordtag

            current_tag = future_tag

        sentence = sentence + " /end"
        sentence_and_probability = sentence + " " + "{Probability of this sentence: " + str(probability) + "}"
        random_sentence_list.append(sentence_and_probability)
        iterator += 1
    print("Random Sentences generated")


def pos_tagging():
    rf = open(path_of_test_file+ "/" + "Test_File.txt", "r")
    words = rf.readlines()
    word_list = list()
    id = 1
    for word in words:
        if word.strip():
            w = word.replace("\n", "")
        if( str(w) != "<EOS>"):
            word_list.append(w)
        else:
            if word_list:
                word_list.pop(0)
                abc = viterbi_algorithm(word_list)
                pos_tagged_list.append("< sentence ID =" + str(id) + ">")
                for i in range(0, len(word_list)):
                    pos_tagged_list.append(str(word_list[i]) + "/" + str(abc[i]))
                pos_tagged_list.append("<EOS>")
                word_list = list()
                id += 1
    rf.close()
    print("POS tagged sentences generated")


def viterbi_algorithm(sentence):
    l = len(sentence)
    # print(l, "length")
    tag_list = dict_tag_unigram.keys()
    V = [{}]
    POStags = {}
    # print(sentence)
    for tag in tag_list:
        if(str(sentence[0]) + "/" + str(tag)) in dict_emission_probabilities:
            V[0][tag] = dict_transition_probabilities["start" + " " + tag] * dict_emission_probabilities[sentence[0] + "/" + tag]
        else:
            V[0][tag] = dict_transition_probabilities["start" + " " + tag] * (1.0/len(tag_list))

        POStags[tag] = [tag]


    for i in range(1,l):
        V.append({})
        newtags = {}

        for tag in tag_list:
            max = 0
            n_state = ""

            for p_state in tag_list:
                score = 0
                if(sentence[i] + "/" + tag) in dict_emission_probabilities:
                    score = V[i-1][p_state] * dict_transition_probabilities[p_state + " " + tag] * dict_emission_probabilities[sentence[i] + "/" + tag]
                    if score > max:
                        max = score
                        n_state = p_state
                else:
                    score = V[i-1][p_state] * dict_transition_probabilities[p_state + " " + tag] * (1.0/len(tag_list))
                    if score > max:
                        max = score
                        n_state = p_state

            V[i][tag] = max
            newtags[tag] = POStags[n_state] + [tag]
        POStags = newtags

    max1 = 0
    fstate = ""
    for tag in tag_list:
        s = V[len(sentence) - 1][tag]
        if s > max1:
            max1 = s
            f_state = tag
    return POStags[f_state]


def create_word_tag_file():
    wf = open("word-tag-frequency.txt", "w")
    d = sorted(dict_word_tag.items(), key=operator.itemgetter(1), reverse = True)
    for key, value in d:
        wf.write('%s:%s\n' % (key, value))
    print("Word Tag file created")

def create_tag_unigram_file():
    wf = open("tag-unigram-frequency.txt", "w")
    d = sorted(dict_tag_unigram.items(), key=operator.itemgetter(1), reverse = True)
    for key, value in d:
        wf.write('%s:%s\n' % (key, value))
    print("Tag Unigram file created")

def create_tag_bigram_file():
    wf = open("tag-bigram-frequency.txt", "w")
    d = sorted(dict_tag_bigram.items(), key=operator.itemgetter(1), reverse = True)
    for key, value in d:
        wf.write('%s:%s\n' % (key, value))
    print("Tag Bigram file created")

def create_transition_probability_file():
    wf = open("transition-probability.txt", "w")
    d = sorted(dict_transition_probabilities.items(), key=operator.itemgetter(1), reverse = True)
    for key, value in d:
        wf.write('%s:%s\n' % (key, value))
    print("Transition Probability file created")

def create_emission_probability_file():
    wf = open("emission-probability.txt", "w")
    d = sorted(dict_emission_probabilities.items(), key=operator.itemgetter(1), reverse = True)
    for key, value in d:
        wf.write('%s:%s\n' % (key, value))
    print("Emission Probability file created")

def create_random_sentence_file():
    wf = open("random-sentences.txt", "w")
    wf.write('\n'.join(random_sentence_list))
    print("Random Sentence File created")

def create_pos_tagged_file():
    wf = open("pos-tagged-sentences.txt", "w")
    wf.write('\n'.join(pos_tagged_list))
    print("Pos tagged Sentence File created")


create_word_tag()

replace_less_freq_with_unk()

create_tag_unigram()

create_tag_bigram()

find_transition_probability()

find_emission_probability()

generate_random_sentecnces()

create_word_tag_file()

create_tag_unigram_file()

create_tag_bigram_file()

create_transition_probability_file()

create_emission_probability_file()

create_random_sentence_file()

pos_tagging()

create_pos_tagged_file()
