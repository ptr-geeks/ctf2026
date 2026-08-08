#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

void win() {
	FILE *f = fopen("flag.txt", "r");
	char flag[64];
	fgets(flag, sizeof(flag), f);
	printf("%s\n", flag);
}

int attack() {
	char weapon[32];
	printf("What weapon do you want to use?\n");
	printf("Your options are: sword, bow, staff\n");
	
	read(0, weapon, 128);

	if (strstr(weapon, "sword") != NULL) {
		printf("*SLASH* You hit the enemy with your sword!\n");
	}
	else if (strstr(weapon, "bow") != NULL) {
		printf("*TWANG* You hit the enemy with your bow!\n");
	}
	else if (strstr(weapon, "staff") != NULL) {
		printf("*WHOOSH* You hit the enemy with your staff!\n");
	}
	else {
		printf("You missed the enemy!\n");
	}

	return 1;
}

int defend() {
	if (rand() % 100 < 25) {
		printf("*WOOSH* The enemy missed anyway.\n");
	}
	else {
		printf("*CLING* You successfully defended yourself!\n");
	}

	return 0;
}

void vuln() {
	int idx = 0;
	int hp = 10;

	while (hp > 0) {
		printf("You have %d HP. What do you want to do?\n", hp);
		printf("1. Attack!\n");
		printf("2. Defend!\n");
		printf("3. Heal!\n");
		printf("> ");
		scanf("%d", &idx);

		if (idx == 3) {
			hp += 5;
			continue;
		}

		if (idx == 1) {
			if (fork() == 0) {
				exit(attack());
			}
		}
		else if (idx == 2) {
			if (fork() == 0) {
				exit(defend());
			}
		}

		int status = 0;
		wait(&status);
		if (status >> 8 == 1) {
			hp--;
		}
		else if ((status & 0xff) > 0) {
			printf("Ouch! This was unexpected!\n");
			hp -= 3;
		}
	}

	printf("You have been defeated!\n");
}

int main() {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);

	srand(time(NULL));
	vuln();

	return 0;
}
