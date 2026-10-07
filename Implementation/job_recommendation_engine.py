import json
from dataclasses import dataclass
from pathlib import Path

DATA_FILE = Path(__file__).with_name("jobs_users_dataset.json")

@dataclass
class Job:
    job_id: str
    job_title: str
    company: str
    category: str
    experience: int
    skills: list[str]

class BSTNode:
    def __init__(self, job):
        self.job, self.left, self.right = job, None, None

class BST:
    def __init__(self): self.root = None
    def insert(self, job):
        def add(node, job):
            if node is None: return BSTNode(job)
            if job.job_id < node.job.job_id: node.left = add(node.left, job)
            elif job.job_id > node.job.job_id: node.right = add(node.right, job)
            return node
        self.root = add(self.root, job)
    def search(self, job_id):
        node = self.root
        while node:
            if job_id == node.job.job_id: return node.job
            node = node.left if job_id < node.job.job_id else node.right
        return None
    def inorder(self):
        result = []
        def walk(node):
            if node:
                walk(node.left); result.append(node.job.job_id); walk(node.right)
        walk(self.root); return result

class AVLNode:
    def __init__(self, job):
        self.job, self.left, self.right, self.height = job, None, None, 1

class AVLTree:
    def _h(self, n): return n.height if n else 0
    def _bal(self, n): return self._h(n.left) - self._h(n.right) if n else 0
    def _upd(self, n): n.height = 1 + max(self._h(n.left), self._h(n.right))
    def _rr(self, y):
        x, t = y.left, y.left.right
        x.right, y.left = y, t
        self._upd(y); self._upd(x); return x
    def _rl(self, x):
        y, t = x.right, x.right.left
        y.left, x.right = x, t
        self._upd(x); self._upd(y); return y
    def _insert(self, n, job):
        if n is None: return AVLNode(job)
        if job.job_id < n.job.job_id: n.left = self._insert(n.left, job)
        elif job.job_id > n.job.job_id: n.right = self._insert(n.right, job)
        else: return n
        self._upd(n); b = self._bal(n)
        if b > 1 and job.job_id < n.left.job.job_id: return self._rr(n)
        if b < -1 and job.job_id > n.right.job.job_id: return self._rl(n)
        if b > 1: n.left = self._rl(n.left); return self._rr(n)
        if b < -1: n.right = self._rr(n.right); return self._rl(n)
        return n
    def insert(self, job): self.root = self._insert(getattr(self, "root", None), job)
    def search(self, job_id):
        n = getattr(self, "root", None)
        while n:
            if job_id == n.job.job_id: return n.job
            n = n.left if job_id < n.job.job_id else n.right
        return None

class Graph:
    def __init__(self): self.adj = {}
    def add_edge(self, a, b):
        self.adj.setdefault(a, []).append(b); self.adj.setdefault(b, []).append(a)
    def bfs(self, start):
        seen, q, order = {start}, [start], []
        while q:
            n = q.pop(0); order.append(n)
            for x in self.adj.get(n, []):
                if x not in seen: seen.add(x); q.append(x)
        return order
    def dfs(self, start):
        seen, order = set(), []
        def visit(n):
            if n in seen: return
            seen.add(n); order.append(n)
            for x in self.adj.get(n, []): visit(x)
        visit(start); return order

class MaxHeap:
    def __init__(self): self.items = []
    def push(self, score, job):
        self.items.append((score, job)); i = len(self.items) - 1
        while i:
            p = (i - 1) // 2
            if self.items[p][0] >= self.items[i][0]: break
            self.items[p], self.items[i] = self.items[i], self.items[p]; i = p
    def pop(self):
        top = self.items[0]; last = self.items.pop()
        if self.items:
            self.items[0] = last; i = 0
            while True:
                l, r, m = 2*i+1, 2*i+2, i
                if l < len(self.items) and self.items[l][0] > self.items[m][0]: m = l
                if r < len(self.items) and self.items[r][0] > self.items[m][0]: m = r
                if m == i: break
                self.items[i], self.items[m] = self.items[m], self.items[i]; i = m
        return top
    def top_k(self, k):
        temp = MaxHeap(); temp.items = self.items.copy()
        return [temp.pop() for _ in range(min(k, len(temp.items)))]

def merge_sort(records):
    if len(records) <= 1: return records[:]
    m = len(records)//2
    a, b = merge_sort(records[:m]), merge_sort(records[m:])
    out=[]; i=j=0
    while i < len(a) and j < len(b):
        if a[i][0] >= b[j][0]: out.append(a[i]); i += 1
        else: out.append(b[j]); j += 1
    return out + a[i:] + b[j:]

def match_score(user_skills, job_skills):
    u, j = set(x.lower() for x in user_skills), set(x.lower() for x in job_skills)
    return round(100 * len(u & j) / len(j), 2) if j else 0.0

def load_data():
    raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return [Job(**j) for j in raw["jobs"]], raw["users"][0]

def build_graph(jobs, user):
    g = Graph(); user_node = f"USER:{user['user_id']}"
    for s in user["skills"]: g.add_edge(user_node, f"SKILL:{s}")
    for job in jobs:
        for s in job.skills: g.add_edge(f"JOB:{job.job_id}", f"SKILL:{s}")
    return g

def main():
    jobs, user = load_data()
    job_hash = {j.job_id: j for j in jobs}
    bst, avl = BST(), AVLTree()
    for j in jobs: bst.insert(j); avl.insert(j)
    graph = build_graph(jobs, user)
    scored = [(match_score(user["skills"], j.skills), j) for j in jobs]
    heap = MaxHeap()
    for score, job in scored: heap.push(score, job)
    print("=== AI JOB RECOMMENDATION DSA PROTOTYPE ===")
    print(f"User: {user['name']} | Skills: {', '.join(user['skills'])}")
    print("\nBST Search:", bst.search("J003").job_title)
    print("BST Inorder:", bst.inorder())
    print("AVL Search:", avl.search("J005").job_title)
    print("\nBFS:", " -> ".join(graph.bfs(f"USER:{user['user_id']}")[:8]))
    print("DFS:", " -> ".join(graph.dfs(f"USER:{user['user_id']}")[:8]))
    print("\nHash Lookup:", job_hash["J008"].job_title)
    print("\nMerge Sort Ranking:")
    for s,j in merge_sort(scored)[:5]: print(f"{j.job_id} | {j.job_title} | {s}%")
    print("\nMax Heap Top-5:")
    for s,j in heap.top_k(5): print(f"{j.job_id} | {j.job_title} | {s}%")
    print("\nComplexity Summary:")
    print("BST search: average O(log n), worst O(n)")
    print("AVL search/insert: O(log n)")
    print("BFS/DFS: O(V + E)")
    print("Hash lookup: average O(1)")
    print("Merge Sort: O(n log n)")
    print("Heap push/pop: O(log n); Top-K: O(k log n)")
if __name__ == "__main__": main()
