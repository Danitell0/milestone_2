unsigned char	revese_bits(unsigned char octec)
{
	unsigned char	result;
	int		i;

	i = 8;
	result = 0;
	while (i-- > 0)
	{
		result = ((result << 1) | (octet & 1));
		octet = octet >> 1;
	}
	return (result);
}
