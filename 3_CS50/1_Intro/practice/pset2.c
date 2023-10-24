#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    string user_input = get_string("Input: \n");
    string word = "gamer";

    for (int i = 0, len = strlen(user_input); i < len; i++)
    {
        if (user_input[i] == word[i])
        {
            printf("match:    %i\n", i);
        }
        else
        {
            printf("no match: %i\n", i);
        }
    }
}

