#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_NOTES 10
#define TITLE_MAX 64
#define CONTENT_MAX 1024

struct Note {
	int title_len;
	char title[TITLE_MAX];
	int content_len;
	char *content;
} notes[MAX_NOTES];
struct Note* note_selected = NULL;

struct Note* note_new() {
	struct Note* note = NULL;
	for (int i = 0; i < MAX_NOTES; i++) {
		if (notes[i].content == NULL) {
			note = &notes[i];
			break;
		}
	}
	if (note == NULL) {
		printf("Max notes reached\n");
		return NULL;
	}

	printf("Enter title length: ");
	scanf("%d", &note->title_len);
	getchar(); // consume newline
	if (note->title_len < 1 || note->title_len >= TITLE_MAX - 1) {
		printf("Invalid title length\n");
		return NULL;
	}

	printf("Enter title: ");
	memset(note->title, 0, TITLE_MAX);
	read(0, note->title, note->title_len);

	printf("Enter content length: ");
	scanf("%d", &note->content_len);
	getchar(); // consume newline
	if (note->content_len < 1 || note->content_len >= CONTENT_MAX - 1) {
		printf("Invalid content length\n");
		return NULL;
	}

	note->content = (char*)malloc(note->content_len);
	printf("Enter content: ");
	read(0, note->content, note->content_len);

	return note;
}

void note_list() {
	for (int i = 0; i < MAX_NOTES; i++) {
		if (notes[i].content != NULL) {
			printf("%d: %s\n", i, notes[i].title);
		}
	}
}

struct Note* note_select() {
	int idx = -1;
	
	printf("Enter note index: ");
	scanf("%d", &idx);
	getchar(); // consume newline
	if (idx < 0 || idx >= MAX_NOTES) {
		printf("Invalid index\n");
		return NULL;
	}

	if (notes[idx].content == NULL) {
		printf("Note does not exist\n");
		return NULL;
	}

	return &notes[idx];
}

void note_print() {
	if (note_selected == NULL) {
		printf("No note selected\n");
		return;
	}

	printf("Title: %s\n", note_selected->title);
	printf("Content: %s\n", note_selected->content);
}

struct Note* note_resize() {
	struct Note* note = note_selected;
	if (note == NULL) {
		printf("No note selected\n");
		return NULL;
	}

	printf("Enter new title length: ");
	scanf("%d", &note->title_len);
	getchar(); // consume newline
	if (note->title_len < 1 || note->title_len >= TITLE_MAX - 1) {
		printf("Invalid title length\n");
		return NULL;
	}

	printf("Enter new content length: ");
	scanf("%d", &note->content_len);
	getchar(); // consume newline
	if (note->content_len < 1 || note->content_len >= CONTENT_MAX - 1) {
		printf("Invalid content length\n");
		return NULL;
	}

	note->content = (char*)realloc(note->content, note->content_len);
	return note;
}

struct Note* note_edit() {
	struct Note* note = note_selected;
	if (note == NULL) {
		printf("No note selected\n");
		return NULL;
	}

	printf("Edit what?");
	printf("1. Title\n");
	printf("2. Content\n");
	int choice = 0;
	scanf("%d", &choice);
	getchar(); // consume newline
	
	if (choice == 1) {
		printf("Enter new title: ");
		memset(note->title, 0, TITLE_MAX);
		read(0, note->title, note->title_len);
	} else if (choice == 2) {
		printf("Enter new content: ");
		read(0, note->content, note->content_len);
	} else {
		printf("Invalid choice\n");
		return NULL;
	}

	return note;
}

void note_delete() {
	struct Note* note = note_selected;
	if (note == NULL) {
		printf("No note selected\n");
		return;
	}

	free(note->content);
	note->content = NULL;
	note->title_len = 0;
	note->content_len = 0;
}

void note_menu() {
	printf("0. Create note\n");
	printf("1. List notes\n");
	printf("2. Select note\n");
	printf("3. Print note\n");
	printf("4. Resize note\n");
	printf("5. Edit note\n");
	printf("6. Delete note\n");
	printf("7. Exit\n");
	printf("> ");
}

void vuln() {
	while (1) {
		int choice = 6;
		note_menu();
		scanf("%d", &choice);
		getchar(); // consume newline
		switch (choice) {
			case 0:
				note_new();
				break;
			case 1:
				note_list();
				break;
			case 2:
				note_selected = note_select();
				break;
			case 3:
				note_print();
				break;
			case 4:
				note_resize();
				break;
			case 5:
				note_edit();
				break;
			case 6:
				note_delete();
				break;
			case 7:
				return;
			default:
				printf("Invalid choice\n");
		}
	}
}

int main() {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);

	vuln();

	return 0;
}
