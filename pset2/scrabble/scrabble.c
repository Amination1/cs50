#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int match(string word);

int main(void)
{
    string p1 = get_string("player one : ");
    string p2 = get_string("player two : ");
    if (match(p1) > match(p2))
    {
        printf("Player 1 wins!");
    }
    if (match(p2) > match(p1))
    {
        printf("Player 2 wins!");
    }
    else
    {
        printf("Tie!");
    }
}

int match(string word)
{
    int words[26] = {1, 3, 3, 2,  1, 4, 2, 4, 1, 8, 5, 1, 3,
                     1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
    int sum = 0;
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        if (isalpha(word[i]))
        {
            sum += words[tolower(word[i]) - 'a'];
        }
    }
    return sum;
}
