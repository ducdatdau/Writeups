#include<stdlib.h>
#include<stdio.h>



void setup()
{
    setvbuf(stdin,0LL,2,0LL);
    setvbuf(stdout,0LL,2,0LL);
    setvbuf(stderr,0LL,2,0LL);
    
}
void getshell()
{
    puts("[+] SAVED RIP OVERWRITED !!!");
    system("/bin/sh");
}
int main()
{
    setup();
    char buf[40];
    int size ;
    puts("Intput write size:");
    scanf("%d",&size);
    write(1,&buf,size);

    puts("Input read size:");
    scanf("%d",&size);
    read(0,&buf,size);
    return 0;
}