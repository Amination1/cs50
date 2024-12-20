#include <cs50.h>
#include <stdio.h>
#include <string.h>

bool str_check(char *f, char *s);

int main(int argc, char *argv[])
{
    if (argc < 3 || argc > 3)
    {
        printf("Excepted 2 input!\n");
        return 1;
    }
    char *first = argv[1];
    char *second = argv[2];

    if (str_check(first, second))
    {
        printf("Same\n");
    }
    else
    {
        printf("Different\n");
    }

    return 0;
}

bool str_check(char *f, char *s)
{
    if (strlen(f) != strlen(s))
    {
        return false;
    }

    for (int i = 0; i < strlen(f); i++)
    {
        if (f[i] != s[i])
        {
            return false;
        }
    }

    return true;
}
