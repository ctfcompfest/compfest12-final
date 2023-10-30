

#include <stdio.h>
#include <stdlib.h>

int main(int argc, const char* argv[])
{
	if(argc < 2)	{
		fprintf(stderr, "%s\n", "Usage: ./readFlag <file>");
		return -1;
	}
	char* buf = malloc(100);
	FILE* fp = fopen(argv[1], "r");
	if(fgets(buf, 100, fp) == NULL)
		return 0;
	puts(buf);
	return 0;
}