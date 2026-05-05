#include <stdio.h>
#include <stdlib.h>

int	is_seperator(char c)
{
	if (c == ' ' || c == '\t' || c == '\n')
		return (1);
	return (0);
}

size_t	word_len(char *str, int i)
{
	size_t	len;

	len = 0;
	while (str[i] && !is_seperator(str[i++]))
		len++;
	return (len);
}

size_t	count_words(char *str)
{
	size_t	counter;
	int	i;

	i = 0;
	counter = 0;
	while (is_seperator(str[i]))
		i++;
	while (str[i])
	{
		if (!is_seperator(str[i]) && (i == 0 || is_seperator(str[i - 1])))
			counter++;
		i++;
	}
	return (counter);
}

char	**ft_split(char *str)
{
	char	**result;
	size_t	words;
	int	i;
	int	j;
	int	k;

	i = 0;
	j = 0;
	words = count_words(str);
	result = (char **)malloc((words + 1) * sizeof(char *));
	while (str[i])
	{
		k = 0;
		if (!is_seperator(str[i]))
		{
			result[j] = malloc((word_len(str, i) + 1) * sizeof(char));
			while (!is_seperator(str[i]) && str[i])
				result[j][k++] = str[i++];
			result[j][k] = '\0';
			j++;
		}
		else
			i++;
	}
	return (result);
}

int	main(void)
{
	char	**test;
	int	i = 0;

	test = ft_split("Hello World");
	while (test[i])
	{
		printf("%s\n", test[i]);
		i++;
	}
}
