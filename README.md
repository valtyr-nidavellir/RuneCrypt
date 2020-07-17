# RuneCrypt
~A hardcore encryption application~
Currently in beta testing
Available on Windows and Linux

#Basic Usage:
 Most used commands-
  python3 RuneCrypt.py -f some_file_name_or_path -decoy t
  python3 RuneCrypt.py -f rune.glyph -d crypto.glyph
  
To use the default action of encrypting a file with 15 random layers-
  python3 RuneCrypt.py -f some_file_name_or_path
  
To decrypt a rune.glyph-
  python3 RuneCrypt.py -f rune.glyph -d crypto.glyph
  
To specify encryption layers-
  python3 RuneCrypt.py -f some_file_name_or_path -e random-random-random etc.
  
To use the streamline glyph ability-
  python3 RuneCrypt.py -f some_file_name_or_path -g glyph.json
  
To create a rune.glyph decoy-
  python3 RuneCrypt.py -f some_file_name_or_path -decoy t
