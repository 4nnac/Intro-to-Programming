# Import the pygame library
import pygame
import random  # NEW: For generating random math problems

# Initialize pygame - this must be done before using pygame functions
pygame.init()

# Set up the display window
# Creates a window that is 800 pixels wide and 600 pixels tall
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the window title that appears at the top
pygame.display.set_caption("Frogger Game")

# Create a clock object to control frame rate
clock = pygame.time.Clock()

# Define colors using RGB values (Red, Green, Blue) from 0-255
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
YELLOW = (255, 255, 0)
BRIGHT_YELLOW = (255, 255, 150)
RED = (200, 0, 0)
BLUE = (0, 100, 200)
PURPLE = (150, 0, 150)
ORANGE = (255, 140, 0)
BROWN = (139, 69, 19)
TAN = (210, 180, 140)
PINK = (255, 182, 193)

# Grid settings
grid_size = 50  # Each grid square is 50 pixels
rows = screen_height // grid_size  # Calculate number of rows (12 rows)
cols = screen_width // grid_size  # Calculate number of columns (16 columns)

# Player settings
player_row = 11  # Start at bottom row
player_col = 7   # Start near middle column (column 7 out of 0-15)
player_lives = 3  # Number of lives the player has
player_score = 0  # Player's score (increases when reaching goal)
successful_crossings = 0  # NEW: Track number of successful crossings

# Game state
game_over = False  # Tracks if the game has ended
difficulty_multiplier = 1.0  # Multiplier for car speeds (increases with score)
easy_mode = False  # NEW: Flag to indicate if easy mode is active
time_challenge_active = False  # NEW: Flag for time guessing challenge
start_time = pygame.time.get_ticks()  # NEW: Track when game started (in milliseconds) - NEVER RESETS
game_start_time = start_time  # NEW: Store the very first start time for current game session
user_time_guess = ""  # NEW: Store user's time guess input
show_time_result = False  # NEW: Flag to show the result screen
actual_play_time = 0  # NEW: Store actual play time in minutes
actual_play_seconds = 0  # NEW: Store the seconds component of play time
user_guessed_time = 0  # NEW: Store what user guessed
time_guess_correct = False  # NEW: Store if guess was correct
passed_time_challenge = False  # NEW: Flag if user passed the time challenge
crossings_after_time_challenge = 0  # NEW: Count crossings after time challenge
math_mode = False  # NEW: Flag for math problem mode
current_math_problem = None  # NEW: Store current math problem
math_answer_input = ""  # NEW: Store user's math answer input
time_limit_reached = False  # NEW: Flag for 5-minute time limit

# Function to create a lane
def create_lane(row, direction, base_speed, color, cars):
    return {
        "row": row,
        "direction": direction,
        "base_speed": base_speed,
        "color": color,
        "cars": cars
    }

# Function created for cars in lanes 
lanes = [
    create_lane(2, 1, 2, RED, [
        {"x": 0, "width": 80},
        {"x": 250, "width": 80},
        {"x": 500, "width": 80}
    ]),
    create_lane(3, -1, 3, BLUE, [
        {"x": 100, "width": 100},
        {"x": 400, "width": 100},
        {"x": 700, "width": 100}
    ]),
    create_lane(4, 1, 2.5, PURPLE, [
        {"x": 150, "width": 90},
        {"x": 450, "width": 90}
    ]),
    create_lane(6, -1, 3.5, ORANGE, [
        {"x": 50, "width": 70},
        {"x": 300, "width": 70},
        {"x": 550, "width": 70}
    ]),
    create_lane(7, 1, 2, RED, [
        {"x": 200, "width": 85},
        {"x": 500, "width": 85}
    ]),
    create_lane(8, -1, 4, BLUE, [
        {"x": 0, "width": 95},
        {"x": 350, "width": 95},
        {"x": 650, "width": 95}
    ]),
    create_lane(9, 1, 3, PURPLE, [
        {"x": 100, "width": 75},
        {"x": 400, "width": 75},
        {"x": 700, "width": 75}
    ])
]

# Function to generate a random math problem
def generate_math_problem():
    """Generate a simple math problem (addition, subtraction, or multiplication)"""
    operation = random.choice(["+", "-", "*"])
    
    if operation == "+":
        num1 = random.randint(1, 50)
        num2 = random.randint(1, 50)
        answer = num1 + num2
        question = f"{num1} + {num2} = ?"
    elif operation == "-":
        num1 = random.randint(10, 50)
        num2 = random.randint(1, num1)
        answer = num1 - num2
        question = f"{num1} - {num2} = ?"
    else:  # operation == "*"
        num1 = random.randint(2, 12)
        num2 = random.randint(2, 12)
        answer = num1 * num2
        question = f"{num1} × {num2} = ?"
    
    return {"question": question, "answer": answer}

