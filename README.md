This project aims to analyze and identify arbitrage opportunities in cryptocurrency markets by tracking real-time price discrepancies across different trading pairs on the Binance exchange. 
The script calculates potential arbitrage opportunities by examining the price differences of cryptocurrencies in various trading pairs. 


This project is Dockerized.
First, ensure the Docker daemon is running.

Copy the project and navigate into the respective folder.
There, run the following:
```
docker build -t arbitrage .
```
Then, run the following:
```
docker run arbitrage
```

It is also possible to install the dependencies with ```pip``` manually and then run the main.py file.


A few notes about the code:
- In the final version, only the main.py is necessary. All the other .py files were used for intermediary data processing.
- Initially, all possible pairs were fetched. From there, all possible triplets of the following form were constructed: AB, BC, AC.
- The rest is very simple async logic.
- Because some pairs' data are sent in such a short span of time, no price discrepancies might occur. To account for this, I added a 5-second cool down for each pair.
- Amongst all possible triplets, I prioritized the ones containing symbols that have been known to show high volatility and those paired with fiat currencies experiencing significant fluctuations (such as TRY)).

The entirety of this project was built by me, Tuna Bozkurt.
I look forward to hearing back from the TankX team.
