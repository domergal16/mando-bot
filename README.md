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

**fandoa**<br>
Finds all words that contain the search term and prints the results to the current text channel. Accesses local fandoa file dictionary - NOT an existing google doc. NOTE: betens can be *any* single quotation mark!<br>
Usage: `fandoa <search term> <language> [-r] `<br>
`<search term>`: The word or letters being looked for - can look for all words with `kar` or for all words with `when`<br>
`language`: Specify the language to search through. Current options are `english` and `mandoa`<br>
`[-r]`: root - if specific term is wanted; such as `ad` but not `adiike`.<br>

**fandoa_edit**<br>
Allows a user to edit the fandoa.json file- whether by writing a new definition, correcting misspellings. Additional editing features may be added in the future. Use `!fandoa_edit MANDOA_WORD LANGUAGE -REP Original_word New_word` ; where language is either the mandoa or english definition you wish to update and mandoa_word is the specific word you want to edit. -REP signals that you want to replace a part of the definition or term, and New_word is what you will be replacing the original with.

`!fandoa_edit MANDOA_WORD LANGUAGE TERM` is used when you want to replace the entire definition or term.

The `fandoa.json` file will be updated.<br>
Usage: `!fandoa_edit MANDOA_WORD LANGUAGE [-REP] Original_word New_word` <br>
`<search term>`: The word or letters being looked for - can look for all words with `kar` or for all words with `when`<br>
`language`: Specify the language to search through. Current options are `english` and `mandoa`<br>
`[-r]`: replace - if only a portion of an existing term is to be modified.<br> 
`og_term`: USE IF REPLACING; part of term you want to replace.<br>
`new_term`: REQUIRED; the word or definitions that will be inserted.<br>

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
