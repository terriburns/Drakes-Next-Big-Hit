#Drake Generation: Class Presentation

Terri Burns

My final project aims to generate a rap song based on the previous work of an artist.

---

#The Question

![left filtered](http://www.rapbasement.com/wp-content/uploads/2013/11/drake-cover-650.jpg)

Can a computer program generate lyrics that could have reasonably been written by one of my favorite artists?

---

#My approach

1. I use NLTK to do POS tagging for each word in training corpus, which is a document of lyrics of former songs

2. I then calculate the prior/transition probabilities for each POS

3. When generating the new song, I use the previous word to determine the most likley subsequent POS. I then look at a dictionary for that given POS containing words formerly used by that artists, and randomly select one.

---

#Conclusion

1. Loops are a problem. For example, if the most common word to follow a Verb is a Noun, and the most common word to follow a Noun is a Verb, there is an endless loop that ends in uninteresting/nonsensical results.

2. Ideally, my song generation would reflect the same proportion of POS word distributions as the training corpus, but for the sake of time I am sticking with simply assigning the most likely POS.

3. Considering adding my own words to the dictionary of possible words to use.

---

#References

A Survey of Natural Language Generation Systems + Rap Lyrics by Janette Martinez
