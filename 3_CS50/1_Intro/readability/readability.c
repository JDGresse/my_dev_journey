// Libraries and/or Header files
#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

// Global variables
int calc_variables[3];
int letters = 0;
int words = 0;
int sentences = 0;
float index = 0;

// Functions
int count_text(string text);
float readability(int var1, int var2, int var3);

// Main algorithm
int main(void)
{
    string text = get_string("Text: ");

    count_text(text);

    readability(letters, words, sentences);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %0.f\n", round(index));
    }
}

// Count the letters, words, and sentences
int count_text(string text)
{
    // Count function
    for (int i =0, len = strlen(text); i < len; i++)
    {
        // Convert any UPPERCASE to lowercase
        if (isupper(text[i]))
        {
            text[i] = tolower(text[i]);
        }

        // Count letters
        if (text[i] >= 'a' && text[i] <= 'z')
        {
            letters++;
        }
        // Count words
        else if (isspace(text[i]) || text[i] == '\0')
        {
            words++;
        }
        // Count sentences
        else if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
    }
    // Count last word
    words++;

    return letters;
    return words;
    return sentences;
}

// Calculate the Coleman-Liau formula
float readability(int var1, int var2, int var3)
{
    // Average letters per 100 words
    float l = ((float) var1 / (float) var2) * 100.0;
    float s = ((float) var3 / (float) var2) * 100.0;

    // Coleman-Liau Index
    index = (0.0588 * l) - (0.296 * s) - 15.8;

    return index;
}