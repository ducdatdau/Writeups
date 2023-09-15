#include<stdlib.h>
#include<stdio.h>

int win(){
    printf("YES INTEGER OVERFLOW");
    system("/bin/sh");
    return 0;
}
int main()
{
    unsigned int target = 4294967040 ; // 0xffffff00
    unsigned int add ;
    scanf("%u",&add);
    target += add;
    if(target == 0)
    {
        win();
    }
    printf("Good bye");
    return 0;
}