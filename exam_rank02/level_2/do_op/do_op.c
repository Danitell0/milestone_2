#include <stdio.h>
#include <stdlib.h>

int	main(int argc, char **argv)
{
	int	val1;
	int	val2;

	if (argc != 4)
		printf("\n");
	else
	{
		val1 = atoi(argv[1]);
		val2 = atoi(argv[3]);
		if (argv[2][0] == '+')
			printf("%d", (val1 + val2));
		else if (argv[2][0] == '-')
			printf("%d", (val1 - val2));
		else if (argv[2][0] == '*')
			printf("%d", (val1 * val2));
		else if (argv[2][0] == '/')
			printf("%i", (val1 / val2));
		else if (argv[2][0] == '%')
			printf("%i", (val1 % val2));
		printf("\n");
	}
}
