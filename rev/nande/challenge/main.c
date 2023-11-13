#include <stdio.h>
#include <string.h>

typedef unsigned char bit;
bit InputSequence[0x100];
bit OutputSequence[0x100];
bit AnswerSequence[0x100] = {
	1,1,1,1,1,0,0,1,1,0,0,1,0,0,1,0,0,1,1,0,0,0,0,1,1,1,1,1,0,0,1,1,1,1,0,1,0,1,1,1,0,0,0,1,1,0,
	1,1,1,1,0,1,0,1,0,0,1,0,1,0,1,1,0,1,0,0,1,1,0,1,1,0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,1,1,1,
	0,0,1,1,1,0,0,1,1,1,0,1,0,1,1,1,1,0,1,1,0,0,0,1,1,0,0,1,1,0,1,1,0,0,0,1,0,1,1,1,0,1,0,0,0,0,
	1,0,0,0,0,1,1,1,0,1,0,0,0,1,1,0,0,1,0,0,0,0,0,1,0,0,0,0,1,1,1,1,1,1,1,1,1,0,1,0,1,0,0,1,1,0,
	1,1,1,0,1,0,1,0,1,0,0,0,0,0,0,1,1,0,1,1,0,1,1,0,1,0,1,0,1,0,0,1,1,1,1,1,0,1,1,0,1,1,1,0,0,1,
	0,1,1,0,1,1,0,0,1,0,0,1,1,0,0,1,1,1,0,1,0,1,0,1,1,0,
};

// CakeCTF{h2fsCHAo3xOsBZefcWudTa4}
void NAND(bit a, bit b, bit*z) {
	*z = a & b ? 0 : 1;
}

void MODULE(bit a, bit b, bit*x) {
	bit t1, t2, t3;
	NAND(a, b, &t1);
	NAND(a, t1, &t2);
	NAND(b, t1, &t3);
	NAND(t2, t3, x);
}

void CIRCUIT(bit in[], bit out[]) {
	size_t i;
	for (size_t rnd = 0; rnd < 0x1234; rnd++) {
		for (i = 0; i < 0xff; i++) {
			MODULE(in[i], in[i + 1], &out[i]);
		}
		MODULE(in[i], 1, &out[i]);
		memcpy(in, out, 0x100);
	}
}

int main(int argc, char **argv) {
	if (argc < 2) {
		printf("Usage: %s <flag>\n", argv[0]);
		return 1;
	}
	char* flag = argv[1];
	if (strlen(flag) != 0x20) goto wrong;

	for (size_t i = 0; i < 0x20; i++) {
		for (size_t j = 0; j < 8; j++) {
			InputSequence[i*8+j] = (flag[i] >> j) & 1;
		}
	}

	CIRCUIT(InputSequence, OutputSequence);

	bit is_correct = 1;
	for (size_t i = 0; i < 0x100; i++) {
		is_correct &= OutputSequence[i] == AnswerSequence[i];
	}
	if (!is_correct) goto wrong;

correct:
	puts("Correct!");
	return 0;
wrong:
	puts("Wrong...");
	return 1;
}
