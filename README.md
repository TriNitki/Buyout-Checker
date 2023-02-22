# Buyout-Checker

Buyout Checker is a web-app for finding the cheapest item for a full buyout from the Hypixel Skyblock bazzar. This feature is used to securely transfer in-game currency between accounts.

## Installation

+ Clone repository: 
```
$ git clone https://github.com/TriNitki/Buyout-Checker
```
+ Create and activate virtual environment.
+ Install the required packages: 
```
pip install -r requirements.txt
```
+ Start the server:
```
python3 manage.py runserver
```

After that, follow the link [127.0.0.1:8000](https://127.0.0.1:8000), you will see the main page.

## Usage
In the picture below you can see an example of an item from list.

![12](https://user-images.githubusercontent.com/115486555/220753420-df179114-2eb4-4bb8-870a-8085d83d4ed2.png)

Tiny explanation:
+ ENCHANTMENT_INFINITE_QUIVER_6 - Is the name of the item.
+ 17293 - Is the approximate price of the full buyout of all specific items from the bazaar.
+ 1.49% - Is the percentage of information available on which the buyout price was based.

## FAQ
Q: 
> Why is the data outdated?

A:
> Don't forget to update the data using the Update Button which is located on the right side of the top menu. This operation may take a while.


Q:
> Why is the buyout price inaccurate?

A:

> The Hypixel API provides only a fraction of all the offers in the bazaar, and that is why the information provided for some items may be incorrect, 
so if you don't want to try your luck, then I advise you to choose items whose accuracy is > 80%.
