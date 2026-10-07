import unittest
from job_recommendation_engine import load_data, BST, AVLTree, Graph, MaxHeap, match_score, merge_sort

class TestRecommendationSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.jobs, cls.user = load_data()
    def test_dataset_loaded(self): self.assertEqual(len(self.jobs), 8)
    def test_bst_search(self):
        t=BST()
        for j in self.jobs: t.insert(j)
        self.assertEqual(t.search("J003").job_title, "Python Developer")
    def test_bst_missing(self):
        t=BST()
        for j in self.jobs: t.insert(j)
        self.assertIsNone(t.search("J999"))
    def test_avl_search(self):
        t=AVLTree()
        for j in self.jobs: t.insert(j)
        self.assertEqual(t.search("J005").job_title, "Backend Developer")
    def test_match_full(self): self.assertEqual(match_score(["Python","SQL"], ["Python","SQL"]), 100.0)
    def test_match_partial(self): self.assertEqual(match_score(["Python","SQL"], ["Python","SQL","DSA","Git"]), 50.0)
    def test_graph_bfs(self):
        g=Graph(); g.add_edge("USER","SKILL:Python"); g.add_edge("SKILL:Python","JOB:J003")
        self.assertEqual(g.bfs("USER"), ["USER","SKILL:Python","JOB:J003"])
    def test_graph_dfs(self):
        g=Graph(); g.add_edge("USER","SKILL:Python"); g.add_edge("SKILL:Python","JOB:J003")
        self.assertIn("JOB:J003", g.dfs("USER"))
    def test_heap_top(self):
        h=MaxHeap()
        for s in [20,80,50]: h.push(s,str(s))
        self.assertEqual(h.top_k(2)[0][0], 80)
    def test_merge_sort(self):
        self.assertEqual([x[0] for x in merge_sort([(20,"B"),(80,"A"),(50,"C")])], [80,50,20])
if __name__ == "__main__": unittest.main(verbosity=2)
