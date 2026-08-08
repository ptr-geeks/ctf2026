#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

char pass[] = "!nokaz ej RTP";
int seed = 0xdeadbeef;
char flag[64];

void setup() {
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
}

bool init() {
  FILE *f = fopen("flag.txt", "r");
  if (f == NULL) {
    printf("Could not open flag file!\n");
    return false;
  }
  fgets(flag, sizeof(flag), f);

  int s = (time(NULL) / 60) ^ seed;
  srand(s);

  return true;
}

bool check_password(char *input) {
  int n = strlen(input) - 1;
  for (int i = 0; i < n; i++) {
    if (input[i] != pass[n - i - 1]) {
      return false;
    }
  }
  return true;
}

bool check_2fa(int code) {
  int twofa = rand() % 10000;
  return code == twofa;
}

int main() {
  setup();

  if (!init())
    return 1;

  char input[32];
  int code;

  printf("Enter password: ");
  fgets(input, sizeof(input), stdin);

  if (!check_password(input)) {
    printf("Incorrect password!\n");
    return 1;
  }

  printf("Enter 2FA code: ");
  scanf("%d", &code);

  if (!check_2fa(code)) {
    printf("Incorrect 2FA code!\n");
    return 1;
  }

  printf("Access granted! Here is your flag: %s\n", flag);
  return 0;
}
