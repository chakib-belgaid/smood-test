## changelog 

update the generating methode using numpy.chocie instead of a loop 

## reasons 

The process is asynchrone so it is allowed to take its time and it is better to do the heavy calculations at this moment instead of the phase when the user is waiting for the shoping list

## consequences 
Change the strucutre of the policyDB products from a dict to two numpy arrays 
