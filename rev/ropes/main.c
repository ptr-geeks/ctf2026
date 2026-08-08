#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

char *flag = "ptr{7h1s_AI_M0D3l_s33M5_3x7r3M3lY_iNEff1c13n7}";

int main() {
	int idx;
	char c;

	srand(time(NULL));

	printf("Ask me something about the flag\n");
	printf("Input format: <index> <character>\n");
	printf("Index starts at 0 and tells you something about the flag\n");
	printf("Character is the character you want to check at that index\n");

  scanf("%d %c", &idx, &c);

	printf("Machine is learning ...\n");
	usleep(2500000);
	printf("Using thinking model ...\n");
	usleep(2500000);
	if (rand() % 100 < 30) {
		printf("This looks wrond, retrying with another model ...\n");
		usleep(2500000);
	}
	printf("Compiling results ...\n");
	usleep(2500000);
	if (rand() % 100 < 5) {
		printf("Critical falure, model offline! Try again later\n");
		return 0;
	}

	if (idx < 0) {
		printf("The flag is larger than that\n");
		return 1;
	}
	if (idx >= strlen(flag)) {
		printf("The flag is smaller than that\n");
		return 1;
	}

	if (flag[idx] == c) {
		printf("I think this matches\n");
	} else if (flag[idx] < c) {
		printf("I don't think this matches\n");
	}

	printf("\n");
	printf("Cleaning up ...\n");
	usleep(5000000);

	return 0;
}
