#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int compute(string text);

int main(void)
{
    string text = get_string("Text: ");
    int index = compute(text);
    if (index <= 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index == 0)
    {
        return 1;
    }
    else if (index < 16)
    {
        printf("Grade %i\n", index);
    }
}

int compute(string text)
{
    int letters = 0, words = 1, sentences = 0;
    if (strlen(text) == 0)
    {
        return 0;
    }
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
        if (text[i] == ' ')
        {
            words++;
        }
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
    }

    float l = (letters / (float) words) * 100;
    float s = (sentences / (float) words) * 100;

    int index = round(0.0588 * l - 0.296 * s - 15.8);
    return index;
}
// hard!
