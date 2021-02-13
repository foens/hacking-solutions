#define MAX_STRING_LENGTH 64
typedef struct _treenode_t {
	struct _treenode_t * left;
	struct _treenode_t * right;
	unsigned int pattern;
	char text[MAX_STRING_LENGTH];
} treenode_t;

char* shellcode(struct _treenode_t* root)
{
	if (root == 0)
		return 0;
	if (root->pattern == 0xdeadbeef)
		return root->text;

	char* left = shellcode(root->left);
	if (left != 0)
		return left;

	return shellcode(root->right);
}

int main()
{
	return 0;
}



