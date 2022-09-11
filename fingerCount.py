from unittest import result
import cv2
import mediapipe as mp

#captura do vídeo onde 0 é a câmera que será aberta
video = cv2.VideoCapture(0)

#variável de configuração
hand = mp.solutions.hands
#variável responsável pela detecção da mão dentro do vídeo com max_num_hands=1 para apenas uma mão se quiser mais mudar o número
Hand = hand.Hands(max_num_hands=1)
#variável de configuração onde o drawing é responsável por desenhar as ligações entre os pontos na mão
mpDraw = mp.solutions.drawing_utils

while True:
    check, img = video.read()
    # A imagem recebida da câmera vem no formato BGR aqui ela é convertida para RGB para ser processada pelo MediaPipe
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Processando a imagem da mão com MediaPipe
    results = Hand.process(imgRGB)
    # Extraindo informações ou coordenadas dos pontos da imagem da mão
    handsPoints = results.multi_hand_landmarks
    # Convertendo coordenadas de pontos em pixels
    # Pegando as dimensões da imagem da mão com as variáveis h de height(altura), w de width(largura) e a 3ª variável não precisa
    h, w, _ = img.shape
    # Criando um array que receberá o nome de pontos
    pontos = []

    # Essa condicional só será exacutada se a variável handPoints não estiver vazia
    if handsPoints:
        # For para percorrer a variável handsPoints retornando as coordenadas para cada ponto da imagem da mão
        for points in handsPoints:
            # Variável para desenhar os pontos dentro da imagem da mão
            mpDraw.draw_landmarks(img, points, hand.HAND_CONNECTIONS)
            # Identificando cada ponto isoladamente e suas coordenadas para criar uma lógica em cima delas criando um...
            # for para enumerar cada ponto da mão com a variável id que vai receber essa enumeração e outra...
            # variárel chamada cord que vai receber as coordenadas
            for id, cord in enumerate(points.landmark):
                # Variáveis que irão fazer a conversão dos landmarks(pontos da mão) em pixels
                cx, cy = int(cord.x*w), int(cord.y*h)
                # Enumerando os pontos da mão
                #cv2.putText(img, str(id), (cx, cy+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
                # X, 0.5, (255, 0, 0), 2)
                # Incrementando valor no array chamado pontos a cada frame
                pontos.append((cx, cy))
                # printando o array com todas as coordenadas dos pontos a cada frame
                #print(pontos)

        # Criando um segundo array chamado dedos contendo os pontos superiores de cada dedo exceto o polegar (pois terá uma lógica diferente)
        dedos = [8, 12, 16, 20]
        # Criando a variável contador que vai contar quantos dedos estão levantados
        contador = 0
        # Essa condicional só será executada se a variável points não estiver vazia
        if points:
            # Condicional com a lógica para o dedo polegar na posição 4 que é ponta do polegar no eixo x que é [0](eixo que mostra as informações na horizontal), pois o ponto superior dele tem que estar à direita, caso contrário, o polegar estará dobrado
            if pontos[4][0] < pontos[3][0]:
                contador +=1
            # Criando uma variável x para percorrer a variável/array dedos
            for x in dedos:
                # Condicional que verifica se o ponto superior é menor que os dois pontos abaixo no eixo y que é [1](eixo que mosta as informações na vertical) pois o ponto superior dos dedos tem que estar acima, caso contrário, o dedo esta abaixado.
                if pontos[x][1] < pontos[x-2][1]:
                    # Incrementado a variável contador com 1
                    contador +=1

        # printando a variável contador para ver quantos dedos estão levantados
        #print(contador)

        # Inserindo a lógica de contagem dos dedos dentro da imagem
        img = cv2.flip(img, 1)
        cv2.rectangle(img, (80, 10), (200, 110), (255, 0, 0), -1)
        cv2.putText(img, str(contador), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 5)


    img = cv2.flip(img, 1)
    img = cv2.flip(img, 1)
    cv2.imshow("Imagem", img)
    cv2.waitKey(1)