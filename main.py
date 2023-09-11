import cv2,os,pygame
  
pygame.init()

window = pygame.display.set_mode((300,200))
buttons=[pygame.Rect(10,10,80,80),pygame.Rect(110,10,80,80),pygame.Rect(210,10,80,80)]
pygame.draw.rect(window,(0,255,0),buttons[0])
pygame.draw.rect(window,(255,0,0),buttons[1])
pygame.draw.rect(window,(255,255,255),buttons[2])
select=True
source = 0
max_source = 0
source_done = False
while not source_done:
    if cv2.VideoCapture(max_source+1).read()[0]:
        max_source+=1
    else:
        source_done=True
print(max_source)
vid = cv2.VideoCapture(source)
font = pygame.font.SysFont("Sans-Serif",20)
window.blit(font.render("Use the green and red buttons to go",True,(255,255,255)),(10,110))
window.blit(font.render("through the cameras connected. When",True,(255,255,255)),(10,130))
window.blit(font.render("you find the camera you want to use, click",True,(255,255,255)),(10,150))
window.blit(font.render("the white button.",True,(255,255,255)),(10,170))
while select:
    ret, frame = vid.read()
    cv2.imshow('frame', frame)

    for i in pygame.event.get():
        if i.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if buttons[0].collidepoint(mouse_position):
                vid.release()
                source = source+1 if source + 1 <max_source+1 else 0
                vid = cv2.VideoCapture(source)
            elif buttons[1].collidepoint(mouse_position):
                vid.release()
                source = source-1 if source - 1 > -1 else max_source
                vid = cv2.VideoCapture(source)
            elif buttons[2].collidepoint(mouse_position):
                select = False
    pygame.display.update()


window = pygame.display.set_mode((300,240))
buttons=[pygame.Rect(10,10,80,80),pygame.Rect(110,10,80,80),pygame.Rect(210,10,80,80)]
num = int(open("vidnum.txt").read())+1
print(num)
vid = cv2.VideoCapture(source)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(f'Videos/vid{num}.mp4', fourcc, 30.0, (640, 480))

pygame.draw.rect(window,(0,255,0),buttons[0])
pygame.draw.rect(window,(255,0,0),buttons[1])
pygame.draw.rect(window,(255,255,255),buttons[2])
window.blit(font.render("Use the green button to stop the",True,(255,255,255)),(10,110))
window.blit(font.render("recording and start a new one.",True,(255,255,255)),(10,130))
window.blit(font.render("Use the red button to stop and",True,(255,255,255)),(10,150))
window.blit(font.render("delete this recording. Use the",True,(255,255,255)),(10,170))
window.blit(font.render("white button to quit. Recordings",True,(255,255,255)),(10,190))
window.blit(font.render("start immediately after pressing the buttons.",True,(255,255,255)),(10,210))
go=True
while go:
    ret, frame = vid.read()
    cv2.imshow('frame', frame)
    out.write(frame)

    for i in pygame.event.get():
        if i.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if buttons[0].collidepoint(mouse_position):
                print('saving')
                vid.release()
                out.release()
                vid = cv2.VideoCapture(source)
                num+=1
                out = cv2.VideoWriter(f'Videos/vid{num}.mp4', fourcc, 30.0, (640, 480))
            elif buttons[1].collidepoint(mouse_position):
                print('deleting')
                vid.release()
                out.release()
                vid = cv2.VideoCapture(source)
                os.remove(f'Videos/vid{num}.mp4')
                out = cv2.VideoWriter(f'Videos/vid{num}.mp4', fourcc, 30.0, (640, 480))
            elif buttons[2].collidepoint(mouse_position):
                vid.release()
                out.release()
                with open('vidnum.txt','w') as a:
                    a.write(str(num-1))
                os.remove(f'Videos/vid{num}.mp4')
                go = False
    pygame.display.update()

  

cv2.destroyAllWindows()