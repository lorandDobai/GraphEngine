import pygame,sys,math
from pygame.locals import *
pygame.init()
from algo.parcurgeri import ptg,ptbf,ptdf
from algo.arbori import generic,prim,kruskal
from algo.drumuri import djikstra,bellmanFord,floydWarshall
from algo.problema import ciclue

class Node(pygame.sprite.Sprite):
    SIZE = 45
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("res/node.png").convert_alpha()
        self.image.set_colorkey((255,255,255))
        self.image = pygame.transform.smoothscale(self.image,(Node.SIZE ,Node.SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = x,y
        self.val = None
        self.arc_list = []
        self.adj_list = []
        self.selected = False

    def set_node_number(self, val):
        self.val = val

    def draw(self,display):
        display.blit(self.image,self.rect)
        label = DrawApp.FONT.render(str(self.val), 1, (0,100,255))
        x =int((math.log10(self.val)+1))
        display.blit(label, (self.rect.center[0]-5*x,self.rect.center[1]-8))
        if self.selected:
            pygame.draw.circle(DrawApp.displaySurf,(0,255,0),self.rect.center,Node.SIZE//2+5,1)
    def set_selected(self,val):
        self.selected = val

class Arc():
    def __init__(self,start,end,start_node,end_node):

        self.val = None
        self.start_node = start_node
        self.end_node = end_node
        self.dx = end[0] - start[0]
        self.dy = end[1] - start[1]
        rads = math.atan2(-self.dy,self.dx)
        self.start = round(start[0]+Node.SIZE/2*math.cos(rads)), round(start[1]+Node.SIZE/2*math.sin(-rads))
        self.end = round(end[0]+Node.SIZE/2*math.cos(math.pi-rads)), round(end[1]+Node.SIZE/2*math.sin(math.pi-rads))

        self.arrow_heads = [round(self.end[0]+6.5*math.cos(math.pi-(rads-math.pi/6))),round(self.end[1]+6.5*math.sin(math.pi-(rads-math.pi/6)))],\
                            [round(self.end[0]+6.5*math.cos(math.pi-(rads+math.pi/6))),round(self.end[1]+6.5*math.sin(math.pi-(rads+math.pi/6)))]
        self.val = 0
    def set_arc_cost(self, val):
        self.val = val
    def draw(self,display):
        pygame.draw.aaline(display,(0,255,0),self.start,self.end)
        if(DrawApp.DIRECTED_GRAPH):
            pygame.draw.aaline(display,(0,255,0),self.end, self.arrow_heads[0])
            pygame.draw.aaline(display,(0,255,0),self.end, self.arrow_heads[1])
        if(DrawApp.WEIGHTED_ARCS):
            display.blit(DrawApp.myfont.render(str(self.val),1,(255,255,255)),((self.start[0]+self.end[0])//2,(self.start[1]+self.end[1])//2))

class Graf():
    def __init__(self,app):
        self.node_count = 1
        self.node_list = pygame.sprite.Group()
        self.arc_list = []
        self.nodeTouched = False
        self.firstPos = None
        self.adj_matrix=[]
        self.app = app

    def draw_nodes(self):
        for s in self.node_list:
            s.draw(DrawApp.displaySurf)

    def draw_arcs(self):
        for arc in self.arc_list:
            arc.draw(DrawApp.displaySurf)
    def draw(self):
        self.draw_nodes()
        self.draw_arcs()
    def release(self):
         self.nodeTouched = False
         for node in self.node_list:
             node.set_selected(False)
         self.firstPos = None
    def handle_node(self,node):
        l=pygame.sprite.spritecollide(node,self.node_list,False)

        if not l:
            node.set_node_number(self.node_count)
            self.node_list.add(node)
            for line in self.adj_matrix:
                line.extend([0])
            self.adj_matrix.append([0]*self.node_count)

            self.node_count+=1
            self.nodeTouched = False
            self.release()


        else:
            for node in self.node_list:
                node.set_selected(False)
            if self.nodeTouched == True:
                if(l[0].rect.center != self.firstPos.rect.center):
                    a = Arc(self.firstPos.rect.center,l[0].rect.center,self.firstPos,l[0])

                    if(DrawApp.WEIGHTED_ARCS):
                        self.app.weigh(a)
                    else:
                        a.set_arc_cost(1)
                    self.adj_matrix[self.firstPos.val-1][l[0].val-1]=a.val
                    if not DrawApp.DIRECTED_GRAPH:
                        self.adj_matrix[l[0].val-1][self.firstPos.val-1]=a.val
                    self.arc_list.append(a)
                    l[0].arc_list.append(a)
                    self.firstPos.arc_list.append(a)
                    self.firstPos.adj_list.append(l[0])

                    self.firstPos = l[0]
                    self.firstPos.set_selected(True)
            else:
                self.firstPos = l[0]
                self.firstPos.set_selected(True)
                self.nodeTouched = True


class Button(object):
    def __init__(self,rect,label,color,value):
        self.rect = rect
        self.label = label
        self.color = color
        self.value = value
    def draw(self):
         pygame.draw.rect(DrawApp.displaySurf,self.color,self.rect,2)
         DrawApp.displaySurf.blit(self.label, (self.rect.topleft[0]+self.rect.width/2-self.label.get_width()//2,self.rect.topleft[1]+7))
    def is_clicked(self,pos):
        return self.rect.collidepoint(pos)
class DrawApp(object):

    WINDOW_HEIGHT = 600
    WINDOW_WIDTH = 800
    displaySurf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    fpsClock = pygame.time.Clock()
    FPS = 120
    FONT = pygame.font.SysFont("arialb", 25)
    myfont = pygame.font.SysFont("monospace", 12)
    DIRECTED_GRAPH = True
    WEIGHTED_ARCS = False
    def __init__(self):
        DrawApp.WINDOW_WIDTH = 970
        DrawApp.WINDOW_HEIGHT = 670
        DrawApp.displaySurf = pygame.display.set_mode((DrawApp.WINDOW_WIDTH, DrawApp.WINDOW_HEIGHT))
        pygame.display.set_caption("GraphDraw")
        self.node_list= pygame.sprite.Group()
        self.arc_list= []
        self.node_count = 1
        self.nodeTouched = False
        self.background_image = pygame.image.load("res/back2.jpg").convert_alpha()
        self.background_image.fill((128, 128, 128, 220), None, pygame.BLEND_RGBA_MULT)
        self.graf = Graf(self)
        
        self.buttons = [Button(pygame.Rect(830,20,120,30),DrawApp.FONT.render("PTG",1,(255,250,255)),(255,250,255),"ptg"),
                        Button(pygame.Rect(830,70,120,30),DrawApp.FONT.render("PTBF",1,(255,250,255)),(255,250,255),"ptbf"),
                        Button(pygame.Rect(830,120,120,30),DrawApp.FONT.render("PTDF",1,(255,250,255)),(255,250,255),"ptdf"),
                        Button(pygame.Rect(830,170,120,30),DrawApp.FONT.render("Generic",1,(255,250,255)),(255,250,255),"generic"),
                        Button(pygame.Rect(830,220,120,30),DrawApp.FONT.render("Prim",1,(255,250,255)),(255,250,255),"prim"),
                        Button(pygame.Rect(830,270,120,30),DrawApp.FONT.render("Kruskal",1,(255,250,255)),(255,250,255),"kruskal"),
                        Button(pygame.Rect(830,320,120,30),DrawApp.FONT.render("Djikstra",1,(255,250,255)),(255,250,255),"djikstra"),
                        Button(pygame.Rect(830,370,120,30),DrawApp.FONT.render("Bellman-Ford",1,(255,250,255)),(255,250,255),"bf"),
                        Button(pygame.Rect(830,420,120,30),DrawApp.FONT.render("Floyd-W.",1,(255,250,255)),(255,250,255),"floyd_w"),
                        Button(pygame.Rect(830,470,120,30),DrawApp.FONT.render("Ciclu Eu.",1,(255,250,255)),(255,250,255),"ciclue")
                        ]
        
        self.s_console = Pane(pygame.Rect(830,530,120,30),(200,200,200))
        self.s_console.add_text("s=")
        self.s = ""
        self.ok_button =  Button(pygame.Rect(830,580,120,30),DrawApp.FONT.render("Go",1,(255,250,255)),(255,250,255),"go")
        self.draw_zone = pygame.Rect(0,0,800,550)
        self.OPTION = None
        self.options= {"ptg":ptg.ptg,"ptbf":ptbf.ptbf,"ptdf":ptdf.ptdf,"generic":generic.arbore_minim_generic,"prim":prim.arbore_minim_prim,\
                       "kruskal":kruskal.kruskal,"djikstra":djikstra.djikstra,"bf":bellmanFord.bellman_ford,"floyd_w":floydWarshall,"ciclue":ciclue.ciclue}
        self.console = Pane(pygame.Rect(0,550,800,120),(200,200,200))
        self.arc_to_weigh = None

    def main_loop(self):
        while True:
            DrawApp.displaySurf.fill((10,10,10))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    self.handle_event(event)
            DrawApp.displaySurf.set_alpha(100)
            DrawApp.displaySurf.blit(self.background_image,(0,0))
            DrawApp.displaySurf.set_alpha(255)

            self.graf.draw()
            for b in self.buttons:
                b.draw()
            self.ok_button.draw()
            self.console.draw()
            self.s_console.draw()
            pygame.display.update()
            DrawApp.fpsClock.tick(DrawApp.FPS)

    def handle_event(self,event):

        if event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.graf.release()
            elif(self.arc_to_weigh):
                self.input+=chr(event.key)
                self.console.add_text("b({},{}) = {}".format(self.arc_to_weigh.start_node.val,self.arc_to_weigh.end_node.val,self.input))
            elif self.s_console.selected:
                self.s += chr(event.key)
                self.s_console.add_text("s= "+self.s)
            if event.key == pygame.K_RETURN:
                self.arc_to_weigh.set_arc_cost(int(self.input))
                self.graf.adj_matrix[self.arc_to_weigh.start_node.val-1][self.arc_to_weigh.end_node.val-1] = self.arc_to_weigh.val
                if(not DrawApp.DIRECTED_GRAPH):
                    self.graf.adj_matrix[self.arc_to_weigh.end_node.val-1][self.arc_to_weigh.start_node.val-1] = self.arc_to_weigh.val
                print(self.arc_to_weigh.val)
                self.arc_to_weigh = None
                self.console.add_text("")
            if event.key == pygame.K_s:
                with open("out.txt","w") as fout:
                    fout.write("\n".join(' '.join(map(str,line)) for line in self.graf.adj_matrix))
            if event.key == pygame.K_F5:
                self.graf.node_list = pygame.sprite.Group()
                self.graf.arc_list = []
                self.graf.firstPos = None
                self.node_count = 1

        if event.type == MOUSEBUTTONDOWN:
            if(self.draw_zone.collidepoint(event.pos)):
                n = Node(*event.pos)
                self.graf.handle_node(n)
                self.s_console.select(False)
            elif self.ok_button.is_clicked(event.pos):
                if self.OPTION!=None :
                    self.execute_selected_algorithm()
            elif self.s_console.rect.collidepoint(event.pos):
                self.s_console.select(True)
            else:
                for button in self.buttons:
                    button.color = (255,250,255)
                    if button.is_clicked(event.pos):
                        button.color = (0,255,0)
                        self.OPTION = button.value

    def execute_selected_algorithm(self):
        algo = self.options[self.OPTION]
        if not self.s:
            self.s = '1'
        res = algo(self.graf.adj_matrix,int(self.s)-1)
        self.console.add_text(str(res))
        if(self.OPTION in ["kruskal","generic","prim"]):
            self.graf.arc_list = [arc for arc in self.graf.arc_list if (min(arc.start_node.val,arc.end_node.val),max((arc.start_node.val,arc.end_node.val))) in res["T"]]
        if(self.OPTION in ["ptdf","ptbf","ptg"]):
             p = res["p"]
             #arcs_keep = [(i,j) for i,j in enumerate(p)]
             arcs_keep = [(j,i+1) for i,j in enumerate(p) if j!= 0]
             print(arcs_keep)
             self.graf.arc_list = [arc for arc in self.graf.arc_list if (arc.start_node.val,arc.end_node.val) in arcs_keep]

        if(self.OPTION in ["djikstra","bf","floyd_w"]):
            p = res["p"]
            print(p)
            arcs_keep = [(j+1,i+1) for i,j in enumerate(p) if j!= None]
            print(arcs_keep)
            self.graf.arc_list = [arc for arc in self.graf.arc_list if (arc.start_node.val,arc.end_node.val) in arcs_keep]
        if(self.OPTION  == "ciclue"):
            if res["W"][0] == res["W"][-1]:
                self.console.add_text(str(res)+" "+"Exista ciclu!")
            else:
                self.console.add_text(str(res)+" "+"Nu exista ciclu!")







    def weigh(self,arc):
        self.arc_to_weigh = arc
        self.input = ""
        self.console.add_text("b({},{}) = {}".format(self.arc_to_weigh.start_node.val,self.arc_to_weigh.end_node.val,self.input))


class Pane(object):
    def __init__(self,rect,color):
        self.rect = rect
        self.color = color
        self.text = ''
        self.selected = False
    def draw(self):
        pygame.draw.rect(DrawApp.displaySurf,self.color,self.rect,0)
        pygame.draw.rect(DrawApp.displaySurf,(50,50,70),self.rect,4)
        DrawApp.displaySurf.blit(DrawApp.myfont.render(self.text,1,(5,5,5)),(self.rect.topleft[0]+5,self.rect.topleft[1]+5))
    def add_text(self,text):
        self.text = text
    def select(self,val):
        self.selected = val

def main_menu():
    myfont = pygame.font.SysFont("monospace", 30)
    myfont2 = pygame.font.SysFont("arialnb", 60)

    labelTitle = myfont2.render("GraphEngine by Lorand Dobai",1, (55,50,255))

    OrientedOption = {"rect":pygame.Rect(300, 100, 190, 50),'label' : myfont.render("Orientat", 1, (225,250,225)),'color':(10,170,10)}
    UnOrientedOption = {"rect":pygame.Rect(500, 100, 190, 50),'label' : myfont.render("Neorientat", 1, (225,250,225)),'color':(55,50,255)}

    background_image = pygame.image.load("res/back.jpg").convert_alpha()
    background_image.fill((128, 128, 128, 220), None, pygame.BLEND_RGBA_MULT)

    withCostOption ={"rect":pygame.Rect(300,240, 190, 50),'label': myfont.render("Cu cost", 1, (225,250,225)),'color':(55,50,255)}
    withoutCostOption ={"rect":pygame.Rect(500,240, 190, 50),'label': myfont.render("Fara cost", 1, (225,250,225)),'color':(10,170,10)}


    labelGo = myfont.render("OK", 1,(255,250,255))
    okBtn = pygame.Rect(280,400, 190, 50)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            else:
                if event.type == MOUSEBUTTONDOWN:
                    if OrientedOption["rect"].collidepoint(event.pos):
                        OrientedOption["color"]=(10,170,10)
                        UnOrientedOption["color"] = (55,50,255)
                        DrawApp.DIRECTED_GRAPH= True
                    elif UnOrientedOption["rect"].collidepoint(event.pos):
                        UnOrientedOption["color"]=(10,170,10)
                        OrientedOption["color"] = (55,50,255)
                        DrawApp.DIRECTED_GRAPH=False
                    elif withCostOption["rect"].collidepoint(event.pos):
                        withCostOption["color"]=(10,170,10)
                        withoutCostOption["color"] = (55,50,255)
                        DrawApp.WEIGHTED_ARCS = True
                    elif withoutCostOption["rect"].collidepoint(event.pos):
                        withoutCostOption["color"]=(10,170,10)
                        withCostOption["color"] = (55,50,255)
                        DrawApp.WEIGHTED_ARC = False
                    elif okBtn.collidepoint(event.pos):
                        app = DrawApp()
                        app.main_loop()

        DrawApp.displaySurf.fill((255,255,255))
        DrawApp.displaySurf.blit(background_image,(0,0))
        
        pygame.draw.rect(DrawApp.displaySurf,OrientedOption["color"],OrientedOption["rect"],2)
        pygame.draw.rect(DrawApp.displaySurf,UnOrientedOption["color"],UnOrientedOption["rect"],2)
        pygame.draw.rect(DrawApp.displaySurf,withCostOption["color"],withCostOption["rect"],2)
        pygame.draw.rect(DrawApp.displaySurf,withoutCostOption["color"],withoutCostOption["rect"],2)
        pygame.draw.rect(DrawApp.displaySurf,(255,250,255),okBtn,2)
        DrawApp.displaySurf.blit( myfont.render("Tip graf: ", 1, (225,250,225)), (OrientedOption["rect"].topleft[0]-175,OrientedOption["rect"].topleft[1]+10))
        DrawApp.displaySurf.blit( myfont.render("Arce/Muchii: ", 1, (225,250,225)), (OrientedOption["rect"].topleft[0]-230,OrientedOption["rect"].topleft[1]+150))

        DrawApp.displaySurf.blit(OrientedOption["label"], (OrientedOption["rect"].topleft[0]+16,OrientedOption["rect"].topleft[1]+10))
        DrawApp.displaySurf.blit(UnOrientedOption["label"], (UnOrientedOption["rect"].topleft[0]+10,UnOrientedOption["rect"].topleft[1]+10))
        DrawApp.displaySurf.blit(withCostOption["label"], (withCostOption["rect"].topleft[0]+10,withCostOption["rect"].topleft[1]+10))
        DrawApp.displaySurf.blit(withoutCostOption["label"], (withoutCostOption["rect"].topleft[0]+10,withoutCostOption["rect"].topleft[1]+10))
        DrawApp.displaySurf.blit(labelGo, (okBtn.topleft[0]+80,okBtn.topleft[1]+10))
        DrawApp.displaySurf.blit(labelTitle,((DrawApp.displaySurf.get_width()-labelTitle.get_width())/2,20))
        pygame.display.update()

if __name__ == '__main__':
    #app = DrawApp()
    #app.main_loop()
    main_menu()
