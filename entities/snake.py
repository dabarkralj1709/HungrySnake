class Snake:

    def __init__(self, width, height, size):
        self.width = width
        self.height = height
        self.size = size

        self.x = width // 2
        self.y = height // 2

        self.dx = 0
        self.dy = 0

        self.body = [(self.x, self.y)]
        self.grow_pending = 0

    def move(self):
        self.x += self.dx
        self.y += self.dy

        self.body.insert(0, (self.x, self.y))

        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def grow(self, amount):
        self.grow_pending += amount

    def check_wall_collision(self):
        return (
            self.x < 0 or
            self.x >= self.width or
            self.y < 0 or
            self.y >= self.height
        )

    def check_self_collision(self):
        return (self.x, self.y) in self.body[1:]

    def draw(self, screen, head_img, body_img):
        for i, segment in enumerate(self.body):
            if i == 0:
                screen.blit(head_img, segment)
            else:
                screen.blit(body_img, segment)