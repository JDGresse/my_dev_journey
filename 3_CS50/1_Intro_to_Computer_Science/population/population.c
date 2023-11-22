#include <cs50.h>
#include <stdio.h>

int years = 0;

int get_start_size(void);
int get_end_size(int start_pop);
int num_years(int start_pop, int end_pop);
void print_result(int years);

int main(void)
{
    // TODO: Prompt for start size
    int start_pop = get_start_size();
    // TODO: Prompt for end size
    int end_pop = get_end_size(start_pop);
    // TODO: Calculate number of years until we reach threshold
    if (end_pop == start_pop)
    {
        years = 0;
    }
    else
    {
        years = num_years(start_pop, end_pop);
    }
    // TODO: Print number of years
    print_result(years);
}

int get_start_size(void)
{
    int start_pop;
    do
    {
        start_pop = get_int("Starting Population: ");
    }
    while (start_pop < 9);
    return start_pop;
}

int get_end_size(int start_pop)
{
    int end_pop;
    do
    {
        end_pop = get_int("End Population: ");
    }
    while (end_pop < start_pop);
    return end_pop;
}

int num_years(int start, int end)
{
    int growth;
    int new_pop = start;

   do
   {
        growth = (new_pop / 3) - (new_pop / 4);
        new_pop = new_pop + growth;
        years += 1;
    }
    while (new_pop < end);
    return years;
}
void print_result(int result)
{
    if (result == 0)
    {
        printf("Years: 0\n");
    }
    else
    {
        printf("Years: %i\n", result);
    }
}