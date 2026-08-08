#include <iostream>
#include <string>
#include "maze.cpp"

void setup() {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
}

int main() {
	setup();

	genmaze();

	int start = 0;
	scanf("%d", &start);
	getchar();
	if (start < 0 || start >= N) {
		return 1;
	}
	
	Node* current = &graph[start];
	char c = '\0';
	while (true) {
		c = getchar();
		getchar();
		if (c == 'q') {
			break;
		}

		if (c == 'w') {
			current = current->up();
		} else if (c == 's') {
			current = current->down();
		} else if (c == 'a') {
			current = current->left();
		} else if (c == 'd') {
			current = current->right();
		}
	}

  int edges = 0;
	for (int i = 0; i < N; i++) {
		if (graph[i].up != mov_null) edges++;
		if (graph[i].down != mov_null) edges++;
		if (graph[i].left != mov_null) edges++;
		if (graph[i].right != mov_null) edges++;
	}
	if (edges != 0) {
		return 1;
	}

	FILE *f = fopen("flag.txt", "r");
	char flag[64];
	fgets(flag, sizeof(flag), f);
	printf("%s\n", flag);
}
