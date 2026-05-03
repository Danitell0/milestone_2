#include <stdio.h>
#include <stdlib.h>

typedef struct s_list
{
	void			*data;
	struct s_list	*next;
}					t_list;

t_list	*sort_list(t_list* lst, int (*cmp)(int, int))
{
	t_list	*current;
	t_list	*next;
	void	*temp;

	temp = 0;
	current = lst;
	while (current)
	{
		next = current->next;
		while (next)
		{
			if ((*cmp)((int)(long)current->data, (int)(long)next->data) == 0)
			{
				temp = current->data;
				current->data = next->data;
				next->data = temp;
			}
			next = next->next;
		}
		current = current->next;
	}
	return (lst);
}

t_list	*create_node(int data)
{
	t_list	*new_node;

	new_node = malloc(sizeof(t_list));
	new_node->data = (void *)(long)data;
	new_node->next = NULL;
	return (new_node);
}

void	print_list(t_list *lst)
{
	while (lst)
	{
		printf("%d", (int)(long)lst->data);
		lst = lst->next;
	}
}

int	ascending(int a, int b)
{
	return (a <= b);
}

int	main(void)
{
	t_list *test;

	test = create_node(5);
	test->next = create_node(2);
	test->next->next = create_node(8);
	test->next->next->next = create_node(6);

	print_list(test);
	printf("\n");

	sort_list(test, ascending);

	print_list(test);
	printf("\n");
}
