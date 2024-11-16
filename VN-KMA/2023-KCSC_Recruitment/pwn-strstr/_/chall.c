#include <stdio.h>
#include <string.h>
#include <stdlib.h>


void win()
{
    system("cat flag.txt");
}

void filter(char buf[0x80])
{
    if(strstr(buf, "v\x11@") || strstr(buf, "w\x11@") || strstr(buf, "z\x11@") != NULL)
    {
        printf("bypass strstr pls");
        exit(0);
    }
    if(buf[0] == NULL)
    {
        printf("no null byte");
        exit(0);
    }
}

void banner()
{
    puts(" _  ____  __    _                                   ");
    puts("| |/ /  \\/  |  / \\                                  ");
    puts("| ' /| |\\/| | / _ \\                                 ");
    puts("| . \\| |  | |/ ___ \\                                ");
    puts("|_|\\_\\_|  |_/_/__ \\_\\___ ____                       ");
    puts(" / ___\\ \\ / / __ )| ____|  _ \\                      ");
    puts("| |    \\ V /|  _ \\|  _| | |_) |                     ");
    puts("| |___  | | | |_) | |___|  _ <                      ");
    puts(" \\____|_|_|_|____/|_____|_|_\\_\\__ _______   __      ");
    puts("/ ___|| ____/ ___| | | |  _ \\|_ _|_   _\\ \\ / /      ");
    puts("\\___ \\|  _|| |   | | | | |_) || |  | |  \\ V /       ");
    puts(" ___) | |__| |___| |_| |  _ < | |  | |   | |        ");
    puts("|____/|_____\\____|\\___/|_| \\_\\___| |_|   |_|        ");
    puts(" / ___| |  | | | | __ )                             ");
    puts("| |   | |  | | | |  _ \\                             ");
    puts("| |___| |__| |_| | |_) |                            ");
    puts(" \\____|_____\\___/|____/                             \n");
}

void main()
{
    setbuf(stdin, 0);
    setbuf(stderr, 0);
    setbuf(stdout, 0);
    char buf[0x30];
    banner();
    printf("Do you want to play. Let's play\n");
    read(0, buf, 0x40);
    filter(buf);
}