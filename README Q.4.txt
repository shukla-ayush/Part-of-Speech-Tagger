Q.4 POS Tagging

There is a file named POSTagging.py

You will have to enter the path of the folder of the training files and path of the 
test file initially.

The file is divided into various functions - 

1) create_word_tag - This function reads in the training files and creates a list of sentences
   after completing the pre-processing on it. It also assigns the start and end token to each 
   sentence. This function is primarily responsible for creating the word-tag count dictionary.

2) replace_less_freq_with_unk -  This function is resposible for replacing the words in the word-tag
   token with "UNK". It does so if the count of that word in the word-tag is equal to 1. This function
   thus updates the word-tag dictionary. It also creates another dictionary dict_words_for_tag which
   stores all the words corresponding to the tags as found in the training data.

3) create_tag_unigram - This function then creates the tag unigram, which is unigram count of all the tags.
                        It is saved in dict_tag_unigram dictionary.

4) create_tag_bigram - This function then creates the tag bigrams, which are bigram count of all the tags.
                        It is saved in dict_tag_bigram dictionary.

5) find_transition_probability - This function creates the transition probability dictionary whereby it stores
                                 the tag bigram count divided the first occuring tag unigram. Add-1 smoothing is also
                                 performed in this function.

6) find_emission_probabilty - This function creates the emission probability dictionary whereby it stores
                                 the word-tag count divided by thte tag unigram count. Add-1 smoothing is also
                                 performed in this function.

7) generate_random_sentences - This function generates random sentences. Starting from the start token, a random
                               tag is generated and then it's transition probability form previous tag is multiplied,
                               again a word in randomly generated for the current tag and its emission probability is
                               then multiplied. This keeps going on until randomly an '/end' tag is not generated. The
                               final list of random sentences is created in this function.

8) pos_tagging - This function reads the test file and creates list of sentence and passes that list of sentence to 
                 the viterbi algorithm function. After receiving the part of speech tags as a list it concatenates the
                 tags with words.

9) viterbi_algorithm - The viterbi algorithm has been implemented here by dynamic programming, where the initialzation
                       is done with the start tag and first word of the sentence. Then the most probable tag is 
                       determined for each word. If the emission and transition probability for word-tag or tag-tag
                       combination is not found, the smoothed probability is assigned.

Once all these functions are implemented all the functions associated with writing the above created dictionaries and 
lists are run and thus corresponding files are generated.