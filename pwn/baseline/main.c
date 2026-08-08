#include <stdio.h>

void win() {
	FILE *f = fopen("flag.txt", "r");
	char flag[64];
	fgets(flag, sizeof(flag), f);
	printf("%s\n", flag);
}

void vuln() {
	char name[32];

	printf("Hello, what's your name?\n");
	gets(name);
	printf("Nice to meet you, %s! Enjoy the CTF :)\n", name);
}

int main() {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);

	vuln();

	return 0;
}

