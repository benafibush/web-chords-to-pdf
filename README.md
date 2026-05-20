# Web Chords to PDF  
![Explanation.png](docs%2FExplanation.png)
This program receives a list of URLs and produces a chords songbook.   
It supports the following sites:
- [Ultimate Guitar](https://www.ultimate-guitar.com/) (English)
- [Tab for you](https://www.tab4u.com/) (Hebrew)

## Special Features
- Fit to screen - PDF width can be pre-adjusted
- Line wrapping - while keeping chords and words aligned
- Multithreading - 3 browser windows yield x10 acceleration

# The Story
I used to rely on printed guitar chord sheets for quite a while until I had a realization:
we're living in the 21st century, after all!  
Instead of carrying around a tiny ring binder filled with carefully chosen song pages in my guitar case, 
only to struggle with them on a windy day outside, 
I discovered a simpler solution. I decided to switch to using a screen!  
Initially, I considered using an e-reader, 
but later realized that a tablet screen would be even more convenient due to its responsiveness.

# Project structure
URLs ➜ **Browse** ➜ Webpages ➜ **Parse** ➜ Songbook ➜ **Publish** ➜ PDF

![Structure.png](docs%2FStructure.png)