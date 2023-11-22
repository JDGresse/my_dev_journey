#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Variables
int counter;
int final_mod;

// Functions
int card_length(long card_num, int count);
int luhn(long card_num, int count);
void which_card(long card_num, int count);

int main(void)
{
    long card_number = get_long("Number: ");

    card_length(card_number, counter);

    luhn(card_number, counter);

    // Check Luhns algorithm
    if (final_mod != 0)
    {
        printf("INVALID\n");
    }
    else
    {
        which_card(card_number, counter);
    }
}
// Cont the number of digits in the card number
int card_length(long card_num, int count)
{
    long count_num = card_num;
    count = 0;
    while (count_num != 0)
    {
        count_num = count_num / 10;
        counter++;
    }
    return count;
}
// Luhn's algorithm
int luhn(long card_num, int count)
{
    // Convert number to array
    long count_num = card_num;
    int digits[count];

    for (int i = 0; i < count; i++)
    {
        digits[i] = count_num % 10;
        count_num = count_num / 10;
    }

    // Variables
    int sum1 = 0;
    int sum2 = 0;

    // Step 1
    for (int i = 1; i <= count; i = i + 2)
    {
        if (digits[i] * 2 < 10)
        {
            sum1 = sum1 + (digits[i] * 2);
        }
        else
        {
            int more_than_10 = digits[i] * 2;
            sum1 = sum1 + (more_than_10 % 10) + 1;
        }
    }

    // Step 2
    for (int i = 0; i <= count; i = i + 2)
    {
        sum2 = sum2 + digits[i];
    }

    // Step 3
    int sum3 = sum1 + sum2;
    final_mod = sum3 % 10;

    return final_mod;
}
// Determine which Card type
void which_card(long card_num, int count)
{
    // Convert card number to array
    long count_num = card_num;
    int digits[count];

    for (int i = 0; i < count; i++)
    {
        digits[i] = count_num % 10;
        count_num = count_num / 10;
    }

    // Check for AMEX
    if (count == 15 && digits[count - 1] == 3)
    {
        if (digits[count - 2] == 4 || digits[count - 2] == 7)
        {
            printf("AMEX\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    // Check for Visa
    else if (count == 13 && digits[count - 1] == 4)
    {
        printf("VISA\n");
    }
    // Check for MasterCard or Visa
    else if (count == 16)
    {
        if (digits[count - 1] == 4)
        {
            printf("VISA\n");
        }
        else if (digits[count - 1] == 5)
        {
            if (digits[count - 2] == 1 || digits[count - 2] == 2 || digits[count - 2] == 3 || digits[count - 2] == 4 ||
                digits[count - 2] == 5)
            {
                printf("MASTERCARD\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else
        {
            printf("INVALID\n");
        }
    }
    // Invalid
    else if (count < 13 || count > 16)
    {
        printf("INVALID\n");
    }
}