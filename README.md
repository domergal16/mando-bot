# mando-bot
Initial attempt to create a Discord bot that can call the dictionary at mandoa.org

## Usage
Default command prefix: `!`

### Commands      
Type !help command for more info on a command.

**fandoa**<br>
accesses local fandoa sqlite3 file dictionary <br>
to search, use `!fandoa [SEARCHTERM] [LANGUAGE]`; where language is either mandoa or english and term is what you are looking for. If no language is specified, mando'a will be searched first.<br>
Use `!fandoa [SEARCHTERM] [LANGUAGE] [s]` (or s) if you are searching for an exact word, instead of words containing the search term. Search works for all single quotation marks. <br>
Use `!f [word] language p` to display the pronunciation<br>
If you want to use any of the additional flags; language must be specified
Aliases:`f`

**fandoa add**<br>
add entry to fandoa sqlite3 database<br>
Usage:use `!fandoa_add [FANDOA_WORD] [Definition] [ROOT(S)] [Pronunciation]`. Roots is needed - list the word(s) that are used to make your new word. If there are more than one root in your new word, please use an underscore instead of a space.If your word *has* no roots, please use a dash instead. Pronunciation is optional, but is the fourth string. Also, if you want to add a specific phrase, please use `_` instead of a space.<br>
WARNING: This function is case sensitive<br>

Example: `!fa jat correct;_valid_from_Jango_the_Muse jatne JAT`<br>
Aliases:`fa`<br>

**fandoa edit**<br>
edit local fandoa sqlite3 database entry<br>
Usage:use `!fandoa_edit [FANDOA_WORD] [COLUMN] [new_phrase]`. If this changes in the future, any additional keys will be documented here. Also, if you want to replace a specific phrase, please use `_` instead of a space.<br>
WARNING: This function is case sensitive<br>
Example: `!fe jat roots jatne jatne;_jate`<br>
Aliases:`fe`<br>

**fandoa delete**<br>
Note: Restricted to owner of bot/administrator<br> 
remove entry from local fandoa sqlite3 database<br>
Usage:use `!fandoa_delete [FANDOA_WORD]` or `!fd [FANDOA_WORD]` to remove the word [FANDOA_WORD] from the database<br>
Aliases:`fd`<br>

**mandoa**<br>
Finds all words that contain the search term and prints the results to the current text channel. NOTE: betens can be *any* single quotation mark!<br>
Usage: `m <search term> <language> [-r] `<br>
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
