# Author:  Elliott Dicus
# Website: Junenith.com
# License: MIT
# Description:
#   This takes a command line string with an optional lanuguage flag and plays the 
#   resulting audio produced by the google translate TTS api.
#   To work around API limitations, this breaks text into 100 character max strings 
#   at punctuation marks (to preserver intonation). The audio is cached by string to 
#   prevent redundant API calls.
#   
#   TODO:
#   When the cache grows quite large, remove files with the earliest access date.

import os
import sys
import unicodedata
import string
import urllib
import urllib2

# From: http://glowingpython.blogspot.com/2012/11/text-to-speech-with-correct-intonation.html
def parseText(text):
    #returns a list of sentences with less than 100 caracters
    toSay = []
    punct = [',',':',';','.','?','!'] # punctuation
    words = text.split(' ')
    sentence = ''
    for w in words:
        if w[len(w)-1] in punct: # encountered a punctuation mark
            if (len(sentence)+len(w)+1 < 100): # is there enough space?
                sentence += ' '+w # add the word
                toSay.append(sentence.strip()) # save the sentence
            else:
                toSay.append(sentence.strip()) # save the sentence
                toSay.append(w.strip()) # save the word as a sentence
            sentence = '' # start another sentence
        else:
            if (len(sentence)+len(w)+1 < 100):   
                sentence += ' '+w # add the word
            else:
                toSay.append(sentence.strip()) # save the sentence
                sentence = w # start a new sentence
    if len(sentence) > 0:
        toSay.append(sentence.strip())
    return toSay

def say(inputString, language='en'):
    fileList = [];

    # Break string at punctuation
    toSay = parseText(inputString)
    # Check for existing strings in sound_cache
    for sentence in toSay:
        fileList.append(findOrCreateAudioFile(sentence, language))

    # Play it all back
    filenames = ' '.join(['"%s"' % filename for filename in fileList])
    commandString = 'mpg123 -q %s' % filenames
    print "Running: " + commandString
    os.system(commandString)

# Returns the path to an mp3 of the input string in the given language
# Parts from: http://glowingpython.blogspot.com/2012/11/text-to-speech-with-correct-intonation.html
def findOrCreateAudioFile(inputString, language):
    languageDir = os.path.join("sound_cache", language)
    filenameString = removeDisallowedFilenameChars(inputString + ".mp3")
    filePath = os.path.join(languageDir, filenameString)
    # Does the directory for this language exist?
    if not os.path.isdir(languageDir):
        # Create it
        os.makedirs(languageDir)
    # Do we have something that looks like this in the cache?
    if os.path.exists(filePath):
        return filePath
    else: # Otherwise, go get it.
        opener = urllib2.build_opener()
        # Is this required?
        opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)')]
        encodedString = urllib.quote_plus(inputString)
        tts_url = "http://translate.google.com/translate_tts?tl=%s&q=%s" % (language, encodedString)
        print "Downloading: " + tts_url
        response = opener.open(tts_url)
        ttsFile = open(filePath, 'wb')
        ttsFile.write(response.read())
        ttsFile.close()
        return filePath

def clearCache(cacheSize):
    # Tally up the size. Over?
    # In a loop adding up size:
        # Find the largest file with oldest access time
        # Is this enough reclaimed space to fall under the limit?
    # Delete the files
    pass

# From: http://stackoverflow.com/a/698714
def removeDisallowedFilenameChars(filename):
    filename = filename.decode('unicode-escape')
    validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleanedFilename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore')
    return ''.join(c for c in cleanedFilename if c in validFilenameChars)

if __name__ == "__main__":
    inputString = "I'm sorry Dave. I'm afraid I can't do that."
    if len(sys.argv) > 1:
        inputString = sys.argv[1]
    say(inputString)
