#include <unistd.h>

void	ft_putstr(char *str)
{
	int	i;

	i = 0;
	while (str[i])
	{
		write(1, &str[i], 1);
		i++;
	}
}

int	ft_atoi(char *str)
{
	int	i;
	int	result;

	i = 0;
	result = 0;
	while (str[i])
	{
		result = (result * 10) + (str[i] - '0');
		i++;
	}
	return (result);
}

void	ft_putnbr(int nb)
{
	char	c;

	if (nb > 9)
		ft_putnbr(nb / 10);
	c = (nb % 10) + '0';
	write(1, &c, 1);
}

void	tab_mult(char *str)
{
	int	i;
	int	nbr;

	i = 1;
	nbr = ft_atoi(str);
	while (i <= 9)
	{
		ft_putnbr(i);
		ft_putstr(" x ");
		ft_putstr(str);
		ft_putstr(" = ");
		ft_putnbr(i * nbr);
		if (i != 9)
			write(1, "\n", 1);
		i++;
	}

	
}

int	main(int argc, char **argv)
{
	if (argc > 1)
		tab_mult(argv[1]);
	write (1, "\n", 1);
}
