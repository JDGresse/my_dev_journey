#include <cs50.h>
#include <stdio.h>

// Variables
int height;

// Functions
void left_pyramid(int counter, int row);
void right_pyramid(int row);

int main(void)
{
    //Get pyramid height from user
    do
    {
        height = get_int("(Please select a Pyramid height between 1 and 8)\nPyramid height: ");
    }
    while (height < 1 || height > 8);

    // Print Pyramid
    for (int i = 1; i <= height; i++)
    {
        left_pyramid(height, i);

        printf("  ");

        right_pyramid(i);

        printf("\n");
    }

}

// Function that prints the left half of the pyramid
void left_pyramid(int counter, int row)
{
    for (int space = (counter - row - 1); space >= 0; space--)
    {
        printf(" ");
    }
    for (int j = row; j >= 1; j--)
    {
        printf("#");
    }
}

// Function that prints the right half of the pyramid
void right_pyramid(int row)
{
    for (int j = row; j >= 1; j--)
    {
        printf("#");
    }
}