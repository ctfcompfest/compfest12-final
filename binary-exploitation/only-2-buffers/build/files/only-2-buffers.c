

#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>

union special_number
{
    char charNum[5];
    unsigned long long longNum;
} number;
void* mmaped_area;

char *getsn(char *s, int n)	{
	return fgets(s, n, stdin);
}

int main(int argc, char const *argv[])
{
	setvbuf(stdout, NULL, _IONBF, 0);
	char buf[16];

	int fd = open("/dev/urandom", O_RDONLY, PROT_READ);
	fgets(number.charNum, 5, fdopen(fd, "r"));
	close(fd);
	mmaped_area = mmap((void*)number.longNum, 0x1000, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);

	printf("Here's you first buffer, located at the address %p:\n", mmaped_area);
	getsn(mmaped_area, 0x1000);
	printf("Ok here's your last buffer, on the stack:\n");
	getsn(buf, 48);
	printf("Ok no more buffers for you :)\n");
	close(0);
	close(1);
	close(2);

	return 0;
}