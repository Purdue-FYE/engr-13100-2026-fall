Your friend is sorting their collection of antique coins. You are recording data for each coin: coins have a *denomination*, which is the value of the coin (1 for penny, 5 for nickel, 100 for dollar, etc.). The coins also have a *date*, which is the four-digit year that the coin was minted (produced). 

You recorded the denominaton and date for the first 100 coins in the collection in two Excel columns. In cell A1, you wrote "Denomination" and in cell B1, "date". 

### Question a) Write the Excel formula that tells you the average denomination.
=AVERAGE(A2:A101)

### Question b) Write the Excel formula that tells you the median mint date.
=MEDIAN(B2:B101)

### Question c) Write the Excel formula that tells you the date the oldest coin was minted.
=MIN(B2:B101)

### Question d) What does the mean denomination tell you about your friend’s collection?
The mean denomination tells you the average value of the coins in the collection. It gives an overall sense of whether the collection mostly contains low-value coins (like pennies and nickels) or higher-value coins (like dollars or rare denominations). However, the mean can be influenced by a few very high-value coins, such as dollar coins.

### Question e) If the mean denomination is much larger than the median, what does that suggest about the distribution of coin values?
If the mean is much larger than the median, the distribution is right-skewed (positively skewed). This suggests most coins are lower denominations, and small number of high-denomination coins are pulling the average upward.

### Question f) What does the standard deviation of the mint year tell you about the collection?
The standard deviation of the mint year measures how spread out the coin years are. A small standard deviation means most coins were minted around the same time period. A large standard deviation means the coins come from many different time periods, showing greater historical variety.
