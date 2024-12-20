#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// hard for that i need to use ai for debug!!
int check_str(string text);
string hash_str(string text, int key);

int main(int argc, string argv[])
{
    if (argc == 2)
    {
        if (check_str(argv[1]))
        {
            string ptext = get_string("plaintext: ");
            printf("ciphertext: %s\n", hash_str(ptext, atoi(argv[1])));
        }
        else
        {
            return 1;
        }
    }
    else if (argc == 1)
    {
        printf("Usage: %s key\n", argv[0]);
        return 1;
    }
    else
    {
        printf("Usage: ");
        for (int i = 0, n = argc; i < n; i++)
        {
            printf(" %s", argv[i]);
        }
        printf("\n");
        return 1;
    }
}

int check_str(string text)
{
    bool x = true;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (!isdigit(text[i]))
        {
            x = false;
        }
    }
    return x;
}

string hash_str(string text, int key)
{
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            if (isupper(text[i]))
            {
                text[i] = (text[i] - 'A' + key) % 26 + 'A';
            }
            else
            {
                text[i] = (text[i] - 'a' + key) % 26 + 'a';
            }
        }
    }
    return text;
}
