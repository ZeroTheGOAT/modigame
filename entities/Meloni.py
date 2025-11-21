from entities.EntityBase import EntityBase

class Meloni(EntityBase):
    def __init__(self, screen, spriteCollection, x, y, gravity=0):
        super(Meloni, self).__init__(x, y, gravity)
        self.screen = screen
        self.spriteCollection = spriteCollection
        self.image = self.spriteCollection.get("meloni").image
        self.type = "Meloni"

    def update(self, cam):
        self.screen.blit(self.image, (self.rect.x + cam.x, self.rect.y))
