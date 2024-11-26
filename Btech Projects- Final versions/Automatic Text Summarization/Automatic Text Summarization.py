# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 16:18:09 2019

@author: Siddhi
"""

import random 

from collections import Counter 

  
# This function calulates the freq of the (i+1)th 
# word in the whole corpus, where i is the index of 
# the sentence or the word. 

  

def next_word_freq(array, sentence): 

      

    sen_len, word_list = len(sentence.split()), [] 

      

    for i in range(len(array)): 

  

        # If the sentence matches the sentence in the range (i, i+x) 

        # and the length is less than the length of the corpus, append 

        # the word to word_list. 

          

        if ' '.join(array[i : i + sen_len]).lower() == sentence.lower(): 

  

            if i + sen_len < len(array) - 1: 

  

                word_list.append(array[i + sen_len]) 

  

    # Return the count of each word in word_list 

      

    return dict(Counter(word_list)) 

  
# Calculate the CDF of each word in the 
# Counter dictionary. 

  

def CDF(d): 

      

    prob_sum, sum_vals = 0, sum(d.values()) 

      

    for k, v in d.items(): 

  

        # Calculate the PMF of each word by dividing 

        # the freq. by total of all frequencies then add 

        # all the PMFs till ith word which is the CDF of 

        # the ith word. 

          

        pmf = v / sum_vals 

        prob_sum += pmf 

        d[k] = prob_sum 

  

    # Return cdf dictionary 

      

    return d 

  
# The main function reads the sentence/word as input 
# from user and reads the corpus file. For faster processing, 
# we have taken only the first 1000 words. 

  

  

def main(sent, x, n): 

  

    # I am using this sample text here to illustrate the output. 

    # If anyone wants to use a text file, he can use the same. The code 

    # to read corpus from file has been commented below. 

  

    # corpus = open('a.txt','r').read() 

  

    corpus = '''When Johnny comes marching home again,
Hurrah! Hurrah!
We'll give him a hearty welcome then
Hurrah! Hurrah!
The men will cheer and the boys will shout
The ladies they will all turn out
And we'll all feel gay when Johnny comes marching home.
The old church bell will peal with joy
Hurrah! Hurrah!
To welcome home our darling boy,
Hurrah! Hurrah!
The village lads and lassies say
With roses they will strew the way,
And we'll all feel gay when Johnny comes marching home.
Get ready for the Jubilee,
Hurrah! Hurrah!
We'll give the hero three times three,
Hurrah! Hurrah!
The laurel wreath is ready now
To place upon his loyal brow
And we'll all feel gay when Johnny comes marching home.
Let love and friendship on that day,
Hurrah, hurrah!
Their choicest pleasures then display,
Hurrah, hurrah!
And let each one perform some part,
To fill with joy the warrior's heart,
And we'll all feel gay when Johnny comes marching home
When I was just a little girl
I asked my mother, what will I be
Will I be pretty
Will I be rich
Here's what she said to me
Que será, será
Whatever will be, will be
The future's not ours to see
Que será, será
What will be, will be
When I grew up and fell in love
I asked my sweetheart, what lies ahead
Will we have rainbows
Day after day
Here's what my sweetheart said
Que será, será
Whatever will be, will be
The future's not ours to see
Que será, será
What will be, will be
Now I have children of my own
They ask their mother, what will I be
Will I be handsome
Will I be rich
I tell them tenderly
Que será, será
Whatever will be, will be
The future's not ours to see
Que será, será
What will be, will be
Que será, será

'''

      

    l = corpus.split() 

  

    # "temp_out" will be used to store each partial sentence 

    # which will later be stored into "sent". "out" is used to store 

    # the final output. 

      

    temp_out = '' 

    out = sent + ' '

      

    for i in range(n - 6): 

  

        # calling the next_word_freq method that returns 

        # the frequency of each word next to sent in the 

        # whole word corpus. 

          

        func_out = next_word_freq(l, sent) 

  

        # cdf_dict stores the cdf of each word in the above map 

        # that is calulated using method CDF. 

          

        cdf_dict = CDF(func_out) 

          

        # We use a random number to predict the next word. 

        # The word having its CDF greater than or equal to rand 

        # and less than or equal to 1. 

          

        rand = random.uniform(0, 1) 

  

        # If cdf_dict is empty, it means the word.sentence entered by you 

        # does not exist in the corpus. Hence, break the loop and just print 

        # the word entered by you. To implement this we use try-except block. 

        # If an error occurs it implies there aren't enough values to unpack 

        # and this can happen only when your input is absent from the corpus. 

          

        try: key, val = zip(*cdf_dict.items()) 

        except: break

  

        # Iterate through the cdf values and find the smallest value 

        # greater than or equal to the random number. That value is the 

        # cdf of your predicted word. Add the key of the value to the output 

        # string and update the "sent" variable as "temp_out". 

          

        for j in range(len(val)): 

              

            if rand <= val[j]: 

                pos = j 

                break

                      

        temp_out = key[pos] 

        out = out + temp_out + ' '

        sent = temp_out 

          

    print(out, end = '\n\n') 

  

if __name__ == '__main__': 

  

    inp_sent = 'him'

    # The output will have 10 words, including the input sentence/word. 

    main(inp_sent, len(inp_sent), 10) 

