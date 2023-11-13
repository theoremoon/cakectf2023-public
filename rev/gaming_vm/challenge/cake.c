int rand();
int strlen(const char*);
void gets(char*, int);

int vmMain() {
  int i, j, n;
  char c, flag[100];

  trap_Printf("FLAG: ");
  gets(flag, sizeof(flag));

  n = strlen(flag);
  if (n != 42)
    goto wrong;

  for (i = 0; i < n; i++)
    flag[i] ^= 7;

  for (i = n - 1; i > 0; i--) {
    j = rand() % i;
    c = flag[j];
    flag[j] = flag[i];
    flag[i] = c;
  }

  if (strcmp(flag, "DDt4zNXXuAjk476XpsNs6bluNwfJVlQbXaSi|XfrXF") != 0)
    goto wrong;

  trap_Printf("Correct!\n");
  return 0;
 wrong:
  trap_Printf("Wrong...\n");
  return 1;
}

int seed = 1;

int rand() {
  seed = seed * 0x41c64e6d + 0x6073;
  return seed & 0x7fffffff;
}

int strlen(s) const char *s; {
  int n = 0;
  while (*s++) n++;
  return n;
}

int strcmp(s1, s2) const char *s1; const char *s2; {
  while (*s1 == *s2) {
    if (*s1 == '\0') return 0;
    s1++; s2++;
  }
  return 1;
}

void gets(buf, size) char* buf; int size; {
  int i;

  memset(buf, 0, size);
  if (size == 0)
    return;

  for (i = 0; i < size-1; i++) {
    if (trap_Read(buf + i, 1) != 1)
      break;
    if (buf[i] == '\n') {
      buf[i] = '\0';
      break;
    }
  }
}
