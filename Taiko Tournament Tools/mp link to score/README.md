# mp link to score

## Description
Given the multi play link, map mod name, map link and player link, you can get the player's play score in the map from the multi play link.

## Requirement
* Python
* BeautifulSoup
* selenium
* newest webdriver version

## Usage
1. Open `setup.txt`, use the following format to fill in the player link, map mod name and map link.  
```
USER,[player link]
[map mod name 1],[map link 1]  
[map mod name 2],[map link 2]  
...   
```
* [player link] is your osu profile link.  
* The name of [map mod name `x`] should be one of NM, HD, HR, DT, FM, TB and the order from top to bottom should be NM, HD, HR, DT, FM, TB. If there is no such mod, then leave it blank. And `x` should start from 1 in ascending order.
* [map link `x`] should  
ex:

warning: 

* mplink.txt
* setup.txt
### output:
* mp score.txt

