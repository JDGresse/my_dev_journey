#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int count = 0;

int collatz(int n);

int main(void)
{
    int n = get_int("n: ");

    collatz(n);
    printf("Steps: %i\n", count);
}

// Recursive merge sort
int collatz(int n)
{
    // Base case
    if (n == 1)
    {
        return 1;
    }
    else if (n % 2 == 0)
    {
        count++;
        collatz(n/2);
    }
    else
    {
        count++;
        collatz(3*n+1);
    }
    return count;
}