#include <stdio.h>

size_t	ft_strspn(const char *s, const char *accept)
{
	int		i;
	int		j;
	int		found;
	size_t	len;

	i = 0;
	len = 0;
	while (s[i])
	{
		j = 0;
		found = 0;
		while (accept[j])
		{
			if (s[i] == accept[j])
				found = 1;
			j++;
		}
		if (found == 0)
			return (len);
		len++;
		i++;
	}
	return (len);
}

int	main(void)
{
	printf("%zu\n", ft_strspn("hello world", "hel"));
}

