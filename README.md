
# Duplicate Parser

This is a simple script to parse a list of companies and output potential duplicates.

## Usage

The script is run from the CLI, using the `main.py` file as the entrypoint and specifying the input file as an argument:
```bash
python main.py input.txt
```
Each company name in the input file is cleaned (lowercased, stripped of punctuation and common words, etc.) and then stored and checked in a dictionary of all company names. If duplicates are found, they are output to the `output/duplicates.txt` file.




## Design Considerations and Future Improvements

### Simple, but Fast
Our current implementation runs in O(n) time, as we process company names and then store them in a dictionary, allowing us to check for duplicates in constant time. This is very basic duplicate detection, relying on exact string matching after some preprocessing. More sophisticated strategies, such as inverted index-based matching and fuzzy matching, would likely capture more duplicates, but at a tradeoff of increased runtime complexity. Is that tradeoff worth it? It's impossible to say without more data and a better understanding of duplicate patterns. With more time, I would certainly explore these more sophisticated strategies in more detail (relevant links [here](https://stackoverflow.com/questions/28305008/algorithm-to-find-similar-strings-in-a-list-of-many-strings) and [here](https://yassineelkhal.medium.com/the-complete-guide-to-string-similarity-algorithms-1290ad07c6b7)). However, given the time constraints and scope of this assignment, I erred on the side of simplicity and speed.


### Ideal Approach
The biggest challenge with this assignment is the lack of visibility over duplicate patterns. Ideally, when encountering a complex problem like this, I would spend time reviewing data samples to identify patterns in how duplicates present themselves. I can make intuitive guesses - which are reflected in the string cleaning logic and `removal_words.txt` - but our intuition-based solution may be missing other patterns of duplicates. Deeply understanding the problem space would subsequently inform the appropriate selection of duplicate capturing strategies (i.e., should we add a more complex string matching algorithm, even if it impacts runtime? Should we add more removal words to `removal_words.txt`?).
