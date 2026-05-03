#include <unistd.h>

void	ft_putchar(char c, int i)
{
	while (i > 0)
	{
		write (1, &c, 1);
		i--;
	}
}

void	repeat_alpha(char *str)
{
	int	i;

	i = 0;
	while (str[i])
	{
		if (str[i] >= 'a' && str[i] <= 'z')
			ft_putchar(str[i], str[i] + 1 - 'a');
		else if (str[i] >= 'A'  && str[i] <= 'Z')
			ft_putchar(str[i], str[i] + 1 - 'A');
		else
			write (1, &str[i], 1);
		i++;
	}
}

int	main(int argc, char **argv)
{
	if (argc == 2)
		repeat_alpha(argv[1]);
	write (1, "\n", 1);
}
