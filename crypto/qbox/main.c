#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
	setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);

	char data[256];
	fgets(data, sizeof(data), stdin);
	if (data[strlen(data) - 1] == '\n') {
		data[strlen(data) - 1] = '\0';
	}

	int n = strlen(data);
	srand(n + (1337 << 8));
	for (int i = 0; i < n; i++) {
		int j = rand() % n;
		char tmp = data[i];
		data[i] = data[j];
		data[j] = tmp;
	}

	printf("%s\n", data);

	return 0;
}
