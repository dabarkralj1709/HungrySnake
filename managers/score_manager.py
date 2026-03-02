class ScoreManager:

    def __init__(self):
        self.score = 0
        self.high_score = self.load_high_score()

    def add(self, amount):
        self.score += amount

    def reset(self):
        self.score = 0

    def check_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

    def load_high_score(self):
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read())
        except:
            return 0

    def save_high_score(self):
        with open("highscore.txt", "w") as f:
            f.write(str(self.high_score))