class Problem:
    def __init__(self, title, description, privacy, solution_r, n_seen=1):
        self.title = title
        self.description = description
        self.privacy = privacy
        self.solution_r = solution_r
        self.n_seen = n_seen
