

#include<stdio.h>
#include<stdlib.h>

void delete_secret();
void edit_secret();

struct secret
{
	char id;
	char name[15];
	uint num;
	uint content_length;
	char content[];
};

struct secret *secrets[5];
uint number_of_secrets = 0;

void print_menu()	{
	puts("=====Secret Sharing=====");
	puts("1. Add Secret");
	puts("2. Print Secret Metadata");
	puts("3. Delete Secret");
	puts("4. Exit");
	puts("========================");
	printf("Choice: ");
}

int my_read(char* buf, int size)	{
	int count;
	count = read(0, buf, size);
	if(count == -1)	{
		puts("Read Error");
		exit(-1);
	}
	if(buf[count-1] == '\n')	{
		buf[count-1] = '\0';
	}
	else	{
		char temp;
		do
		{
			read(0, &temp, 1);
		} while (temp != '\n');
	}
	return count;
}

uint read_uint()	{
	char num[5];
	my_read(num, 5);
	return atoi(num);
}

void add_secret()	{
	uint index, secret_length, count;
	printf("Index: ");
	index = read_uint();
	if(index > 4)	{
		puts("Invalid Index!");
		return;
	}
	printf("Secret Length: ");
	secret_length = read_uint();
	if(secret_length > 0x4f || secret_length < 5)	{
		puts("Too long/short!");
		return;
	}
	secrets[index] = malloc(secret_length + 0x17);
	printf("Id: ");
	my_read(&(secrets[index]->id), 1);
	printf("Your Name (we'll keep it a secret): ");
	my_read(secrets[index]->name, 15);
	printf("Content: ");
	count = my_read(secrets[index]->content, secret_length);
	secrets[index]->content_length = count;
	secrets[index]->num = ++number_of_secrets;
	puts("Secret created!");
}

void print_secret_metadata()	{
	uint index;
	printf("Index: ");
	index = read_uint();
	if(index > 4)	{
		puts("Invalid Index!");
		return;
	}
	printf("Id: %c\n", secrets[index]->id);
	printf("Content Length: %u\n", secrets[index]->content_length);
	printf("Content #: %u\n", secrets[index]->num);
}

void delete_secret()	{
	uint index;
	printf("Index: ");
	index = read_uint();
	if(index > 4)	{
		puts("Invalid Index!");
		return;
	}
	free(secrets[index]);
	puts("Secret deleted!");
}

int main(int argc, char const *argv[])
{
	setvbuf(stdout, NULL, _IONBF, 0);
	uint choice;
	while(1)	{
		print_menu();
		choice = read_uint();
		switch(choice)	{
			case 1:
				add_secret();
				break;
			case 2:
				print_secret_metadata();
				break;
			case 3:
				delete_secret();
				break;
			case 4:
				puts("Goodbye!");
				exit(0);
			default:
				puts("Invalid choice!");
				break;
		}
	}
	return 0;
}