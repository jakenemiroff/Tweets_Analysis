##program to perform a sentiment analysis on a file containing tweets from different regions
#
#import function drawSimpleHistogram from the happy_histogram file
from happy_histogram import drawSimpleHistogram


# gets a file name input from user
# input: name of a file in variable filename
# output: returns the file handle (either exception if file does not exist, or opens the file to be read in the function: readData)
#processed in the main function

def open_if_file_exists(filename):
    file_handle = 0
    try:
        file_handle = open(filename, 'r', encoding="utf-8")
    except IOError:
        print("Error: file not found.")
        exit(1)
    except ValueError as exception :
        print("Error:", str(exception))

    return file_handle

#uses the opened file from the previous function
#reads each line of the file
#strips the right-most character (the \n) from each entry in the list
#appends each line to the list called "current_List"
#returns that list

def readData(file_handle):
    current_list=[]
    for line in file_handle:
        line = line.rstrip()
        current_list.append(line)

    return current_list

#splits each tweet into the four different regions based on their individual latitude and longitude points
#defines variables: latitude and longitude to be equal to a float of the first and second element of each tweet in the list of tweets
#checks to see if each current tweet contained in the list of tweets is within the given values for each different region
#if it is, it will append that specific tweet to the list of regions associated with its location
#it will return the result which is a list of each list of regions

def split_by_region(current_tweetsList):
    pacific_list = []
    mountain_list = []
    central_list = []
    eastern_list = []
    for t in current_tweetsList:
        latitude = float(t[0])
        longitude = float(t[1])
        if (24.660845 <= latitude <= 49.189787) and (-87.518395 <= longitude <= -67.444574):
            eastern_list.append(t)
        elif (24.660845 <= latitude <= 49.189787) and (-101.998892 <= longitude < -87.518395):
            central_list.append(t)
        elif (24.660845 <= latitude <= 49.189787) and (-115.236428 <= longitude < -101.998892):
            mountain_list.append(t)
        elif (24.660845 <= latitude <= 49.189787) and (-125.242264 <= longitude < -115.236428):
            pacific_list.append(t)

    return pacific_list, mountain_list, central_list, eastern_list

#computes sentiment value for each given tweet
#creates an empty list to store the sentiment values
#loops through a locally created list called current_tweetsList
#starting with the 5th position of the list of tweets all the way up to the end of the list
#creates variables, "value" and "count" which are used to calculate the sentiment score
#strips punctuation
#checks to see if a keyword is found in the list of tweets,
#if so, the the sentiment value defined in the keyword.txt file is added to the variable "value"
#count is increased by one
#append each value to the list called "sentiment_list" if the score for that tweet is not equal to zero
#return that list

def compute_sentiment(current_tweetsList, current_keywordsList):
    sentiment_list = []
    for t in current_tweetsList:
        value = 0
        count = 0
        for k in range(5, len(t)):
            word = t[k].lower().strip('#!,.@":[]')
            for keyword_element in current_keywordsList:
                if word == keyword_element[0]:
                    value = value + keyword_element[1]
                    count = count+ 1
        score = 0
        if count != 0:
            score = value / count
            sentiment_list.append(score)

    return sentiment_list

#compute the happiness score for each specific region
#sets the variable "total" equal to zero
#loops through each list of tweets by region
#adds each sentiment score for individual tweets to the total
#computes the happiness score by dividing by the total sentiment score by the number of tweets in the list

def happiness_score_by_region(sentiment_region_list):
    total = 0
    for s in sentiment_region_list:
       total = total + s
    happiness_score = total / len(sentiment_region_list)

    return happiness_score

#this is the core part of the program
#this function collects input from the user, for both the keywords as well as the tweets
#opens eacb file
#calls the function readData with the paramater of each specific file (either tweets.txt or keywords.txt)
#after the readData function is called for each file, the specific files are closed
#loops through the length of each list and splits each element of the list seperated by commas
#for the keywords, converts the second element to an integer
#splits the elements in the tweet list seperated by a space character
#creates a new list called "stripped_full_list" goes through every element in tweetsList and strips "[]," characters from each of the strings
#appends each element (without the characters mentioned above) to list "stripped_tweet_list" which is then appended to a "stripped_full_list"
#calls function "split_by_region" and puts all the lists of the different regions inside one big list
#organizes each of the four lists of regions
#calls the function "compute_sentiment"
#stores each sentiment list for each of the four regions inside their own list to be used by the next function
#calls the function "happiness_score_by_region"
#prints out the happiness score and the number of tweets for each specific region
#calls the simple histogram function
#prints the output for each region (both the happiness score and number of tweets)

def main():
    keywords_filename = input('Please enter the file name containing keywords: ')
    keywords_file_handle = open_if_file_exists(keywords_filename)
    keywordsList = readData(keywords_file_handle)
    keywords_file_handle.close()

    for i in range(len(keywordsList)):
        keywordsList[i] = keywordsList[i].split(',')
        keywordsList[i][1]=int(keywordsList[i][1])

    tweets_filename = input('Please enter the file name containing tweets: ')

    tweets_file_handle = open_if_file_exists(tweets_filename)
    tweetsList = readData(tweets_file_handle)
    tweets_file_handle.close()

    for i in range(len(tweetsList)):
        tweetsList[i] = tweetsList[i].split(' ')

    stripped_full_list = []
    for i in range(len(tweetsList)):
        stripped_tweet_list = []
        for ch in tweetsList[i]:
            ch = ch.strip('[],')
            stripped_tweet_list.append(ch)
        stripped_full_list.append(stripped_tweet_list)

    four_lists = split_by_region(stripped_full_list)

    pacific_list = four_lists[0]
    mountain_list = four_lists[1]
    central_list = four_lists[2]
    eastern_list = four_lists[3]

    sentiment_list_pacific = compute_sentiment(pacific_list, keywordsList)

    sentiment_list_eastern = compute_sentiment(eastern_list, keywordsList)

    sentiment_list_mountain = compute_sentiment(mountain_list, keywordsList)

    sentiment_list_central = compute_sentiment(central_list, keywordsList)

    happinessScore = happiness_score_by_region(sentiment_list_pacific)
    print('The happiness score for the pacific region is:', happinessScore, 'and the number of tweets for this region is:', len(sentiment_list_pacific))

    happinessScore = happiness_score_by_region(sentiment_list_eastern)
    print('\nThe happiness score for the eastern region is:', happinessScore, 'and the number of tweets for this region is:', len(sentiment_list_eastern))

    happinessScore = happiness_score_by_region(sentiment_list_mountain)
    print('\nThe happiness score for the mountain region is:', happinessScore, 'and the number of tweets for this region is:', len(sentiment_list_mountain))

    happinessScore = happiness_score_by_region(sentiment_list_central)
    print('\nThe happiness score for the central region is:', happinessScore, 'and the number of tweets for this region is:', len(sentiment_list_central))

    drawSimpleHistogram(happiness_score_by_region(sentiment_list_eastern),happiness_score_by_region(sentiment_list_central),happiness_score_by_region(sentiment_list_mountain),happiness_score_by_region(sentiment_list_pacific))

#call the main function to run the program
main()
