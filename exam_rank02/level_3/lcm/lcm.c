
unsigned int	HCF(unsigned int a, unsigned int b)
{
	unsigned int	temp;

	while (b != 0)
	{
		temp = b;
		b = a % b;
		a = temp;
	}
	return (a);
}

unsigned int	lcm(unsigned int a, unsigned int b)
{
	unsigned int	result;

	if (a == 0 || b == 0)
		return (0);
	result = (a * b) / HCF(a, b);
	return (result);
}
