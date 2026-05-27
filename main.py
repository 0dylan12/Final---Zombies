from turtle import *
from random import randint, choice

zombies = []
bombs = []
game_over = False
touch_count = 0

def playing_area():
    t = Turtle()
    t.speed(0)
    t.ht()
    t.pu()
    t.goto(-250,250)
    t.color('light blue')
    t.pd()
    t.begin_fill()
    for i in range(4):
        t.forward(500)
        t.right(90)
    t.end_fill()
    return t

class Score:
    def __init__(self, x, y, name, color):
        self.value = 0
        self.name = name
        self.score = Turtle()
        self.score.ht()
        self.score.pu()
        self.score.color(color)
        self.score.goto(x, y)
        self.update_display()
        
    def update_display(self):
        self.score.clear()
        self.score.write(f"{self.name}: {self.value}")
        
    def increment(self):
        self.value += 1
        self.update_display()

class Bullet(Turtle):
    def __init__(self, player):
        super().__init__()
        self.ht()
        self.pu()
        self.speed(0)
        self.player = player
        self.shape('circle')
        self.shapesize(0.3)
        self.color(player.playercolor)
        self.setheading(player.heading())
        self.goto(player.xcor(), player.ycor())
        self.st()
        self.move()

    def move(self):
        if game_over:
            return
        self.forward(15)
        x = self.xcor()
        y = self.ycor()
        
        for z in zombies[:]:
            if self.distance(z) < 20:
                z.ht()
                if z in zombies:
                    zombies.remove(z)
                self.player.score.increment()
                self.die()
                return

        if x < -250 or x > 250 or y < -250 or y > 250:
            self.die()
        else:

            screen.ontimer(self.move, 20)

    def die(self):
        self.ht()
        if self in self.player.bullets:
            self.player.bullets.remove(self)

class Bomb(Turtle):
    def __init__(self, player):
        super().__init__()
        self.ht()
        self.pu()
        self.speed(0)
        self.player = player
        self.shape('circle')
        self.color('red')
        self.goto(player.xcor(), player.ycor())
        self.st()
        screen.ontimer(self.explode, 1000)

    def explode(self):
        if game_over:
            return
        self.ht()
        
        bomb = Turtle()
        bomb.ht()
        bomb.speed(0)
        bomb.pu()
        bomb.goto(self.xcor(), self.ycor() - 100)
        bomb.color('orange')
        bomb.pd()
        bomb.circle(100)

        
        for z in zombies[:]:
            if self.distance(z) <= 100:
                z.ht()
                if z in zombies:
                    zombies.remove(z)
                self.player.score.increment()
                
        screen.ontimer(bomb.clear, 400)
        if self in self.player.bombs:
            self.player.bombs.remove(self)

class Zombie(Turtle):
    def __init__(self, target_player):
        super().__init__()
        self.shape('turtle')
        self.color('darkred')
        self.pu()
        self.speed(0)
        self.target_player = target_player
        self.speed_val = randint(2, 3)
        self.goto(randint(-230, 230), randint(-230, 230))

    def move_zombie(self):
        if game_over:
            return
        self.setheading(self.towards(self.target_player))
        self.forward(self.speed_val)
        
        if self.distance(self.target_player) < 18:
            announce_winner(self.target_player)

class Prize(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('circle')
        self.color('gold')
        self.pu()
        self.speed(0)
        self.relocate()

    def relocate(self):
        self.goto(randint(-230, 230), randint(-230, 230))

class Player(Turtle):
    def __init__(self, x, y, color_name, key_left, key_right, key_fire, key_bomb, name):
        super().__init__()
        self.shape('turtle')
        self.pu()
        self.speed(0)
        self.goto(float(x), float(y))
        self.playercolor = color_name
        self.color(self.playercolor)
        self.name = name
        self.bullets = []
        self.bombs = []
        self.bomb_limit = 3
        self.key_left = key_left
        self.key_right = key_right
        self.key_fire = key_fire
        self.key_bomb = key_bomb
        self.setup_keys()

    def turn_left(self):
        self.left(30)

    def turn_right(self):
        self.right(30)

    def move(self):
        self.forward(5)
        x, y = self.xcor(), self.ycor()
        if x <= -250:
            self.setx(-249)
            self.setheading(180 - self.heading())
        elif x >= 250:
            self.setx(249)
            self.setheading(180 - self.heading())
            
        if y <= -250:
            self.sety(-249)
            self.setheading(-self.heading())
        elif y >= 250:
            self.sety(249)
            self.setheading(-self.heading())

    def fire(self):
        if not game_over:
            b = Bullet(self)
            self.bullets.append(b)

    def drop_bomb(self):
        if not game_over and len(self.bombs) < self.bomb_limit:
            b = Bomb(self)
            self.bombs.append(b)

    def setup_keys(self):
        screen.onkey(self.turn_left, self.key_left)
        screen.onkey(self.turn_right, self.key_right)
        screen.onkey(self.fire, self.key_fire)
        screen.onkey(self.drop_bomb, self.key_bomb)

def announce_winner(lost_player):
    global game_over
    if game_over:
        return
    game_over = True
    
    announcer = Turtle()
    announcer.ht()
    announcer.pu()
    announcer.color('yellow')
    announcer.goto(0, 20)
    
    winner = p2 if lost_player == p1 else p1
    announcer.write("GAME OVER", align="center")
    announcer.goto(0, -20)
    announcer.write(f" Celebrating {winner.name} Wins! 🎉")


screen = Screen()
screen.bgcolor('black')
screen.screensize(500, 500)
playing_area()


s1 = Score(-240, 260, "Player 1", "green")
s2 = Score(120, 260, "Player 2", "cyan")

# Core Game Actor Instances (Aligned with your blueprint pattern)
p1 = Player("-100", "-100", 'green', 'Left', 'Right', 'space', 'Up', "Player 1")
p2 = Player("100", "-100", 'cyan', 'a', 'd', 'q', 's', "Player 2")

p1.score = s1
p2.score = s2
prize = Prize()

screen.listen()


def game_loop():
    global touch_count, game_over
    if game_over:
        return


    p1.move()
    p2.move()

    for z in zombies:
        z.move_zombie()

    for p in [p1, p2]:
        if p.distance(prize) < 20:
            prize.relocate()
            touch_count += 1
            spawn_per_player = touch_count + 1
            
            for s in range(spawn_per_player):
                zombies.append(Zombie(p1))
                zombies.append(Zombie(p2))
            break 
    screen.ontimer(game_loop, 20)

game_loop()
screen.mainloop()