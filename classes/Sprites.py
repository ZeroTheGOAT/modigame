import json
import pygame

from classes.Animation import Animation
from classes.Sprite import Sprite
from classes.Spritesheet import Spritesheet


class Sprites:
    def __init__(self):
        self.spriteCollection = self.loadSprites(
            [
                "./sprites/Mario.json",
                "./sprites/Goomba.json",
                "./sprites/Koopa.json",
                "./sprites/Animations.json",
                "./sprites/BackgroundSprites.json",
                "./sprites/ItemAnimations.json",
                "./sprites/RedMushroom.json"
            ]
        )
        self.loadCustomSprites()

    def loadCustomSprites(self):
        # Load custom images
        character_img = pygame.image.load("./img/character.png")
        enemy_img = pygame.image.load("./img/enemy.png")
        happy_img = pygame.image.load("./img/happy_character.png")
        meloni_img = pygame.image.load("./img/meloni.png")

        # Scale images to standard sprite sizes (32x32 for small, 32x64 for big if needed, but let's stick to 32x32 for simplicity or match existing)
        # Mario small is 32x32
        char_small = pygame.transform.scale(character_img, (32, 32))
        char_big = pygame.transform.scale(character_img, (32, 64)) # Or just 32x32 if we don't want big mario visual difference other than size
        
        happy_small = pygame.transform.scale(happy_img, (32, 32))
        happy_big = pygame.transform.scale(happy_img, (32, 64))

        enemy_scaled = pygame.transform.scale(enemy_img, (32, 32))
        meloni_scaled = pygame.transform.scale(meloni_img, (32, 32)) # Meloni size?

        # Override Mario sprites
        # Small Mario
        self.spriteCollection["mario_idle"] = Sprite(char_small, True)
        self.spriteCollection["mario_run1"] = Sprite(char_small, True)
        self.spriteCollection["mario_run2"] = Sprite(char_small, True)
        self.spriteCollection["mario_run3"] = Sprite(char_small, True)
        self.spriteCollection["mario_jump"] = Sprite(char_small, True)

        # Big Mario
        self.spriteCollection["mario_big_idle"] = Sprite(char_big, True)
        self.spriteCollection["mario_big_run1"] = Sprite(char_big, True)
        self.spriteCollection["mario_big_run2"] = Sprite(char_big, True)
        self.spriteCollection["mario_big_run3"] = Sprite(char_big, True)
        self.spriteCollection["mario_big_jump"] = Sprite(char_big, True)

        # Happy Mario (Custom keys)
        self.spriteCollection["mario_happy_idle"] = Sprite(happy_small, True)
        self.spriteCollection["mario_happy_run1"] = Sprite(happy_small, True)
        self.spriteCollection["mario_happy_run2"] = Sprite(happy_small, True)
        self.spriteCollection["mario_happy_run3"] = Sprite(happy_small, True)
        self.spriteCollection["mario_happy_jump"] = Sprite(happy_small, True)
        
        self.spriteCollection["mario_big_happy_idle"] = Sprite(happy_big, True)
        self.spriteCollection["mario_big_happy_run1"] = Sprite(happy_big, True)
        self.spriteCollection["mario_big_happy_run2"] = Sprite(happy_big, True)
        self.spriteCollection["mario_big_happy_run3"] = Sprite(happy_big, True)
        self.spriteCollection["mario_big_happy_jump"] = Sprite(happy_big, True)

        # Override Goomba
        self.spriteCollection["goomba_run1"] = Sprite(enemy_scaled, True)
        self.spriteCollection["goomba_run2"] = Sprite(enemy_scaled, True)
        self.spriteCollection["goomba_flat"] = Sprite(pygame.transform.scale(enemy_img, (32, 16)), True) # Flattened

        # Override Koopa
        self.spriteCollection["koopa-1"] = Sprite(enemy_scaled, True)
        self.spriteCollection["koopa-2"] = Sprite(enemy_scaled, True)
        self.spriteCollection["koopa-hiding"] = Sprite(enemy_scaled, True) # Just use same image for simplicity or maybe a shell if available, but user said "enemy.jpg"
        self.spriteCollection["koopa-hiding-with-legs"] = Sprite(enemy_scaled, True)

        # Add Meloni
        self.spriteCollection["meloni"] = Sprite(meloni_scaled, True)


    def loadSprites(self, urlList):
        resDict = {}
        for url in urlList:
            with open(url) as jsonData:
                data = json.load(jsonData)
                mySpritesheet = Spritesheet(data["spriteSheetURL"])
                dic = {}
                if data["type"] == "background":
                    for sprite in data["sprites"]:
                        try:
                            colorkey = sprite["colorKey"]
                        except KeyError:
                            colorkey = None
                        dic[sprite["name"]] = Sprite(
                            mySpritesheet.image_at(
                                sprite["x"],
                                sprite["y"],
                                sprite["scalefactor"],
                                colorkey,
                            ),
                            sprite["collision"],
                            None,
                            sprite["redrawBg"],
                        )
                    resDict.update(dic)
                    continue
                elif data["type"] == "animation":
                    for sprite in data["sprites"]:
                        images = []
                        for image in sprite["images"]:
                            images.append(
                                mySpritesheet.image_at(
                                    image["x"],
                                    image["y"],
                                    image["scale"],
                                    colorkey=sprite["colorKey"],
                                )
                            )
                        dic[sprite["name"]] = Sprite(
                            None,
                            None,
                            animation=Animation(images, deltaTime=sprite["deltaTime"]),
                        )
                    resDict.update(dic)
                    continue
                elif data["type"] == "character" or data["type"] == "item":
                    for sprite in data["sprites"]:
                        try:
                            colorkey = sprite["colorKey"]
                        except KeyError:
                            colorkey = None
                        try:
                            xSize = sprite['xsize']
                            ySize = sprite['ysize']
                        except KeyError:
                            xSize, ySize = data['size']
                        dic[sprite["name"]] = Sprite(
                            mySpritesheet.image_at(
                                sprite["x"],
                                sprite["y"],
                                sprite["scalefactor"],
                                colorkey,
                                True,
                                xTileSize=xSize,
                                yTileSize=ySize,
                            ),
                            sprite["collision"],
                        )
                    resDict.update(dic)
                    continue
        return resDict
