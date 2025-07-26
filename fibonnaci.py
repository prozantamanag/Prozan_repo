
#Updatteeeed to check the code

#This code is written by Projan Tamang


def fibonacci(n):
    sequence = []
    a, b = 0, 1
    while len(sequence) < n:
        sequence.append(a)
        a, b = b, a + b
    return sequence

if __name__ == "__main__":
    count = int(input("How many Fibonacci numbers? "))
    print(fibonacci(count))
    
    
    
#Changes to be merged in the main file