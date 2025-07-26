"This code is written to check the file updation is done or not"

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