from direct.showbase.ShowBase import ShowBase
from panda3d.core import DirectionalLight,AmbientLight,WindowProperties,CollisionTraverser,CollisionHandlerQueue,CollisionSphere,CollisionPolygon,LPoint3f,CollisionNode,CollisionBox,globalClock
from math import cos,sin,pi
import sys
import neat
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt # pyright: ignore[reportMissingModuleSource]

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.neat = True

        self.importModels()
        self.initCamera()
        self.initLights()
        self.initControls()
        self.initGame()

    def importModels(self):
        #Importation des modèle 3D
        self.mapModel = self.loader.loadModel("map_tuto.glb")
        self.playerModel = self.loader.loadModel("panda.glb")

    def initCamera(self):
        #Initialiser la caméra
        self.disableMouse()
        self.camLens.setFov(110)
        self.camera.setPos(382,270,129)
        self.camera.setHpr(110,-30,0)
        self.captureMouse()
        self.v,self.w = 50,3

    def initLights(self):
        #Lumière principale (Soleil)
        mainLight = DirectionalLight("MainLight")
        mainLightNodePath = self.render.attachNewNode(mainLight)
        mainLightNodePath.setHpr(30, -60, 0)
        self.render.setLight(mainLightNodePath)

        #Lumière Ambiante
        ambientLight = AmbientLight("AmbientLight")
        ambientLight.setColor((0.3, 0.3, 0.3, 1))
        ambientLightNodePath = self.render.attachNewNode(ambientLight)
        self.render.setLight(ambientLightNodePath)

        self.setBackgroundColor(0/255,191/255,255/255)

    def initControls(self):

        #Initialisation des binds

        self.keyMap = {
            "forward" : False,
            "left" : False,
            "right" : False,
            "backward" : False,
            "down" : False,
            "up" : False
        }

        self.accept("z", self.updateKeyMap, ["forward", True])
        self.accept("q", self.updateKeyMap, ["left", True])
        self.accept("s", self.updateKeyMap, ["backward", True])
        self.accept("d", self.updateKeyMap, ["right", True])
        self.accept("lshift", self.updateKeyMap, ["down", True])
        self.accept("space", self.updateKeyMap, ["up", True])

        self.accept("z-up", self.updateKeyMap, ["forward", False])
        self.accept("q-up", self.updateKeyMap, ["left", False])
        self.accept("s-up", self.updateKeyMap, ["backward", False])
        self.accept("d-up", self.updateKeyMap, ["right", False])
        self.accept("lshift-up", self.updateKeyMap, ["down", False])
        self.accept("space-up", self.updateKeyMap, ["up", False])

        self.accept("mouse1",self.captureMouse)
        self.accept("mouse3",self.releaseMouse)
        self.accept("mouse2",self.controlPlayer)

        if self.neat: #Neat Only
            self.accept("p", self.plot)
            self.accept("m",self.ticks)

    def updateKeyMap(self,key,value):
        self.keyMap[key] = value
    def controlPlayer(self):
        self.controlplayer = not self.controlplayer

    def captureMouse(self):
        #Incruster la souris dans l'écran
        self.into_screen = True
        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_relative)
        self.win.requestProperties(properties)
        coordSouris = self.win.getPointer(0)
        self.lastMouseX = coordSouris.getX()
        self.lastMouseY = coordSouris.getY()

    def releaseMouse(self):
        # La libérer
        self.into_screen = False
        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_relative)
        self.win.requestProperties(properties)

    def initGame(self):
        #Création et implantation des éléments du jeu
        self.generateTerrain()
        self.initColliders()

        if not self.neat: #Partie 1
            self.generatePlayer()
            self.taskMgr.add(self.updateCamera, "Update Camera")
            self.taskMgr.add(self.updatePlayer, "Update Player")
            self.taskMgr.add(self.updateCollisions, "Update Collisions")
            # self.displayCollisionNodes()

        else: #Partie 2
            self.initNeat()
            self.runNeat()

    def generateTerrain(self):
        self.terrain = self.render.attachNewNode("Terrain")  # Nouvelle Node
        self.terrain.setPos(0, 0, 0)  # Origine du Jeu
        self.terrain.setHpr(0, 90, 0)  # Orientation
        self.terrain.setScale(10)  # Taille
        self.mapModel.instanceTo(self.terrain)  # On affecte l'apparence de la Node au model terrain

    def generatePlayer(self):
        self.player = self.render.attachNewNode("Player")  # Nouvelle Node
        self.player.setPos(270, 242, 5)  # Origine du Jeu
        self.player.setHpr(-60, 90, 0)  # Orientation
        self.player.setScale(0.4)  # Taille
        self.playerModel.instanceTo(self.player)  # On affecte l'apparence de la Node au model terrain

        self.controlplayer = False
        self.fly = True
        self.vx = 0
        self.vy = 0
        self.vz = 0
        self.precx, self.precy, self.precz = 0, 0, 0

        #Après les collisions
        box = CollisionBox((-24, 13, -16), (20, 100, 16))
        node = CollisionNode("Player")
        node.addSolid(box)
        node.setFromCollideMask(1)
        node.setIntoCollideMask(2)
        path = self.player.attachNewNode(node)
        self.collisionNodes.append(path)
        self.traverser.addCollider(path, self.handler)

        box = CollisionBox((-24, 14, -16), (20, 100, 16))
        node = CollisionNode("Fly")
        node.addSolid(box)
        node.setFromCollideMask(1)
        node.setIntoCollideMask(2)
        path = self.player.attachNewNode(node)
        self.collisionNodes.append(path)
        self.traverser.addCollider(path, self.handler)

    def initColliders(self):

        def addPolygon(x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4,tag):
            polygon = CollisionPolygon(LPoint3f(x1, y1, z1),
                                       LPoint3f(x2, y2, z2),
                                       LPoint3f(x3, y3, z3),
                                       LPoint3f(x4, y4, z4)
                                       )

            node = CollisionNode(tag)
            node.addSolid(polygon)

            node.setFromCollideMask(0)
            node.setIntoCollideMask(1)

            path = self.render.attachNewNode(node)
            self.traverser.addCollider(path, self.handler)
            return path

        def addCube(x, y, z, dx, dy, dz, tag):
            cube = CollisionBox((x, y, z), dx, dy, dz)
            node = CollisionNode(tag)
            node.addSolid(cube)

            node.setFromCollideMask(0)
            node.setIntoCollideMask(1)

            path = self.render.attachNewNode(node)
            self.traverser.addCollider(path, self.handler)
            return path

        def addSphere(x, y, z, r, tag):
            cube = CollisionSphere(x,y,z,r)
            node = CollisionNode(tag)
            node.addSolid(cube)

            node.setFromCollideMask(0)
            node.setIntoCollideMask(1)

            path = self.render.attachNewNode(node)
            self.traverser.addCollider(path, self.handler)
            return path

        self.traverser = CollisionTraverser()
        self.handler = CollisionHandlerQueue()
        self.collisionNodes = []

        self.collisionNodes.append(addPolygon(314,314,10,311,-0.3,10,311,-0.3,26,314,314,26,"Wall"))
        self.collisionNodes.append(addPolygon(314,314,10,-2.6,315,10,-2.6,315,26,314,314,26,"Wall"))
        self.collisionNodes.append(addPolygon(-6, 0, 10, 311, -0.3, 10, 311, -0.3, 26, -6, 0, 26, "Wall"))
        self.collisionNodes.append(addPolygon(-6, 0, 10, -2.6, 315, 10, -2.6, 315, 26, -6, 0, 26, "Wall"))

        self.collisionNodes.append(addCube(115,165,49,20.5,20.5,40,"Wall"))
        self.collisionNodes.append(addPolygon(314, 314, 10, 311, -0.3, 10, -6, 0, 10, -2.6, 315, 10, "Floor"))
        self.collisionNodes.append(addPolygon(136,144,90,94,144,90,95,342,90,136,342,90,"Floor"))
        self.collisionNodes.append(addPolygon(136,374,10,95,374,10,95,415,10,136,415,10,"Floor"))

        self.collisionNodes.append(addCube(290,110,25,18,18,15,"Wall"))
        self.collisionNodes.append(addCube(39,49,25,18,18,15,"Wall"))
        self.collisionNodes.append(addCube(39,289,25,18,18,15,"Wall"))
        self.collisionNodes.append(addSphere(140,250,24,15,"Bomb"))
        self.collisionNodes.append(addCube(115,409,15,5,5,5,"Wall"))
        self.collisionNodes.append(addCube(136,165,40,1.5,8,50,"Ladder"))

        self.collisionNodes.append(addCube(290,110,41,18,18,1,"Floor"))
        self.collisionNodes.append(addCube(39,49,41,18,18,1,"Floor"))
        self.collisionNodes.append(addCube(39,289,41,18,18,1,"Floor"))

        self.collisionNodes.append(addCube(115,410,32,7,2,7,"Reward"))

        self.collisionNodes.append(addCube(113,377,12,22,7,1,"Score9"))
        self.collisionNodes.append(addCube(110,336,94,22,1,10,"Score8"))
        self.collisionNodes.append(addCube(109,302,94,22,1,10,"Score7"))
        self.collisionNodes.append(addCube(115,271,94,22,1,10,"Score6"))
        self.collisionNodes.append(addCube(115,225,94,22,1,10,"Score5"))
        self.collisionNodes.append(addCube(115,182,94,17,1,10,"Score4"))
        self.collisionNodes.append(addCube(138,164,75,3,18,1,"Score3"))
        self.collisionNodes.append(addCube(136,164,16,3,18,1,"Score2"))
        self.collisionNodes.append(addCube(171,178,16,2,20,25,"Score1"))

    def displayCollisionNodes(self):
        for node in self.collisionNodes:
            node.show()

    def updateCamera(self,task):

        #Gérer le mouvement de la caméra

        def degToRad(degrees):
            return degrees * (pi / 180.0)

        dt = globalClock.getDt()

        dx = 0
        dy = 0
        dz = 0

        if self.into_screen:

            coordSouris = self.win.getPointer(0)
            mouseX = coordSouris.getX()
            mouseY = coordSouris.getY()

            mouseChangeX = mouseX - self.lastMouseX
            mouseChangeY = mouseY - self.lastMouseY

            currentH = self.camera.getH()
            currentP = self.camera.getP()

            self.camera.setHpr(
                currentH - mouseChangeX * dt * self.w*3,
                min(90, max(-90, currentP - mouseChangeY * dt * self.w*3)),
                0
            )

            self.lastMouseX = mouseX
            self.lastMouseY = mouseY

            if not self.controlplayer:

                if self.keyMap['forward']:
                    dx -= dt * self.v * sin(degToRad(self.camera.getH()))
                    dy += dt * self.v * cos(degToRad(self.camera.getH()))
                if self.keyMap['backward']:
                    dx += dt * self.v * sin(degToRad(self.camera.getH()))
                    dy -= dt * self.v * cos(degToRad(self.camera.getH()))
                if self.keyMap['left']:
                    dx -= dt * self.v * cos(degToRad(self.camera.getH()))
                    dy -= dt * self.v * sin(degToRad(self.camera.getH()))
                if self.keyMap['right']:
                    dx += dt * self.v * cos(degToRad(self.camera.getH()))
                    dy += dt * self.v * sin(degToRad(self.camera.getH()))
                if self.keyMap['up']:
                    dz += dt * self.v
                if self.keyMap['down']:
                    dz -= dt * self.v

                self.camera.setPos(
                    self.camera.getX() + dx,
                    self.camera.getY() + dy,
                    self.camera.getZ() + dz
                )

            else:
                if not self.neat:
                    self.camera.setPos(
                        self.player.getX() + 70 * cos(degToRad(self.player.getH() + 90)),
                        self.player.getY() + 70 * sin(degToRad(self.player.getH() + 90)),
                        self.player.getZ() + 70,
                    )
                else:
                    self.camera.setPos(
                        self.players[0]["node"].getX() + 70 * cos(degToRad(self.players[0]["node"].getH() + 90)),
                        self.players[0]["node"].getY() + 70 * sin(degToRad(self.players[0]["node"].getH() + 90)),
                        self.players[0]["node"].getZ() + 70,
                    )


        # print(self.camera.getPos())
        # print(self.camera.getHpr())

        return task.cont

    def updatePlayer(self, task):

        def degToRad(degrees):
            return degrees * (pi / 180.0)

        dt = globalClock.getDt()

        if self.controlplayer:
            if self.keyMap['forward']:
                self.vx += self.v * sin(degToRad(self.player.getH())) * .007
                self.vy -= self.v * cos(degToRad(self.player.getH())) * .007
            if self.keyMap['backward']:
                self.vx -= self.v * sin(degToRad(self.player.getH())) * .007
                self.vy += self.v * cos(degToRad(self.player.getH())) * .007
            if self.keyMap['left']:
                self.player.setH(self.player.getH() + self.w)
            if self.keyMap['right']:
                self.player.setH(self.player.getH() - self.w)
            if self.keyMap['up'] and not self.fly and not self.inLadder:
                self.vz += self.v * 0.08

            self.vx = min(3, self.vx)
            self.vy = min(3, self.vy)
            self.vz = min(10, self.vz)

            self.vx = max(-3, self.vx)
            self.vy = max(-3, self.vy)
            self.vz = max(-10, self.vz)

            self.vx *= 0.93
            self.vy *= 0.93

            self.precx, self.precy, self.precz = self.player.getPos()

            self.player.setPos(
                self.player.getX() + self.vx * dt * 80,
                self.player.getY() + self.vy * dt * 80,
                self.player.getZ() + self.vz * dt * 80)

            self.camera.setH(self.player.getH() + 180)

            if self.fly:
                self.vz -= 0.30
            else:
                self.vz = max(0, self.vz)

        if self.player.getZ() < -100:
            self.player.setPos(270, 242, 5)  # Origine du Jeu
            self.player.setHpr(-60, 90, 0)  # Orientation

        return task.cont

    def updateCollisions(self, task):
        self.traverser.traverse(self.render)
        self.fly = True
        self.inLadder = False

        dt = globalClock.getDt()

        for idx in range(self.handler.getNumEntries()):

            entry = self.handler.getEntry(idx)

            intoNodePath = entry.getIntoNodePath()
            fromNodePath = entry.getFromNodePath()
            name_collided = intoNodePath.getName()
            name_collider = fromNodePath.getName()

            if name_collider == "Player" and name_collided == "Wall":
                self.player.setPos(
                    self.precx,
                    self.precy,
                    self.player.getZ()
                )

                self.vx *= -1.3
                self.vy *= -1.3

            if name_collider == "Player" and name_collided == "Floor":
                self.fly = False
                self.player.setZ(self.precz)

            if name_collider == "Fly" and name_collided == "Floor" and self.fly:
                self.player.setZ(self.player.getZ() + 3 * dt)

            if name_collider == "Player" and name_collided == "Ladder":
                self.player.setZ(self.player.getZ() + ((abs(self.vx) > 0.1) + (abs(self.vx) > 0.1)) * 50 * dt)
                self.vx, self.vy = 0, 0
                self.fly = False
                self.inLadder = True

            if name_collider == "Player" and name_collided == "Bomb":
                print("J'ai perdu")
                sys.exit()

            if name_collider == "Player" and name_collided == "Reward":
                print("J'ai gagné")
                sys.exit()

        return task.cont

    def initNeat(self):
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, "config.txt")
        self.config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,neat.DefaultStagnation, config_path)
        self.p = neat.Population(self.config)
        self.p.add_reporter(neat.StdOutReporter(True))
        self.reporter = neat.StatisticsReporter()
        self.p.add_reporter(self.reporter)

        self.controlplayer = False

        self.best_fitnesses = []
        self.mean_fitnesses = []

        self.alpha = 0.0
        self.omega = 8.0 #Durée d'une game en secondes

        # self.displayCollisionNodes()

        self.taskMgr.stop()
        self.taskMgr.add(self.updateCamera,"Update Camera")
        self.taskMgr.add(self.updatePlayerNeat, "Update Player")
        self.taskMgr.add(self.updateCollisionsNeat, "Update Collisions")
        self.taskMgr.add(self.verifFinPartie,"Vérification fin de Game")

    def runNeat(self):
        winner = self.p.run(self.playGame, 10000)
        print(f"Meilleur génome : {winner}")
        with open('best_model.pkl', 'wb') as f:
            pickle.dump(winner, f)
        sys.exit()

    def playGame(self,genomes,config):
        self.alpha = 0.0
        self.players = []

        idx = -1
        for _,g in genomes:
            idx += 1
            net = neat.nn.FeedForwardNetwork.create(g, config)
            self.players.append(self.generatePlayerNeat(idx,net))
            g.fitness = 0

        self.taskMgr.run()

        idx = -1
        for _, g in genomes:
            idx += 1
            if idx < len(self.players):
                g.fitness = self.players[idx]["score"]

        best_fitness = max([g.fitness for _, g in genomes])
        mean_fitnesses = np.mean(np.array([g.fitness for _, g in genomes]))

        self.best_fitnesses.append(best_fitness)
        self.mean_fitnesses.append(mean_fitnesses)

        for player in self.players:
            player["node"].removeNode()

    def generatePlayerNeat(self, i, net):

        nodeP = self.render.attachNewNode(f"Player{i}")  # Nouvelle Node
        nodeP.setPos(270, 242, 5)  # Origine du Jeu
        nodeP.setHpr(-60, 90, 0)  # Orientation
        nodeP.setScale(0.4)  # Taille
        self.playerModel.instanceTo(nodeP)  # On affecte l'apparence de la Node au model terrain

        box = CollisionBox((-24, 13, -16), (20, 100, 16))
        node = CollisionNode(f"Player{i}")
        node.addSolid(box)
        node.setFromCollideMask(1)
        node.setIntoCollideMask(2)
        path = nodeP.attachNewNode(node)
        self.traverser.addCollider(path, self.handler)

        box = CollisionBox((-24, 14, -16), (20, 100, 16))
        node = CollisionNode(f"Fly{i}")
        node.addSolid(box)
        node.setFromCollideMask(1)
        node.setIntoCollideMask(2)
        path = nodeP.attachNewNode(node)
        self.traverser.addCollider(path, self.handler)

        box = CollisionBox((60, -20, 80), (65, 60, 85))
        node = CollisionNode(f"Perception1{i}")
        node.addSolid(box)
        node.setFromCollideMask(1)
        node.setIntoCollideMask(2)
        path = nodeP.attachNewNode(node)
        self.traverser.addCollider(path, self.handler)

        box = CollisionBox((-60, -20, 80), (-65, 60, 85))
        node = CollisionNode(f"Perception2{i}")
        node.addSolid(box)
        node.setFromCollideMask(1)
        node.setIntoCollideMask(2)
        path = nodeP.attachNewNode(node)
        self.traverser.addCollider(path, self.handler)

        box = CollisionBox((-10, -20, 50), (10, 60, 55))
        node = CollisionNode(f"Perception3{i}")
        node.addSolid(box)
        node.setFromCollideMask(1)
        node.setIntoCollideMask(2)
        path = nodeP.attachNewNode(node)
        self.traverser.addCollider(path, self.handler)

        return {"node": nodeP, "vx": 0, "vy": 0, "vz": 0, "fly": True, "precx": 0, "precy": 0, "precz": 0, "net": net,
                "score": 0, "inLadder": False, "alive": True, "p1": 0, "p2": 0, "p3": 0}

    def updatePlayerNeat(self,task):

        def degToRad(degrees):
            return degrees * (pi / 180.0)

        dt = globalClock.getDt()
        self.alpha += dt

        for player in self.players:
            if player["alive"]:

                #Cas Random (Drôle):
                # choice = player["net"].activate([random.uniform(-2,2) for idx in range(12)])

                #Cas IA:
                state = [player["p1"],player["p2"],player["p3"]]
                for c in range(1,10):
                    if c == player["score"]:
                        state.append(1)
                    else:
                        state.append(0)

                choice = player["net"].activate(state)

                if choice[0] > 0:
                    player["vx"] += self.v * sin(degToRad(player["node"].getH()))*.007
                    player["vy"] -= self.v * cos(degToRad(player["node"].getH()))*.007
                if choice[1] > 0:
                    player["vx"] -= self.v * sin(degToRad(player["node"].getH()))*.007
                    player["vy"] += self.v * cos(degToRad(player["node"].getH()))*.007
                if choice[2] > 0:
                    player["node"].setH(player["node"].getH() + self.w)
                if choice[3] > 0:
                    player["node"].setH(player["node"].getH() - self.w)
                if choice[4] > 0 and not player["fly"] and not player["inLadder"]:
                    player["vz"] += self.v*0.08

                player["vx"] = min(3, player["vx"])
                player["vy"] = min(3, player["vy"])
                player["vz"] = min(10, player["vz"])

                player["vx"] = max(-3, player["vx"])
                player["vy"] = max(-3, player["vy"])
                player["vz"] = max(-10, player["vz"])

                player["vx"] *= 0.93
                player["vy"] *= 0.93

                player["precx"],player["precy"],player["precz"] = player["node"].getPos()

                player["node"].setPos(
                    player["node"].getX() + player["vx"]*dt*80,
                    player["node"].getY() + player["vy"]*dt*80,
                    player["node"].getZ() + player["vz"]*dt*80)

                if player["fly"]:
                    player["vz"] -= 0.30
                else:
                    player["vz"] = max(0,player["vz"])

                if player["node"].getZ() < -100:
                    player["alive"] = False
                    player["node"].removeNode()

        return task.cont

    def updateCollisionsNeat(self,task):

        dt = globalClock.getDt()

        for player in self.players:
            player["fly"] = True
            player["inLadder"] = False
            player["p1"] = 0
            player["p2"] = 0
            player["p3"] = 0

        self.traverser.traverse(self.render)

        for idx in range(self.handler.getNumEntries()):

            entry = self.handler.getEntry(idx)

            intoNodePath = entry.getIntoNodePath()
            fromNodePath = entry.getFromNodePath()
            name_collided = intoNodePath.getName()
            name_collider = fromNodePath.getName()

            if name_collider[:6] == "Player" and name_collided == "Wall":
                player = self.players[int(name_collider[6:])]
                player["node"].setPos(
                    player["precx"],
                    player["precy"],
                    player["node"].getZ()
                )

                player["vx"] *= -1.3
                player["vy"] *= -1.3

            if name_collider[:6] == "Player" and name_collided == "Floor":
                player = self.players[int(name_collider[6:])]
                player["fly"] = False
                player["node"].setZ(player["precz"])

            if name_collider[:3] == "Fly" and name_collided == "Floor":
                player = self.players[int(name_collider[3:])]
                if player["fly"]:
                    player["node"].setZ(player["node"].getZ() + 3 * dt)

            if name_collider[:6] == "Player" and name_collided == "Ladder":
                player = self.players[int(name_collider[6:])]
                player["node"].setZ(player["node"].getZ() + ((abs(player["vx"]) > 0.1) + (abs(player["vx"]) > 0.1)) * 50 * dt)
                player["vx"],player["vy"] = 0, 0
                player["fly"] = False
                player["inLadder"] = True

            if name_collider[:6] == "Player" and name_collided == "Bomb":
                player = self.players[int(name_collider[6:])]
                player["alive"] = False
                player["node"].removeNode()

            if name_collider[:6] == "Player" and name_collided == "Reward":
                player = self.players[int(name_collider[6:])]
                player["score"] = 10

            if name_collider[:6] == "Player" and name_collided[:5] == "Score":
                player = self.players[int(name_collider[6:])]
                player["score"] = max(player["score"],int(name_collided[5:]))

            if name_collider[:10] == "Perception":
                player = self.players[int(name_collider[11:])]
                p = name_collider[10]
                player[f"p{p}"] = 1

        return task.cont

    def verifFinPartie(self,task):
        bool = True
        for player in self.players:
            if player["alive"]:
                bool = False
        for player in self.players:
            if player["score"] == 10:
                bool = True
        if self.alpha >= self.omega:
            bool = True
        if bool:
            self.taskMgr.stop()
        return task.cont

    def ticks(self):
        print(f"Alpha : {self.alpha}, Omega : {self.omega}")

    def plot(self):
        plt.figure()
        plt.plot(self.best_fitnesses, label="Meilleure Fitness")
        plt.plot(self.mean_fitnesses, label="Fitness Moyenne")
        plt.title("Progression des IA")
        plt.xlabel("Parties")
        plt.ylabel("Qualité")
        plt.legend()
        plt.show()

jeu = Game()
jeu.run()