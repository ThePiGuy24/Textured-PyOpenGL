print("Setting up...")
import pygame
print("Set up: 1/4")
import sys
print("Set up: 2/4")
from OpenGL.GL import *
print("Set up: 3/4")
from OpenGL.GLU import *
print("Set up: 4/4")
import time
import math

fps = 1

display = (800, 600)

vertices = (
	(-1,-1,0),
	(1,-1,0),
	(1,1,0),
	(-1,1,0)
)

vertices2 = (
	(0,-1,-1),
	(0,-1,1),
	(0,1,1),
	(0,1,-1)
)

vertices3 = (
	(-1,0,-1),
	(-1,0,1),
	(1,0,1),
	(1,0,-1)
)

uv = (
	(0.0,0.0),
	(1.0,0.0),
	(1.0,1.0),
	(0.0,1.0)
)

uv2 = (
	(1.0,0.0),
	(0.0,0.0),
	(0.0,1.0),
	(1.0,1.0)
)



def loadTexture():
	textureSurface = pygame.image.load('grid.png')
	textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
	width = textureSurface.get_width()
	height = textureSurface.get_height()

	glEnable(GL_TEXTURE_2D)
	texture = glGenTextures(1)

	glBindTexture(GL_TEXTURE_2D, texture)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
				 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

	return texture


def draw_poly(offset,vertCoords,uvCoords,col):
	glColor((col[0],col[1],col[2]))
	if len(vertCoords) == len(uvCoords):
		glBegin(GL_QUADS)
		for point in range(len(vertCoords)):
			glTexCoord2f(uvCoords[point][0],uvCoords[point][1])
			glVertex3f(vertCoords[point][0]+offset[0],vertCoords[point][1]+offset[1],vertCoords[point][2]+offset[2])
		glEnd()
		#pygame.display.flip()
		pass
	else:
		raise

def cube(offset=(0,0,0)):
	draw_poly((0+offset[0],0+offset[1],1+offset[2]),vertices,uv,(1,1,1))
	draw_poly((0+offset[0],0+offset[1],-1+offset[2]),vertices,uv2,(1,1,1))
	draw_poly((-1+offset[0],0+offset[1],0+offset[2]),vertices2,uv,(1,1,1))
	draw_poly((1+offset[0],0+offset[1],0+offset[2]),vertices2,uv2,(1,1,1))
	draw_poly((0+offset[0],1+offset[1],0+offset[2]),vertices3,uv,(1,1,1))
	draw_poly((0+offset[0],-1+offset[1],0+offset[2]),vertices3,uv2,(1,1,1))
		
pygame.init()
screen = pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL | pygame.OPENGLBLIT)

#oglsurf = pygame.Surface(display)

loadTexture()

gluPerspective(45, display[0] / display[1], 0.1, 100.0)

glEnable(GL_DEPTH_TEST)
glDepthMask(GL_TRUE)
glDepthFunc(GL_LEQUAL)
glDepthRange(0.0, 1.0)

glTranslatef(0.0, 0.0, -20)

clock = pygame.time.Clock()

t = time.time()

frame = 1

cfps = 0

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
	
	
	if frame >= fps:
		cfps = round(fps/(time.time()-t),1)
		print(str(cfps)+" fps")
		frame = 1
		t = time.time()
		fps = fps + 1
	else:
		frame = frame + 1
		
	
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	
	#for c in range(int(cfps)):
	for x in range(-10,10):
		for y in range(-10,10):
			draw_poly((x*2,-3,y*2),vertices3,uv2,(1,1,1))
			#cube((x*2,0,y*2))
	
	#screen.blit(oglsurf,(0,0))
	
	#clock.tick(fps)
	
	glRotatef(6/cfps,0,1,0.4)

	pygame.display.flip()
