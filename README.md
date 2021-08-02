# mando-bot
Initial attempt to create a Discord bot that can call the dictionary at mandoa.org

## Usage
Default command prefix: `!`

### Commands
**mandoa**<br>
Finds all words that contain the search term and prints the results to the current text channel. NOTE: betens can be *any* single quotation mark!<br>
Usage: `mandoa <search term> <language> [-r] `<br>
`<search term>`: The word or letters being looked for - can look for all words with `kar` or for all words with `when`<br>
`language`: Specify the language to search through. Current options are `english` and `mandoa`<br>
`[-r]` or `root`: root - if specific term is wanted; such as `ad` but not `adiike`.<br>

**help**<br>
Shows available commands.<br>
Usage: `help`<br>
Aliases: `h`<br>

**close**<br>
Makes this bot stop talking and removes any queued definition requests.<br>
Usage: `stop`<br>
Aliases: `s`<br>

<!-------## Screenshots
![taco](https://github.com/TychoTheTaco/Discord-Dictionary-Bot/blob/master/media/taco.jpg)->

## Installation

### Requirements
- Python

### Installation
To install, simply run `pip install .` in the project's root directory. You can then run the bot using `python -m discord_dictionary_bot` along with the appropriate arguments described below.

## Credits
<!------#### Dictionary icon
<img src="https://github.com/TychoTheTaco/Discord-Dictionary-Bot/blob/master/media/dictionary.png?raw=true" width="64" align="left"></img>
This icon was modified from the [original](https://thenounproject.com/term/dictionary/653775/).<br>
`dictionary by Oriol Sallés from the Noun Project`->
