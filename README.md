#gt_say

Use the Google Translate TTS API via python.
Requires mpg123 for audio playback.

Please, make sure to not abuse the API. Until / unless Google opens up their TTS API
this is a bit of an unsupported use. Be kind.


# Usage

Just run `gt_say.py "Any input string."` The audio files will be cached locally so
snippets can be reused

# Notes

Currently uses American English, but it could be easily modified for other languages.

I was using this on a Raspberry Pi to speak weather data from Wunderground.
If you find another good use, send me a link to the project and I'll add it here.
