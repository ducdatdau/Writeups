#include <stdio.h>
#include <string.h>
void hidden()
{
    printf("Semicolon Operator in Linux");
    printf("part 1: KCSC{Linux_");
}

int main()
{
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);
    printf("What is your name: ");
    char name[0x20];
    scanf("%31s", name);
    strncpy(name, "echo \"Welcome to KCSC\"", 22);
    system(name);
}