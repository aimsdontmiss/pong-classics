import pygame;

pygame.init();

WIDTH, HEIGHT = 600, 600;



WIN = pygame.display.set_mode((HEIGHT, WIDTH)); 
pygame.display.set_caption("Pong");

FPS = 60;
BLACK = (0, 0, 0);
WHITE = (255, 255, 255);

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100;
BALL_RADIUS = 7;


class Paddle: 
    COLOR = WHITE; 
    VEL = 4;

    def __init__(self, x, y, width, height):
        self.x = x; 
        self.y = y;
        self.width = width;
        self.height = height;
   
    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height));

    def move(self, up=True):
        if up:
            self.y -= self.VEL;
        else:
            self.y += self.VEL;


class Ball:
    COLOR = WHITE;
    MAX_VEL = 5;

    def __init__(self, x, y, radius):
        self.x = x;
        self.y = y;
        self.radius = radius;
        self.x_vel = self.MAX_VEL;
        self.y_vel = 0;
    
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius);
    
    def move(self):
        self.x += self.x_vel;
        self.y += self.y_vel;



def draw(win, paddles, ball):
    win.fill(BLACK);
    
    for paddle in paddles:
        paddle.draw(win);
        
    ball.draw(win);
    ball.move();
    pygame.display.update();  


def handle_collision(ball, left_paddle, right_paddle):
    # If the ball hits the top or bottom of the screen, bounce it off
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1;
    elif ball.y - ball.radius <= 0: 
        ball.y_vel *= -1;
    
    # If the ball hits the left paddle, bounce it off
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1;

                # TODO: Make the ball bounce off the paddle at an angle depending on where it hits 
                middle_y = left_paddle.y + left_paddle.height//2;
                difference_in_y = middle_y - ball.y;
                reduction_factor = (left_paddle.height//2) // ball.MAX_VEL;
                y_vel = difference_in_y // reduction_factor;
                ball.y_vel = -1 * y_vel;
    else:       # If the ball hits the right paddle, bounce it off
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1;

                # TODO: Make the ball bounce off the paddle at an angle depending on where it hits  
                middle_y = right_paddle.y + right_paddle.height//2;
                difference_in_y = middle_y - ball.y;
                reduction_factor = (right_paddle.height//2) // ball.MAX_VEL;
                y_vel = difference_in_y // reduction_factor;
                ball.y_vel = -1 * y_vel;
    
    # If the ball goes off the screen, reset it to the middle
    if ball.x - ball.radius <= 0 or ball.x + ball.radius >= WIDTH:
        ball.x = WIDTH//2;
        ball.y = HEIGHT//2;
        ball.x_vel = ball.MAX_VEL;
        ball.y_vel = 0;
    # If the ball hits the left or right side of the screen, add a point to the other side (TODO add score)
    if ball.x - ball.radius <= 0 or ball.x + ball.radius >= WIDTH:
        pass;


def handle_paddle_movement(keys, left_paddle, right_paddle):
    # Left paddle movement up is W, down is S. The and conditions are to make sure the paddle doesn't go off the screen
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move();
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(False);
    # Right paddle movement up is UP, down is DOWN. The and conditions are to make sure the paddle doesn't go off the screen
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move();
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(False);



def main():
    run = True;
    clock = pygame.time.Clock();

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT);
    right_paddle = Paddle(WIDTH - PADDLE_WIDTH - 10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT);

    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS);

    while run:
        clock.tick(FPS);
        draw(WIN, [left_paddle, right_paddle], ball);
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                run = False;
    
        keys = pygame.key.get_pressed();
        handle_paddle_movement(keys, left_paddle, right_paddle);

        handle_collision(ball, left_paddle, right_paddle);
    
    pygame.quit();

main();
