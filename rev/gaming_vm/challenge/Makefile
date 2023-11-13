all:
	../bin/linux/lcc -DQ3_VM -S -Wf-target=bytecode -Wf-g ./cake.c
	../q3asm/q3asm g_syscalls.asm cake.asm
