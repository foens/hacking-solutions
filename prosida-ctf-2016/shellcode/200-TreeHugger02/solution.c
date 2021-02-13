// Answer.cpp : Defines the entry point for the console application.
//
#include "stdio.h"

#define MAX_STRING_LENGTH 64
typedef struct _treenode_t {
	struct _treenode_t * left;
	struct _treenode_t * right;
	unsigned int pattern;
	char text[MAX_STRING_LENGTH];
} treenode_t;

char* shellcode(struct _treenode_t* root)
{
	/*unsigned char* byte = (char*)root;
	while(byte[0] != 0xde || 
		  byte[1] != 0xad ||
		  byte[2] != 0xbe ||
		  byte[3] != 0xef)
	{
		byte += 4;
	}
	return &byte[4];*/
	
	/*unsigned int* num = (unsigned int*)root;
	while(*num != 0xdeadbeef)
	{
		num++;
	}
	return (char*)&num[1];*/
	
	
	/*while(1)
	{
		if(root->pattern - root[1].pattern != 1)
			return root[1].text;
		root++;
	}*/
	
	/*if(root->pattern != 0)
	{
		while(1)
		{
			if(root->pattern - root[1].pattern != 1)
				break;
			root++;
		}
	}
	return root->text;*/
	
	/*int i = 0;
	while(1)
	{
		if(root[i].pattern != i)
			return root[i].text;
		i++;
	}*/
	/*int i = 0;
	while(1)
	{
		if(root->pattern != i)
			return root->text;
		i++;
		root++;
	}*/
	
	
	/*int i = 0;
	int* pattern = (int*)(((char*)root)+8);
	while(1)
	{
		if(*pattern != i)
			return (char*)(pattern+1);
		i++;
		pattern += sizeof(struct _treenode_t)/4;
	}*/
	
	while(root->pattern != 0xdeadbeef)
	{
		root++;
	}
	return root->text;
	
	
	//struct _treenode_t* deadbeef = &root[0xdeadbeef];
	//return deadbeef->text;
}

int main()
{
	return 0;
}



