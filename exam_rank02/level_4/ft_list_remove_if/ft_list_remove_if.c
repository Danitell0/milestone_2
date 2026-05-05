#include <stdlib.h>
#include <stdio.h>

typedef struct		s_list
{
	struct s_list	*next;
	void			*data;
}					t_list;

t_list	*create_node(int data)
{
	t_list	*new_node;

	new_node = malloc(sizeof(t_list));
	new_node->data = data;
	new_node->next = NULL;
	return (new_node);
}

void	print_list(t_list *lst)
{
	while (lst)
	{
		printf("%d", (int)lst->data);
		lst = lst->next;
	}
}

int	comparing(void *value, void *ref)
{
	if ((int)value == (int)ref)
		return (0);
	return (1);
}

void	ft_list_remove_if(t_list **begin_list, void *data_ref, int (*cmp)())
{
	while (begin_list)
	{
		if ((*cmp)(begin_list->data, data_ref) == 0)
		{
			
		}
		begin_list = begin_list->next;
	}
}

int	main(void)
{
	t_list	*test;

	test = create_node(5);
	test->next = create_node(10);
	test->next->next = create_node(15);
	test->next->next->next = create_node(20);

	print_list(test);
	printf("\n");

	ft_list_remove_if(test, 15, comparing);
	print_list(test);
}
