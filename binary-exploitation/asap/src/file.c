#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <dirent.h>

char exe[] = "file";
char *flag;
char *txt;

/**
 * Flush input
 */
void myflush()
{
    int c;
    while((c = getchar()) != '\n' && c != EOF);
}

/**
 * ls.
 */
void getListFile()
{
    DIR *d;
    struct dirent *dir;
    d = opendir(".");
    if (d)
    {
        while ((dir = readdir(d)) != NULL)
        {
            if (strcmp(dir->d_name, exe) != 0 && dir->d_name[0] != '.'){ //&& strcmp(dir->d_name, "..") != 0
                printf("- %s\n", dir->d_name);
            }
        }
        closedir(d);
    }
}

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    flag = malloc(50);
    txt = malloc(1000);
    strcpy(flag, getenv("FLAG"));
}

int main(int argc, char * argv[])
{
    char *fname = malloc(40);
    int fd2;
    FILE * fd;
    int in = 0;

    init();
    printf("Welcome to poem reader v1.0!.\nHere you can read poems by another user or submit your own.\nBtw, what do you want ?\n1. Write a poem.\n2. Read a poem.\n> ");
    char opt = getchar();
    sscanf(&opt, "%d", &in);
    myflush();

    if(in == 1){
        printf("\nAfter you submit your poem, your poem will be locked to be reviewed by the owner.\n");
        printf("\nPoem file name ? (Max 40 characters): ");
        scanf("%39s", fname);
        myflush();
        if (strcmp(fname, exe) == 0 || strchr(fname, '/') != 0){
            exit(0);
        }
        printf("Poem text ? (Max 300 characters): ");
        scanf("%299s", txt);
        myflush();

        //Check if fname exists, then remove
        if (access(fname, F_OK) != -1){
            if (remove(fname) != 0){
                printf("Something's wrong, I can feel it...");
                exit(1);
            }
        }

        fd = fopen(fname, "a+");
        setbuf(fd, NULL);
        for (int i = 0; i < strlen(flag); ++i)
            fputc(flag[i], fd);
        for (int i = 0; i < strlen(txt); ++i)
            fputc(txt[i], fd);
        

        fclose(fd);
        chown(fname, 0, 0);
        chmod(fname, 0000);

        printf("Poem file %s is successfully created!\n", fname);
    } else if (in == 2) {
        printf("Some poem texts here to choose:\n");
        getListFile();
        printf("\nPoem file name ? (Max %d characters): ", (int) sizeof(fname));

        scanf("%39s", fname);
        if (strcmp(fname, exe) == 0 || strchr(fname, '/') != 0){
            exit(0);
        }
        fd2 = open(fname, O_RDONLY);

        if (fd2 < 0) {
            printf("Sorry can't read \"%s\", maybe the file is waiting for review.\n", fname);
            exit(1);
        }
        
        printf("I'M SPEED.\n");
        
        FILE *fd = fopen(fname, "r");
        char c = fgetc(fd); 
        while (c != EOF) 
        { 
            printf ("%c", c); 
            c = fgetc(fd); 
        } 
        // fgets(txt, 500, fd);
        // printf("%s\n", txt);
        fclose(fd);
        exit(0);
    }
}