# Game loop control variable
running = True

# Main game loop
while running:
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            # Handle time challenge input
            if time_challenge_active:
                if event.key == pygame.K_RETURN:
                    try:
                        guessed_minutes = int(user_time_guess)
                        actual_time_ms = pygame.time.get_ticks() - game_start_time
                        actual_minutes = actual_time_ms // 60000
                        actual_seconds = (actual_time_ms % 60000) // 1000
                        
                        user_guessed_time = guessed_minutes
                        actual_play_time = actual_minutes
                        actual_play_seconds = actual_seconds
                        
                        if abs(guessed_minutes - actual_minutes) <= 1:
                            time_guess_correct = True
                        else:
                            time_guess_correct = False
                        
                        time_challenge_active = False
                        show_time_result = True
                        
                    except ValueError:
                        user_guessed_time = 0
                        actual_time_ms = pygame.time.get_ticks() - game_start_time
                        actual_play_time = actual_time_ms // 60000
                        actual_play_seconds = (actual_time_ms % 60000) // 1000
                        time_guess_correct = False
                        time_challenge_active = False
                        show_time_result = True
                
                elif event.key == pygame.K_BACKSPACE:
                    user_time_guess = user_time_guess[:-1]
                
                elif event.unicode.isdigit() and len(user_time_guess) < 3:
                    user_time_guess = user_time_guess + event.unicode
            
            # Handle time result screen
            elif show_time_result:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    show_time_result = False
                    user_time_guess = ""
                    if time_guess_correct:
                        passed_time_challenge = True
                        crossings_after_time_challenge = 0
                    else:
                        game_over = True
            
            # Handle math mode input - break expectation of autonomy - make user solve math problems to deter from further game play
            elif math_mode:
                if event.key == pygame.K_RETURN:
                    try:
                        user_answer = int(math_answer_input)
                        if user_answer == current_math_problem["answer"]:
                            player_score = player_score + 50
                            current_math_problem = generate_math_problem()
                            math_answer_input = ""
                        else:
                            game_over = True
                            math_mode = False
                    except ValueError:
                        game_over = True
                        math_mode = False
                
                elif event.key == pygame.K_BACKSPACE:
                    math_answer_input = math_answer_input[:-1]
                
                elif event.key == pygame.K_MINUS and len(math_answer_input) == 0:
                    math_answer_input = "-"
                
                elif event.unicode.isdigit() and len(math_answer_input) < 5:
                    math_answer_input = math_answer_input + event.unicode
            
            # Only process movement if game is not over and not in time challenge
            elif not game_over:
                if event.key == pygame.K_UP:
                    player_row = player_row - 1
                    if player_row < 0:
                        player_row = 0
                
                elif event.key == pygame.K_DOWN:
                    player_row = player_row + 1
                    if player_row >= rows:
                        player_row = rows - 1
                
                elif event.key == pygame.K_LEFT:
                    player_col = player_col - 1
                    if player_col < 0:
                        player_col = 0
                
                elif event.key == pygame.K_RIGHT:
                    player_col = player_col + 1
                    if player_col >= cols:
                        player_col = cols - 1
            
            # Allow restart when game is over
            else:
                if event.key == pygame.K_r:
                    game_over = False
                    player_lives = 3
                    player_score = 0
                    player_row = 11
                    player_col = 7
                    difficulty_multiplier = 1.0
                    successful_crossings = 0
                    easy_mode = False
                    time_challenge_active = False
                    user_time_guess = ""
                    show_time_result = False
                    actual_play_time = 0
                    actual_play_seconds = 0
                    user_guessed_time = 0
                    time_guess_correct = False
                    passed_time_challenge = False
                    crossings_after_time_challenge = 0
                    math_mode = False
                    current_math_problem = None
                    math_answer_input = ""
                    time_limit_reached = False
    
    # Check if 5 minutes have passed
    if not time_limit_reached:
        current_time_ms = pygame.time.get_ticks() - game_start_time
        current_minutes = current_time_ms // 60000
        if current_minutes >= 5:
            time_limit_reached = True
            math_mode = False
    
    # Only update game logic if game is not over and not in time challenge
    if not game_over and not time_challenge_active and not show_time_result and not math_mode and not time_limit_reached:
        # Check if player reached the goal
        if player_row == 0:
            player_score = player_score + 100
            successful_crossings = successful_crossings + 1
            
            # Check if passed time challenge and counting post-challenge crossings
            if passed_time_challenge:
                crossings_after_time_challenge = crossings_after_time_challenge + 1
                if crossings_after_time_challenge >= 3:
                    math_mode = True
                    current_math_problem = generate_math_problem()
                    math_answer_input = ""
                    player_row = 11
                    player_col = 7
                    continue
            
            # Check if player has reached 8 crossings
            if successful_crossings == 8:
                time_challenge_active = True
                player_row = 11
                player_col = 7
                continue
            
            # Check if player has made 4 successful crossings
            if successful_crossings >= 4:
                if not easy_mode:
                    easy_mode = True # support expectation of competence - making game less challenging 
                    difficulty_multiplier = 0.6
                else:
                    difficulty_multiplier = difficulty_multiplier - 0.05
                    if difficulty_multiplier < 0.2:
                        difficulty_multiplier = 0.2
            else:
                difficulty_multiplier = difficulty_multiplier + 0.1
            
            player_row = 11
            player_col = 7
        
        # Update car positions
        for lane in lanes:
            for car in lane["cars"]:
                current_speed = lane["base_speed"] * difficulty_multiplier
                car["x"] = car["x"] + (lane["direction"] * current_speed)
                
                if lane["direction"] == 1:
                    if car["x"] > screen_width:
                        car["x"] = -car["width"]
                else:
                    if car["x"] + car["width"] < 0:
                        car["x"] = screen_width
        
        # Check for collisions
        player_pixel_x = player_col * grid_size
        player_pixel_y = player_row * grid_size
        player_hitbox_width = grid_size
        player_hitbox_height = grid_size
        
        for lane in lanes:
            if player_row == lane["row"]:
                car_y = lane["row"] * grid_size + 10
                car_height = 30
                
                for car in lane["cars"]:
                    car_x = car["x"]
                    car_width = car["width"]
                    
                    x_overlap = (player_pixel_x < car_x + car_width and 
                               player_pixel_x + player_hitbox_width > car_x)
                    y_overlap = (player_pixel_y < car_y + car_height and
                               player_pixel_y + player_hitbox_height > car_y)
                    
                    if x_overlap and y_overlap:
                        player_lives = player_lives - 1
                        
                        if player_lives <= 0:
                            game_over = True
                        else:
                            player_row = 11
                            player_col = 7
                        
                        break
    
    # Fill the screen with background color
    screen.fill(BLACK)
    
    # Display time limit reached screen (check this FIRST)
    if time_limit_reached:
        screen.fill(BLACK)
        
        big_font = pygame.font.Font(None, 60)
        medium_font = pygame.font.Font(None, 48)
        
        message1 = big_font.render("You've exercised your mind enough,", True, BRIGHT_YELLOW)
        msg1_x = (screen_width - message1.get_width()) // 2
        screen.blit(message1, (msg1_x, 220))
        
        message2 = big_font.render("go get some fresh air outside!", True, BRIGHT_YELLOW)
        msg2_x = (screen_width - message2.get_width()) // 2
        screen.blit(message2, (msg2_x, 290))
        
        final_score_text = medium_font.render(f"Final Score: {player_score}", True, WHITE)
        score_x = (screen_width - final_score_text.get_width()) // 2
        screen.blit(final_score_text, (score_x, 380))
    
    # Only draw game elements if time limit not reached
    elif not time_limit_reached:
        # Draw the lanes
        pygame.draw.rect(screen, DARK_GREEN, (0, 0, screen_width, grid_size))
        pygame.draw.rect(screen, GREEN, (0, grid_size * 1, screen_width, grid_size))
        pygame.draw.rect(screen, GRAY, (0, grid_size * 2, screen_width, grid_size))
        pygame.draw.rect(screen, GRAY, (0, grid_size * 3, screen_width, grid_size))
        pygame.draw.rect(screen, GRAY, (0, grid_size * 4, screen_width, grid_size))
        pygame.draw.rect(screen, GREEN, (0, grid_size * 5, screen_width, grid_size))
        pygame.draw.rect(screen, GRAY, (0, grid_size * 6, screen_width, grid_size))
        pygame.draw.rect(screen, GRAY, (0, grid_size * 7, screen_width, grid_size))
        pygame.draw.rect(screen, GRAY, (0, grid_size * 8, screen_width, grid_size))
        pygame.draw.rect(screen, GRAY, (0, grid_size * 9, screen_width, grid_size))
        pygame.draw.rect(screen, GREEN, (0, grid_size * 10, screen_width, grid_size))
        pygame.draw.rect(screen, GREEN, (0, grid_size * 11, screen_width, grid_size))
        
        # Draw grid lines
        for row in range(rows + 1):
            pygame.draw.line(screen, WHITE, (0, row * grid_size), (screen_width, row * grid_size), 1)
        
        for col in range(cols + 1):
            pygame.draw.line(screen, WHITE, (col * grid_size, 0), (col * grid_size, screen_height), 1)
        
        # Draw all cars
        for lane in lanes:
            car_y = lane["row"] * grid_size + 10
            car_height = 30
            
            for car in lane["cars"]:
                pygame.draw.rect(screen, lane["color"], 
                               (car["x"], car_y, car["width"], car_height))
                
                window_color = (0, 0, 0)
                pygame.draw.rect(screen, window_color,
                               (car["x"] + 10, car_y + 5, car["width"] - 20, 10))
        
        # Draw the gnome player
        player_x = player_col * grid_size + grid_size // 2
        player_y = player_row * grid_size + grid_size // 2
        
        body_width = 28
        body_height = 30
        pygame.draw.ellipse(screen, BROWN, 
                           (player_x - body_width // 2, 
                            player_y - 5, 
                            body_width, 
                            body_height))
        
        head_radius = 12
        pygame.draw.circle(screen, TAN, (player_x, player_y - 10), head_radius)
        
        hat_points = [
            (player_x - 15, player_y - 10),
            (player_x + 15, player_y - 10),
            (player_x, player_y - 35)
        ]
        pygame.draw.polygon(screen, RED, hat_points)
        
        pygame.draw.circle(screen, PINK, (player_x, player_y - 8), 3)
        
        beard_points = [
            (player_x - 10, player_y - 5),
            (player_x + 10, player_y - 5),
            (player_x, player_y + 8)
        ]
        pygame.draw.polygon(screen, WHITE, beard_points)
        
        # Display text
        font = pygame.font.Font(None, 36)
        
        lives_text = font.render(f"Lives: {player_lives}", True, WHITE)
        screen.blit(lives_text, (10, 10))
        
        score_text = font.render(f"Score: {player_score}", True, WHITE)
        score_text_width = score_text.get_width()
        screen.blit(score_text, (screen_width - score_text_width - 10, 10))
        
        # Draw easy mode indicator
        if easy_mode and not time_challenge_active and not show_time_result and not math_mode:
            easy_mode_text = font.render("EASY MODE!", True, BRIGHT_YELLOW)
            easy_mode_x = (screen_width - easy_mode_text.get_width()) // 2
            screen.blit(easy_mode_text, (easy_mode_x, 10))
        
        # Display math mode screen
        if math_mode:
            overlay = pygame.Surface((screen_width, screen_height))
            overlay.set_alpha(220)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            huge_font = pygame.font.Font(None, 80)
            big_font = pygame.font.Font(None, 72)
            medium_font = pygame.font.Font(None, 48)
            small_font = pygame.font.Font(None, 36)
            
            math_title = huge_font.render("MATH MODE!", True, PURPLE)
            title_x = (screen_width - math_title.get_width()) // 2
            screen.blit(math_title, (title_x, 80))
            
            problem_text = big_font.render(current_math_problem["question"], True, WHITE)
            problem_x = (screen_width - problem_text.get_width()) // 2
            screen.blit(problem_text, (problem_x, 200))
            
            input_box_width = 250
            input_box_height = 70
            input_box_x = (screen_width - input_box_width) // 2
            input_box_y = 320
            pygame.draw.rect(screen, WHITE, (input_box_x, input_box_y, input_box_width, input_box_height), 4)
            
            answer_text = medium_font.render(math_answer_input if math_answer_input else "_", True, WHITE)
            answer_x = (screen_width - answer_text.get_width()) // 2
            screen.blit(answer_text, (answer_x, input_box_y + 15))
            
            instruction1 = small_font.render("Solve the problem to earn 50 points!", True, BRIGHT_YELLOW)
            inst1_x = (screen_width - instruction1.get_width()) // 2
            screen.blit(instruction1, (inst1_x, 430))
            
            instruction2 = small_font.render("Press ENTER to submit", True, GREEN)
            inst2_x = (screen_width - instruction2.get_width()) // 2
            screen.blit(instruction2, (inst2_x, 480))
            
            instruction3 = small_font.render("Wrong answer = Game Over!", True, RED)
            inst3_x = (screen_width - instruction3.get_width()) // 2
            screen.blit(instruction3, (inst3_x, 520))
        
        # Display time result screen - support expectation of autonomy - makes user guess how long they have played, if correct can continue
        if show_time_result:
            overlay = pygame.Surface((screen_width, screen_height))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            big_font = pygame.font.Font(None, 72)
            medium_font = pygame.font.Font(None, 48)
            small_font = pygame.font.Font(None, 36)
            
            if time_guess_correct:
                result_text = big_font.render("CORRECT!", True, GREEN)
            else:
                result_text = big_font.render("WRONG!", True, RED)
            result_x = (screen_width - result_text.get_width()) // 2
            screen.blit(result_text, (result_x, 120))
            
            guess_display = medium_font.render(f"Your guess: {user_guessed_time} minutes", True, WHITE)
            guess_x = (screen_width - guess_display.get_width()) // 2
            screen.blit(guess_display, (guess_x, 220))
            
            actual_display = medium_font.render(f"Actual time: {actual_play_time} minutes {actual_play_seconds} seconds", True, BRIGHT_YELLOW)
            actual_x = (screen_width - actual_display.get_width()) // 2
            screen.blit(actual_display, (actual_x, 280))
            
            time_diff = abs(user_guessed_time - actual_play_time)
            diff_display = small_font.render(f"Difference: {time_diff} minute(s)", True, WHITE)
            diff_x = (screen_width - diff_display.get_width()) // 2
            screen.blit(diff_display, (diff_x, 350))
            
            if time_guess_correct:
                continue_text = medium_font.render("Press ENTER to continue playing!", True, GREEN)
            else:
                continue_text = medium_font.render("Press ENTER for game over", True, RED)
            continue_x = (screen_width - continue_text.get_width()) // 2
            screen.blit(continue_text, (continue_x, 450))
        
        # Display time challenge screen
        if time_challenge_active:
            overlay = pygame.Surface((screen_width, screen_height))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            big_font = pygame.font.Font(None, 60)
            medium_font = pygame.font.Font(None, 48)
            small_font = pygame.font.Font(None, 36)
            
            challenge_title = big_font.render("TIME CHALLENGE!", True, BRIGHT_YELLOW)
            title_x = (screen_width - challenge_title.get_width()) // 2
            screen.blit(challenge_title, (title_x, 150))
            
            instruction1 = medium_font.render("How many MINUTES have you been playing?", True, WHITE)
            inst1_x = (screen_width - instruction1.get_width()) // 2
            screen.blit(instruction1, (inst1_x, 230))
            
            instruction2 = small_font.render("(Guess within 1 minute to continue)", True, WHITE)
            inst2_x = (screen_width - instruction2.get_width()) // 2
            screen.blit(instruction2, (inst2_x, 280))
            
            input_box_width = 200
            input_box_height = 60
            input_box_x = (screen_width - input_box_width) // 2
            input_box_y = 350
            pygame.draw.rect(screen, WHITE, (input_box_x, input_box_y, input_box_width, input_box_height), 3)
            
            guess_text = medium_font.render(user_time_guess if user_time_guess else "_", True, WHITE)
            guess_x = (screen_width - guess_text.get_width()) // 2
            screen.blit(guess_text, (guess_x, input_box_y + 10))
            
            minutes_label = small_font.render("minutes", True, WHITE)
            minutes_x = (screen_width - minutes_label.get_width()) // 2
            screen.blit(minutes_label, (minutes_x, input_box_y + 70))
            
            enter_text = small_font.render("Press ENTER to submit", True, GREEN)
            enter_x = (screen_width - enter_text.get_width()) // 2
            screen.blit(enter_text, (enter_x, 480))
        
        # If game is over, display game over message
        if game_over:
            big_font = pygame.font.Font(None, 72)
            small_font = pygame.font.Font(None, 48)
            
            game_over_text = big_font.render("GAME OVER", True, RED)
            text_x = (screen_width - game_over_text.get_width()) // 2
            text_y = (screen_height - game_over_text.get_height()) // 2 - 50
            screen.blit(game_over_text, (text_x, text_y))
            
            final_score_text = small_font.render(f"Final Score: {player_score}", True, WHITE)
            score_x = (screen_width - final_score_text.get_width()) // 2
            score_y = text_y + 80
            screen.blit(final_score_text, (score_x, score_y))
            
            restart_text = small_font.render("Press R to Restart", True, WHITE)
            restart_x = (screen_width - restart_text.get_width()) // 2
            restart_y = score_y + 60
            screen.blit(restart_text, (restart_x, restart_y))
    
    # Update the display
    pygame.display.flip()
    
    # Control frame rate
    clock.tick(60)

# Clean up
pygame.quit()