# Pseudocode — AI-Based Job Recommendation and Career Guidance Platform

1. Read jobs_users_dataset.json.
2. Store job records and the selected user profile.
3. Create BST and AVL Tree; insert every job by Job ID.
4. Create an adjacency-list graph:
   - connect the user to each user skill;
   - connect each job to every required skill.
5. For every job:
   - find common skills with the user;
   - MatchScore = common skills / required skills × 100.
6. Insert scored jobs into a Max Heap and retrieve Top-K.
7. Use BST/AVL search for direct Job ID queries.
8. Use BFS and DFS to traverse user-skill-job relationships.
9. Use a hash table/dictionary for direct Job ID lookup.
10. Use Merge Sort to independently rank jobs by MatchScore.
11. Display searches, traversals, ranking, Top-K recommendations, and complexity.
