#Drakes-Next-Big-Hit

This program generates lyrics for [Drake's](https://play.spotify.com/artist/3TVXtAsR1Inumwj472S9r4?play=true&utm_source=open.spotify.com&utm_medium=open) next big hit. It works by taking some of his former songs as input, which is used to train the system and output new lyrics. 

To run this program, cd into the directory and run `python generation.py`. Each run of the program will output a new song.

If you'd like to test it out on other artists, replace the input(`oldsongs.txt`) with lyrics from any other artist. This program was created as a final project for New York University's [Natural Language Processing](http://cs.nyu.edu/courses/fall15/CSCI-UA.0480-006/) Course. 

##Songs

####The good stuff

`oldsong.txt` is a training corpus that contains the lyrics to the following songs, in order (including title)

[Take Care](https://play.spotify.com/album/63WdJvk8G9hxJn8u5rswNh?play=true&utm_source=open.spotify.com&utm_medium=open)

[Marvin's Room](https://play.spotify.com/track/2z3htsNRuhDN923ITatc56?play=true&utm_source=open.spotify.com&utm_medium=open)

[HYFR](https://play.spotify.com/track/0m1KYWlT6LhFRBDVq9UNx4)

[Shot for Me](https://play.spotify.com/track/6k7b4mcxLP5HPo6hNoXoM6?play=true&utm_source=open.spotify.com&utm_medium=open)

[Back to Back](https://play.spotify.com/track/6Q2F6SCi5jrPUCS2m1vPa6)

[Hotline Bling](https://play.spotify.com/album/19YQ10twgD5djBaBDUpH7o)

[6PM in New York](https://play.spotify.com/track/0KPUIYMqfLBvpRCwZ9hpFs)

[Sweeterman](https://www.youtube.com/watch?v=L8mu13y1itU)

[Hold On, We're Going Home](https://play.spotify.com/track/0FyBloIEdLS3f3SodFiju1?play=true&utm_source=open.spotify.com&utm_medium=open)

These songs were picked because they are some of my favorite Drake songs. They are in semi-random order.

##Notes for Class

####My approach & observations, as noted in `presentation.md`:

1. I use NLTK to do part of speech tagging for each word in `oldsong.txt`, the training corpus, which is a document of lyrics of former songs

2. I then calculate the prior/transition probabilities for each part of speech

3. When generating the new song, I use the previous word to determine the most likley subsequent part of speech (more on this below). I then look at a dictionary for that given part of speech containing words formerly used by that artists, and randomly select one.

####Implementation

*Keeping it original while maintaining the essence of the artist.*

When building this program, there were a number of factors I needed to consider in order for me to be relatively pleased with the results. I debated whether or not to exclusively use words from `oldsong.txt`, the training corpus for the output in  `newsong.txt.` Ultimately, for the sake of time, I opted to only use words that had been used before, but I would argue that it might be more effective/original to also include other common possible words (perhaps words commonly used in modern rap today that just happen to not occur in `oldsong.txt`).  To help create results that seemed more original but still stick to the essence of the artist, I opted to include more text in `oldsong.txt`, the training corpus. Though it takes much longer to run the program this way, the possibilities for newly generated songs increase exponentially.

*Determining best word to generate.*

I spend quite a bit of time contemplating how to feasibly and most effectively generate words. Throughout this course, we've learned about part of speech tagging, prior probabilities, likelihoods, HMM Taggers, etc., all used as tools to build various types of language processing programs.  With this in mind, I decided to generate words based on determining the most likely subsequent part of speech, and picking a word at random that fits that part of speech. I ended up doing this in two different ways, and my current implementation is the second:

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
for all Verbs
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

The new song generator would see that the top two most likely subsequent parts of speech are nouns and verbs. The generator would then randomly select either noun or verb to be the part of speech for the subsequent word, and select a word at random based on that. In this example, this is more effective because random selection between two options tends to generate 50/50 results. 50% for nouns is closer to 70% than (as per the Pick One implementation) 100%, and 50% for verbs is closer to 30% than 0. 

In many cases, it's proven that Top Two is more effective, but in certain circumstances it does have it's drawbacks. For example:

If the test corpus returns that 95% of verbs are followed by nouns, and 5% of verbs are followed by adjectives, a random selection between noun vs adjective will again, tend to 50/50 results. In practice, the results would have been more accurate had nouns followed verbs 100% of the time rather than 50, as per the Pick One implementation.

*However, there are a few reasons why I decided on Top Two:*

**1) Prevents Loops**

For a while, my program was spitting out loops of words that were `VBP` (verb, non-3rd person singular present) followed by `PRP` (personal pronoun) followed by `VBP` and so on. This was happening because `PRP` was the most likely word to follow `VBP` and vice-versa. By randomizing between two possibilities, it (theoretically) keeps the output grammatically correct but more diverse.

**###2) Word Diversity**

On the note of diversity, by alternating between options, there's a much greater range of possible words that can follow any preexisting one. Most importantly, there is greater diversity but a maintenance of style and type of words used. This optimizes the goal of the assignment.

####The Best Implementation... For another Time

The best algorithm for this solution would be to generate a part of speech distribution that is a probabilistic reflection of the training corpus. I will clarify through example:

Meaning, writing the program in a way such that if the training corpus suggests:

```
for all verbs
  70% are followed by nouns
  30% are followed by adjectives
```

The new song would reflect the same part of speech output as well. Maybe I can tackle this over winter break.

##Conclusion

The current output of my program is pretty mediocre. 

#References

A Survey of Natural Language Generation Systems + Rap Lyrics by Janette Martinez
