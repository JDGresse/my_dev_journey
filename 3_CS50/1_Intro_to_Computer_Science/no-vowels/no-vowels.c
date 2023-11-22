// Write a function to replace vowels with numbers
// Get practice with strings
// Get practice with command line
// Get practice with switch

#include <cs50.h>
#include <stdio.h>
#include <string.h>

string replace(string input);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Please enter 1 word only!\n");
        return 1;
    }
    string cyper = replace(argv[1]);
    printf("%s\n", cyper);
}

string replace(string input)
{
    for (int j = 0, len = strlen(input); j < len; j++)
    {
        switch (input[j])
        {
            case 'a':
                input[j] = '6';
                break;

            case 'e':
                input[j] = '3';
                break;

            case 'i':
                input[j] = '1';
                break;

            case 'o':
                input[j] = '0';
                break;

            default:
                input[j] = input[j];
                break;
        }
    }
    return input;
}