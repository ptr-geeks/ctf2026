const int N = 100;

struct Node {
	public:
		int idx;
		bool visited;

		Node() {
			visited = false;
		}

		Node(int index, Node* (*up)(), Node* (*down)(), Node* (*left)(), Node* (*right)()) {
			idx = index;
			visited = false;
			this->up = up;
			this->down = down;
			this->left = left;
			this->right = right;
		}

		Node* (*up)();
		Node* (*down)();
		Node* (*left)();
		Node* (*right)();
} graph[N];

#include "maze_gen.cpp"
