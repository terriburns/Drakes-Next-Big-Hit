#Drakes-Next-Big-Hit

This program generates lyrics for [Drake's](https://play.spotify.com/artist/3TVXtAsR1Inumwj472S9r4?play=true&utm_source=open.spotify.com&utm_medium=open) next big hit. It works by analyzing some of Drake's former songs as input, which are used to train the system and output new lyrics.

To run this program, cd into the directory and run `python generation.py`. Each run of the program will output a new song.

If you'd like to test it out on other artists, replace the input (`oldsongs.txt`) with lyrics from any other artist. This program was created as a final project for New York University's [Natural Language Processing](http://cs.nyu.edu/courses/fall15/CSCI-UA.0480-006/) Course. This project is also being presented at Spotify's [Monthly Music Hackathon](http://monthlymusichackathon.org/) (theme: lyrics and language). The presentation for that can be found in my [Talks repo](https://github.com/terriburns/Talks). 

##Songs

####The good stuff

`oldsong.txt` is a training corpus which contains the lyrics to the following songs, in order (including title)

[Take Care](https://play.spotify.com/album/63WdJvk8G9hxJn8u5rswNh?play=true&utm_source=open.spotify.com&utm_medium=open), line 1

[HYFR](https://play.spotify.com/track/0m1KYWlT6LhFRBDVq9UNx4), line 71

[Shot for Me](https://play.spotify.com/track/6k7b4mcxLP5HPo6hNoXoM6?play=true&utm_source=open.spotify.com&utm_medium=open), line 173

[Back to Back](https://play.spotify.com/track/6Q2F6SCi5jrPUCS2m1vPa6), line 225

[Hotline Bling](https://play.spotify.com/album/19YQ10twgD5djBaBDUpH7o), line 288

[6PM in New York](https://play.spotify.com/track/0KPUIYMqfLBvpRCwZ9hpFs), line 363

[Sweeterman](https://www.youtube.com/watch?v=L8mu13y1itU), line 465

[Hold On, We're Going Home](https://play.spotify.com/track/0FyBloIEdLS3f3SodFiju1?play=true&utm_source=open.spotify.com&utm_medium=open), line 540

[From Time](https://play.spotify.com/track/10VBBaul4zVD0reteuIHM2?play=true&utm_source=open.spotify.com&utm_medium=open), line 604

[Headlines](https://play.spotify.com/album/2YLE9V9JI8WaDgbyuuJHnU?play=true&utm_source=open.spotify.com&utm_medium=open), line 681

These songs were picked because they are some of my favorite Drake songs. They are in semi-random order by preference. Note that some of these songs feature other artists, and the lyrics have not been filtered to reflect Drake's verses exclusively. All commas have been removed from the lyrics as well.

##Background, Context, and Other Information

####My approach & observations:

1. I use NLTK to do part of speech tagging for each word in `oldsong.txt` (the lyrics).

2. I then calculate the prior/transition probabilities for each part of speech

3. When generating the new song, I use the previous word to determine the most likley subsequent part of speech (more on this below). I then look at a dictionary for that given part of speech containing words formerly used by that artist, and randomly select a word from the dictionary.

4. Repeat until song is done.

####Implementation

*Keeping it original while maintaining the essence of the artist.*

When building this program, there were a number of factors I needed to consider in order for me to be relatively pleased with the results. I debated whether or not to exclusively use words from the training corpus (`oldsong.txt`), for the output in  `newsong.txt.` Ultimately, for the sake of time, I opted to only use words that had been used before, but I would argue that it might be more effective/original to also include other common possible words (perhaps words commonly used in modern/pop rap that just happen to not occur in `oldsong.txt`).  

To help create results that seemed more original but still stuck to the essence of the artist, I opted to include more text in the training corpus. Though it takes much longer to run the program this way, the possibilities for newly generated songs increase exponentially (more on this below).

*Determining best word to generate.*

I spent quite a bit of time contemplating how to feasibly and most effectively generate words. Throughout this course, we've learned about part of speech tagging, prior probabilities, likelihoods, HMM Taggers, etc., all used as tools to build various types of natural language processing programs.  With this in mind, I decided to generate words based on determining the most likely subsequent part of speech, and picking a word at random that fits that part of speech. I ended up doing this in two different ways, and my current implementation is the second:

####The first implementation: the "Pick One" Implementation

*My first implementation of word generation, not reflected in my current program, assigned the subsequent part of speech by picking the part of speech with the highest probability.*

In the Pick One implementation, if the training corpus suggested that:

```
for all verbs
  70% are followed by nouns
  30% are followed by adjectives
```

The new song generator would see that it is *most likely* that a noun follows a verb, and such, would always assign a noun to follow a verb when generating the new song. The result of which was that the new song generated would have prior probabilities/likelihoods different from the training corpus. Using my example, the new song would have:

```
for all verbs
  100% are followed by Nouns
```

(See previous commits for this version)

####The second (and ultimate) implementation: the "Top Two" Implementation

*The Top Two implementation, in contrast to the Pick One implementation, selects the top two likely parts of speech and picks one at random. After randomly picking the subsequent part of speech, the program continues as normal and selects a word at random that corresponds to that part of speech.*

Continuing with the example from the first implementation, if the training corpus suggested that:

```
for all verbs
  70% are followed by nouns
  30% are followed by adjectives
```

The new song generator would see that the top two most likely subsequent parts of speech are nouns and verbs. The generator would then randomly select either a noun or a verb to be the part of speech for the subsequent word, and select a word at random based on that. In this example, this is more effective because random selection between two options tends to generate 50/50 results. So in this example, the new song would most likely suggest that:

```
for all verbs
  50% are followed by nouns
  50% are followed by adjectives
```

50% for nouns is closer to 70% than (as per the Pick One implementation) 100%, and 50% for verbs is closer to 30% than 0. In many cases, it's proven that Top Two is more effective, but in certain circumstances it does have it's drawbacks. For example:

If the test corpus returns that 95% of verbs are followed by nouns, and 5% of verbs are followed by adjectives, a random selection between noun vs adjective will again, tend to 50/50 results. In practice, the results would have been more accurate had nouns followed verbs 100% of the time rather than 50, as per the Pick One implementation.

*However, there are a few reasons why I decided on Top Two:*

**1) Prevents Loops**

For a while, my program was spitting out loops of words that were `VBP` (verb, non-3rd person singular present) followed by `PRP` (personal pronoun) followed by `VBP` and so on. This was happening because `PRP` was the most likely word to follow `VBP` and vice-versa. By randomizing between two possibilities, it (theoretically) keeps the output grammatically correct but more diverse.

**2) Word Diversity**

On the note of diversity, by alternating between options, there's a much greater range of possible words that can follow any preexisting one. Most importantly, there is greater diversity but a maintenance of style and type of words used. With the Pick One implementation, resulting part of speech pattern would always be the same. With Top Two, the resulting part of speech pattern regularly changes. This optimizes the goal of the assignment.

####The Best Implementation... For another Time

The best algorithm for this solution would be to generate a part of speech distribution that is a probabilistic reflection of the training corpus. Meaning, writing the program in a way such that if the training corpus suggests:

```
for all verbs
  70% are followed by nouns
  30% are followed by adjectives
```

The new song would reflect the same part of speech output as well. Maybe I can tackle this over winter break.

##Conclusion

####The results

The current output of my program is *okay*. A good portion of the output is grammatically correct, but still nonsensical. Some of the output would make more sense if there was more punctuation to clarify it's intent (more on this below).  Some of the output does not make any sense at all.  As it stands, the training corpus has ten songs.  I tested the output of the program on the addition of each song (starting from just one song, Take Care), one at a time, and the results gradually improved greatly. If I were to train the program using every song that Drake has ever released, I hypothesize that the output would be much better.

####Punctuation

NLTK's part of speech tagger takes into account/parses punctuation.  My program, as it stands, takes every token from the part of speech tagger and interprets it as a word.  The most common punctuation mark in `oldsong.txt` was a comma. The regular occurrence of the comma resulted in the output to have what should have been actual words be comma. I opted to remove all commas from `oldsong.txt`.

That being said, there are still periods and question marks, which are interpreted in the program as words. Because these occurrences are much less frequent, and in a notable number of circumstances, their positions could have been interpreted as intentional, I decided to keep some punctuation. This is an imperfect solution, but I think it works for the time being.

####Improvements

*A summary of the aforementioned improvements*

1. Implementing an algorithm that results in prior probabilities reflective of the training corpus.

2. Implementing an algorithm that better accounts for various types of punctuation.

3. Implementing an algorithm that can handle exponentially greater training data.

####The End

![Image of Drake](http://www.etonline.com/news/2015/10/24187336/set_drake_hotling_bling_video-640.jpg)

##References

>A Survey of Natural Language Generation Systems + Rap Lyrics by Janette Martinez

>Lyrics obtained through [Google Play](https://play.google.com/store?hl=en) and [Genius](http://genius.com/)
