### how would you implement batching of tracked events on the client side (mouse movements or clicks)?
- using the library **libraryname** we will generate a heatmap for the user mouse movements, than we will match it with our products and return a matrix with the products and the temperature - number of seconds that have been passed while the mouse is in that position - 
- We can use this information even more to spot the interesting positions for the map - maybe the top rows are not that famous to all the users ( one case the persons monitor is too high so he will focus more on the lower part of the screen )
  
###  why is there a worker processing the events from a waiting queue rather than processing elements directly?

**for user experience sake**. 
Basically the buying process should be transparent for him, and while clicking the order button in general is just add to the list so we need to do something fast, and not block him, in the other hand for the backend since it is in a queue we can do parallelizme and dispatch it between multiplt workers, in my solution i take advantage of that to update the purchase policy for the user which will be a heavy task when we have a larger database

### how did you incorporate fairness among the products in your strategy?
i give probabilities for each product and while picking the products are chosen randomly - in the first case it is uniform since all the product have the same probability -  
  
### how does the learning parameter affect the sorting? 

Each time a product is purchased, I use the learning parameter to increase his probability
- I supposed tht the learning parameter is a ratio ( 2.5% )
- i add that ratio as a gain while balancing the rest as a loss


## extra notes : 
since here we generate only one page, it is fine however if we want to generate multipel pages, than i would add a user **session**, 
where i store the temporary  policy, and to show the rest of the pages, i would put  the probability of 0 for the poructs shown in the previous page- therefore i have to adjust the rest by distributing the *sum of probabities of the chosen products among the rest *