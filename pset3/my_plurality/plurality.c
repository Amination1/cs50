#include <cs50.h>
#include <stdio.h>
#include <string.h>

int check(string vote, int argc, string argv[]);

typedef struct
{
    string name;
    int votes;
} person;

int main(int argc, string argv[])
{

    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    int max_votes = 0;
    int voters = get_int("Number of voters: ");
    string vote;
    person people[argc - 1];

    for (int i = 0; i < argc - 1; i++)
    {
        people[i].name = argv[i + 1];
        people[i].votes = 0;
    }

    for (int i = 0; i < voters; i++)
    {
        vote = get_string("Vote: ");
        if (check(vote, argc, argv))
        {
            for (int k = 0; k < argc - 1; k++)
            {
                if (strcmp(people[k].name, vote) == 0)
                {
                    people[k].votes += 1;
                }
            }
        }
        else
        {
            printf("Invalid vote.\n");
        }
    }

    for (int i = 0; i < argc - 1; i++)
    {
        if (people[i].votes >= max_votes)
        {
            max_votes = people[i].votes;
        }
    }

    for (int j = 0; j < argc - 1; j++)
    {
        if (people[j].votes == max_votes){
            printf("%s\n", people[j].name);
        }
    }

    return 0;
}

int check(string vote, int argc, string argv[])
{
    for (int k = 1; k < argc; k++)
    {
        if (strcmp(argv[k], vote) == 0)
        {
            return true;
        }
    }
    return false;
}
