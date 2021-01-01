from problem import Problem


class Database:
    def __init__(self):
        self.problems = {}
        self._last_problem_key = 0

    def add_problem(self, problem):
        self._last_problem_key += 1
        self.problems[self._last_problem_key] = problem
        return self._last_problem_key

    def delete_problem(self, problem_key):
        if problem_key in self.problems:
            del self.problems[problem_key]

    def get_problem(self, problem_key):
        problem = self.problems.get(problem_key)
        if problem is None:
            return None
        problem_ = Problem(problem.title, problem.description, n_seen=problem.n_seen)
        return problem_

    def get_problems(self):
        problems = []
        for problem_key, problem in self.problems.items():
            problem_ = Problem(problem.title, problem.description, n_seen=problem.n_seen)
            problems.append((problem_key, problem_))
        return problems
