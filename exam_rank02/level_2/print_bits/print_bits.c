#include <unistd.h>

void	print_bits(unsigned char octet)
{
	unsigned char	mask;

	mask = 1 << 7;
	while (mask)
	{
		if ((mask & octet) != 0)
			write(1, "1", 1);
		else
			write(1, "0", 1);
		mask = mask >> 1;
	}
}

int main(void)
{
	print_bits(2);
}
