'''
Created on 5 Jul 2016

@author: ranganathan.veluswamy
'''









if __name__ == '__main__':
    N = 6
    
    for intN in range(N,0,-1):
        space = " "
        hash = "#"
        actSpace = space*(intN-1)
        actHash = hash* ((N+1) - intN)
        print(actSpace+actHash)