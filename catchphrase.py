import pygame, sys

class CatchPhrase():
    def __init__(self, word_list, sound_name):
        self.screen = pygame.display.set_mode((1366, 768), pygame.FULLSCREEN)
        self.font = pygame.font.Font("times.ttf", 35)
        self.clock = pygame.time.Clock()
        self.word_file = open(word_list)
        pygame.mixer.music.load(sound_name)
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.mixer.music.set_volume(1.0)
        self.point_sound = pygame.mixer.Sound("point.wav")
        self.text_boxes = pygame.sprite.Group()
        self.word = TextBox(self, self.screen.get_rect().center, "")
        self.team1 = TextBox(self, [0, self.screen.get_rect().centery], "Team 1: 0")
        self.team2 = TextBox(self, [self.screen.get_width() - 140, self.screen.get_rect().centery], "Team 2: 0")
        self.score_team1 = 0
        self.score_team2 = 0
        self.startstop_button = TextBox(self, [self.screen.get_rect().centerx, 0], "Start/Stop")
        self.startstop_button.adjust(-self.startstop_button.rect.width/2, 0)
        self.playing = False
        self.next_button = TextBox(self, [self.screen.get_rect().centerx, self.screen.get_height() - 50], "Next")
        self.next_button.adjust(-self.next_button.rect.width/2, 0)
        self.loop()
    def loop(self):
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    changed = False
                    if self.next_button.rect.collidepoint(pygame.mouse.get_pos()) and self.playing:
                        self.update_word()
                        changed = True
                    elif self.team1.rect.collidepoint(pygame.mouse.get_pos()):
                        self.point_sound.play()
                        self.score_team1 += 1
                        if self.score_team1 > 7:
                            self.score_team1 = 0
                        self.text_boxes.remove(self.team1)
                        self.team1 = TextBox(self, [0, self.screen.get_rect().centery],\
                            "Team 1: " + str(self.score_team1))
                    elif self.team2.rect.collidepoint(pygame.mouse.get_pos()):
                        self.point_sound.play()
                        self.score_team2 += 1
                        if self.score_team2 > 7:
                            self.score_team2 = 0
                        self.text_boxes.remove(self.team2)
                        self.team2 = TextBox(self, [self.screen.get_width() - 140, self.screen.get_rect().centery],\
                            "Team 2: " + str(self.score_team2))
                    elif self.startstop_button.rect.collidepoint(pygame.mouse.get_pos()):
                        if not self.playing:
                            self.playing = True
                            self.update_word()
                            pygame.mixer.music.play()
                        else:
                            self.playing = False
                            pygame.mixer.music.stop()
                elif event.type == pygame.USEREVENT:
                    self.playing = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True
            self.screen.fill((0,0,0))
            #self.text_boxes.draw(self.screen)
            for text_box in self.text_boxes:
                text_box.draw()
            pygame.display.update()
            self.clock.tick(20)
        pygame.quit()
        sys.exit()
    def update_word(self):
        self.text_boxes.remove(self.word)
        self.word = TextBox(self, self.screen.get_rect().center, self.word_file.readline().strip('\n'))
        self.word.adjust(-self.word.rect.width/2, 0)

class TextBox(pygame.sprite.Sprite):
    def __init__(self, game, location, text):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        size = self.game.font.size(text)
        self.rect = pygame.Rect(location, size)#[location[0] - size[0] / 2, location[1] - size[1] / 2], size)
        self.image = pygame.Surface(size)
        self.image.fill((63,63,63))
        self.image.blit(self.game.font.render(text, True, (255, 255, 255)), (0,0))
        self.game.text_boxes.add(self)
    def adjust(self, x_adjust, y_adjust):
        self.rect.x += x_adjust
        self.rect.y += y_adjust
    def draw(self):
        self.game.screen.blit(self.image, self.rect)

if __name__ == '__main__':
    pygame.init()
    game = CatchPhrase("words.txt", "beeping.ogg")