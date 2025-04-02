import pygame
import os

class HighscoreManager:
    def __init__(self, filename='highscore.txt'):
        self.filename = os.path.join(os.path.dirname(__file__), filename)


    # Retrieve scores
    def get_highscores(self):
        try:
            with open(self.filename, 'r') as f:
                # Read lines and split into name and score
                scores = []
                for line in f:
                    try:
                        name, score = line.strip().split(',')
                        scores.append((name, int(score)))
                    except ValueError:
                        print(f"Skipping malformed line: {line}")
                        continue

                # Sort scores
                scores.sort(key=lambda x: x[1], reverse=True)
                return scores
        except (FileNotFoundError, IOError) as e:
            print(f"Error reading highscore file: {e}")
            # Create the file if it doesn't exist
            try:
                open(self.filename, 'w').close()
            except Exception as create_error:
                print(f"Error creating highscore file: {create_error}")
            return []


    # Sort top scores
    def add_highscore(self, name, score):
        scores = self.get_highscores()

        # Remove duplicates
        unique_scores = []
        seen = set()
        for existing_name, existing_score in scores:
            key = (existing_name, existing_score)
            if key not in seen:
                unique_scores.append(key)
                seen.add(key)
        unique_scores.append((name, score))

        # Keep top 5
        unique_scores.sort(key=lambda x: x[1], reverse=True)
        unique_scores = unique_scores[:5]

        # Overwrite with unique scores
        with open(self.filename, 'w') as f:
            for name, score in unique_scores:
                f.write(f"{name},{score}\n")


    # Prompt for initials
    def get_player_initials(self, screen, font):
        initials = ''
        input_active = True
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(initials) > 0:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        initials = initials[:-1]
                    elif event.key in range(pygame.K_a, pygame.K_z + 1) and len(initials) < 3:
                        initials += chr(event.key)

            screen.fill((0, 0, 0))

            title_text = font.render('Enter your initials', True, (255, 255, 255))
            input_text = font.render(initials, True, (255, 255, 255))
            instructions = font.render('Press ENTER to confirm', True, (200, 200, 200))

            title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
            input_rect = input_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            instructions_rect = instructions.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))

            screen.blit(title_text, title_rect)
            screen.blit(input_text, input_rect)
            screen.blit(instructions, instructions_rect)

            pygame.display.flip()

        return initials.upper()


    # Draw everything
    def draw_high_scores(self, screen, font):
        top_scores = self.get_highscores()

        # Clear screen
        screen.fill((0, 0, 0))

        # Title
        title_text = font.render("HIGH SCORES", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 50))
        screen.blit(title_text, title_rect)

        # Check and draw scores
        if not top_scores:
            no_scores_text = font.render("No high scores yet", True, (200, 200, 200))
            no_scores_rect = no_scores_text.get_rect(center=(screen.get_width() // 2, 200))
            screen.blit(no_scores_text, no_scores_rect)
        else:
            for i, (name, score) in enumerate(top_scores[:5], 1):
                score_text = font.render(f"{i}. {name}: {score}", True, (255, 255, 255))
                score_rect = score_text.get_rect(center=(screen.get_width() // 2, 100 + i * 50))
                screen.blit(score_text, score_rect)

        # Continue prompt
        continue_text = font.render("Press SPACE to restart", True, (200, 200, 200))
        continue_rect = continue_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
        screen.blit(continue_text, continue_rect)

        # Update display
        pygame.display.flip()



