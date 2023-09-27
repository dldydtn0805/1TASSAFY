import socket
import time
import math

# 닉네임을 사용자에 맞게 변경해 주세요.
NICKNAME = 'KIM YEOUG JUN'

# 일타싸피 프로그램을 로컬에서 실행할 경우 변경하지 않습니다.
HOST = '127.0.0.1'

# 일타싸피 프로그램과 통신할 때 사용하는 코드값으로 변경하지 않습니다.
PORT = 1447
CODE_SEND = 9901
CODE_REQUEST = 9902
SIGNAL_ORDER = 9908
SIGNAL_CLOSE = 9909


# 게임 환경에 대한 상수입니다.
TABLE_WIDTH = 254
TABLE_HEIGHT = 127
NUMBER_OF_BALLS = 6
HOLES = [[0, 0], [127, 0], [254, 0], [0, 127], [127, 127], [254, 127]]

order = 0
balls = [[0, 0] for i in range(NUMBER_OF_BALLS)]

sock = socket.socket()
print('Trying to Connect: %s:%d' % (HOST, PORT))
sock.connect((HOST, PORT))
print('Connected: %s:%d' % (HOST, PORT))

send_data = '%d/%s' % (CODE_SEND, NICKNAME)
sock.send(send_data.encode('utf-8'))
print('Ready to play!\n--------------------')


while True:

    # Receive Data
    recv_data = (sock.recv(1024)).decode()
    print('Data Received: %s' % recv_data)

    # Read Game Data
    split_data = recv_data.split('/')
    idx = 0
    try:
        for i in range(NUMBER_OF_BALLS):
            for j in range(2):
                balls[i][j] = float(split_data[idx])
                idx += 1
    except:
        send_data = '%d/%s' % (CODE_REQUEST, NICKNAME)
        print("Received Data has been currupted, Resend Requested.")
        continue

    # Check Signal for Player Order or Close Connection
    if balls[0][0] == SIGNAL_ORDER:
        order = int(balls[0][1])
        print('\n* You will be the %s player. *\n' % ('first' if order == 1 else 'second'))
        continue
    elif balls[0][0] == SIGNAL_CLOSE:
        break

    # Show Balls' Position
    print('====== Arrays ======')
    for i in range(NUMBER_OF_BALLS):
        print('Ball %d: %f, %f' % (i, balls[i][0], balls[i][1]))
    print('====================')

    angle = 0.0
    power = 0.0

    ##############################
    # 이 위는 일타싸피와 통신하여 데이터를 주고 받기 위해 작성된 부분이므로 수정하면 안됩니다.
    #
    # 모든 수신값은 변수, 배열에서 확인할 수 있습니다.
    #   - order: 1인 경우 선공, 2인 경우 후공을 의미
    #   - balls[][]: 일타싸피 정보를 수신해서 각 공의 좌표를 배열로 저장
    #     예) balls[0][0]: 흰 공의 X좌표
    #         balls[0][1]: 흰 공의 Y좌표
    #         balls[1][0]: 1번 공의 X좌표
    #         balls[4][0]: 4번 공의 X좌표
    #         balls[5][0]: 마지막 번호(8번) 공의 X좌표

    # 여기서부터 코드를 작성하세요.
    # 아래에 있는 것은 샘플로 작성된 코드이므로 자유롭게 변경할 수 있습니다.

    # 목적구를 따질 target과, 공의 반지름 r을 선언
    target = 0
    r = 5.73 / 2
    # order가 1일 경우 (5~6 스테이지 + 대결) 1, 3, 8이 목적구
    if order == 1:
        target = 1
    # order가 2일 경우 (5~6 스테이지 + 대결) 2, 4, 8이 목적구
    elif order == 2:
        target = 2

    # 1. 내 공과 홀 그리고 목적구 3개의 각각의 거리를 구한다.
    # whiteBall_x, whiteBall_y: 흰 공의 X, Y좌표를 나타내기 위해 사용한 변수
    whiteBall_x = balls[0][0]
    whiteBall_y = balls[0][1]

    if balls[target][0] == -1 and balls[target][1] == -1:
        if target == 1:
            target = 3
        elif target == 3 or target == 4:
            target = 5
        elif target == 2:
            target = 4

    # targetBall_x, targetBall_y: 목적구의 X, Y좌표를 나타내기 위해 사용한 변수
    targetBall_x = balls[target][0]
    targetBall_y = balls[target][1]


    print(target, balls[target][0], balls[target][1])

    # 목적구와 가까운 홀 좌표 찾기. 4 방향으로 나눠서 따지기
    tmp_hole_x = 500
    tmp_hole_y = 500
    tmp_hole_sum = 1000
    for h in HOLES:
        if whiteBall_x > targetBall_x:
            if h[0] < whiteBall_x and h[0] < targetBall_x:
                tmp_x = abs(h[0] - targetBall_x)
                tmp_y = abs(h[1] - targetBall_y)
                tmp_sum = tmp_x + tmp_y
                if tmp_hole_sum > tmp_sum:
                    tmp_hole_x = h[0]
                    tmp_hole_y = h[1]
                    tmp_hole_sum = tmp_sum

        elif whiteBall_x < targetBall_x:
            if h[0] > whiteBall_x and h[0] > targetBall_x:
                tmp_x = abs(h[0] - targetBall_x)
                tmp_y = abs(h[1] - targetBall_y)
                tmp_sum = tmp_x + tmp_y
                if tmp_hole_sum > tmp_sum:
                    tmp_hole_x = h[0]
                    tmp_hole_y = h[1]
                    tmp_hole_sum = tmp_sum

        elif whiteBall_y > targetBall_y:
            if h[0] < whiteBall_y and h[0] < targetBall_y:
                tmp_x = abs(h[0] - targetBall_x)
                tmp_y = abs(h[1] - targetBall_y)
                tmp_sum = tmp_x + tmp_y
                if tmp_hole_sum > tmp_sum:
                    tmp_hole_x = h[0]
                    tmp_hole_y = h[1]
                    tmp_hole_sum = tmp_sum

        elif whiteBall_y < targetBall_y:
            if h[0] > whiteBall_y and h[0] > targetBall_y:
                tmp_x = abs(h[0] - targetBall_x)
                tmp_y = abs(h[1] - targetBall_y)
                tmp_sum = tmp_x + tmp_y
                if tmp_hole_sum > tmp_sum:
                    tmp_hole_x = h[0]
                    tmp_hole_y = h[1]
                    tmp_hole_sum = tmp_sum

    else:
        hole_x = tmp_hole_x
        hole_y = tmp_hole_y

        print(hole_x, hole_y)

    # width_a_h, height_a_h: 홀과 흰 공의 X좌표 간의 거리, Y좌표 간의 거리
    width_a_h = abs(hole_x - whiteBall_x)
    height_a_h = abs(hole_y - whiteBall_y)
    a_h = math.sqrt(width_a_h**2 + height_a_h**2)

    # width_a_t, height_a_t: 목적구와 흰 공의 X좌표 간의 거리, Y좌표 간의 거리
    width_a_t = abs(targetBall_x - whiteBall_x)
    height_a_t = abs(targetBall_y - whiteBall_y)
    a_t = math.sqrt(width_a_t**2 + height_a_t**2)

    # width_t_h, height_t_h: 목적구와 흰 공의 X좌표 간의 거리, Y좌표 간의 거리
    width_t_h = abs(targetBall_x - hole_x)
    height_t_h = abs(targetBall_y - hole_y)
    t_h = math.sqrt(width_t_h**2 + height_t_h**2)

# 2. 내 공과 홀까지의 각도 구하기
    # radian: width와 height를 두 변으로 하는 직각삼각형의 각도를 구한 결과
    #   - 1radian = 180 / PI (도)
    #   - 1도 = PI / 180 (radian)
    # angle: 아크탄젠트로 얻은 각도 radian을 degree로 환산한 결과

    radian_a_h = math.atan(width_a_h / height_a_h) if height_a_h > 0 else 0
    angle_a_h = math.degrees(radian_a_h)


# 3. 홀과 목적구의 각도 구하기
    radian_t_h = math.acos(round((a_h**2 + t_h**2 - a_t**2) / (2 * a_h * t_h), 5))
    angle_t_h = math.degrees(radian_t_h)


# 4. 내 공과 접점 까지의 거리 구하기
    a_d = math.sqrt(a_h**2 + (t_h + 2 * r)**2 - (2 * a_h * (t_h + 2 * r) * math.cos(angle_t_h)))


# 5. 내 공에서 접점 까지의 각도 구하기
    radian_a_d = math.acos(round((a_h**2 + a_d**2 - (t_h + 2 * r)**2) / (2 * a_h * a_d), 5))
    angle_a_d = math.degrees(radian_a_d)

# 6. 목적구와 홀의 위치에 따라 변하는 각도 지정


    # 목적구가 흰 공을 중심으로 3사분면에 위치했을 때 각도를 재계산
    if whiteBall_x > targetBall_x and whiteBall_y > targetBall_y:
        if abs(targetBall_x - whiteBall_x) > abs(targetBall_y - whiteBall_y):
            angle = 180 + (angle_a_h + angle_a_d)
        elif abs(targetBall_x - whiteBall_x) == abs(targetBall_y - whiteBall_y):
            angle = 180 + angle_a_h
        else:
            angle = 180 + (angle_a_h - angle_a_d)

    # 목적구가 흰 공을 중심으로 4사분면에 위치했을 때 각도를 재계산
    elif whiteBall_x < targetBall_x and whiteBall_y > targetBall_y:
        if abs(targetBall_x - whiteBall_x) > abs(targetBall_y - whiteBall_y):
            angle = 180 - (angle_a_h + angle_a_d)
        elif abs(targetBall_x - whiteBall_x) == abs(targetBall_y - whiteBall_y):
            angle = 180 - angle_a_h + 2
        else:
            angle = 180 - (angle_a_h - angle_a_d)

    # 목적구가 흰 공을 중심으로 1사분면(?)에 위치했을 때 각도를 재계산
    elif whiteBall_x > targetBall_x and whiteBall_y < targetBall_y:
        if abs(targetBall_x - whiteBall_x) > abs(targetBall_y - whiteBall_y):
            angle = 360 - (angle_a_h + angle_a_d)
        elif abs(targetBall_x - whiteBall_x) == abs(targetBall_y - whiteBall_y):
            angle = 360 - angle_a_h
        else:
            angle = 360 - (angle_a_h - angle_a_d)

    # 목적구가 흰 공을 중심으로 2사분면(?)에 위치했을 때 target의 위치에 따른 각도 변화
    else:
        if abs(targetBall_x - whiteBall_x) > abs(targetBall_y - whiteBall_y):
            angle = angle_a_d + angle_a_h - 1
        elif abs(targetBall_x - whiteBall_x) == abs(targetBall_y - whiteBall_y):
            angle = angle_a_h
        else:
            angle = angle_a_h - angle_a_d


    # power: 거리 distance에 따른 힘의 세기를 계산
    power = a_d * 0.5

    '''
    어떤 전략으로 알고리즘을 구현했는가?
    
    - 처음 주어진 코드를 실행해봤을때, 그 코드는 
    첫번째로, 1번 공만 찾아서 다녔고, 
    두번째로, 내 공과 목적구를 직선으로 달려가서 맞추었습니다.
    
    1~3번 스테이지 까지는 내 공과 목적구, 홀이 일직선상으로 이루어져있었기 때문에, 클리어 할 수 있었으나,
    4번 스테이지 같은 경우에는 목적구가 2개 였고, 1번 공을 넣고 난 후에는 일직선 상으로 달려가서 골인 시키기가 어려워 보였습니다.
    그래서 삼각함수를 이용한 알고리즘을 통해 골인 시키고자 하였습니다.
    
    1. 내 공, 목적구, 홀 각각의 거리를 계산하였습니다.
    - 해당 거리를 구하는데에는 피타고라스의 정리를 이용하여 구하였습니다.
      x축 과의 거리, y축과의 거리는 직각을 이루므로 피타고라스 정리를 통해 사이의 거리를 구할 수 있으며
      피타고라스의 정리 연산은 math.sqrt를 이용하였습니다.
      
    - 어떤 홀로 갈 것인가? 는 목적구에서 가장 가까운 홀을 찾아내어 그 홀로 이동하게 하였습니다.
      
    - 내 공과 홀까지의 각도는 직각 삼각형을 이룸으로 math.atan를 통해 구하였습니다.
      
    2. 내 공, 목적구, 홀 각각의 거리를 계산하였습니다.
    - 해당 각도를 알기 위해서는 첫째로 구하고자하는 각도가 들어간 삼각형의 모든 변의 길이를 알 필요가 있었습니다.
      우선적으로, 목적구와 홀 사이의 각도부터 구하면, 그 각도를 통해 내 공과, 목적구의 접점까지의 거리를 구할 수 있었습니다.
      그 거리를 구한 후 그 거리를 토대로 내 공과 접점과의 각도를 구할 수 있었습니다.
      각도와 길이는 직각삼각형이 아니므로, 피타고라스의 정리를 이용하여 구할 순 없었고, 제 2 코사인 법칙을 통해 구할 수 있었습니다.
      거리는 내가 구하고자 하는 변을 제외한 두 변의 길이를 제곱하여 더하고, 그 값에 두 변의 길이를 곱한 값에 2를 곱하고 그 두변의 각도
      (끼인각?)의 cos 값을 곱하여 빼주면 구하고자하는 거리의 제곱 값이었고, math.sqrt를 이용하여 제곱근값으로 거리를 구해주었습니다. 
      
    - 각도는 제 2 코사인 법칙을 응용하여, 3변의 길이를 토대로 구하고자 하는 각도의 cos 값을 구한후에, 그 값을 토대로
      math.acos을 사용해주면, 각도를 얻을 수 있었습니다. 각도는 radian 값으로 반환되었기 때문에, math.degrees를 이용하여
      각도 값으로 바꿔 주었습니다.
      
      
    3. 내 공과 목적구의 위치에 따라 각도 계산을 다르게 하였습니다.
     - 모든 목적구가 현재 내 공의 위치에서 제 2사분면에 들어가 있을리가 없었습니다.
       해당 공식은 절대값으로 계산했기 때문에 있는 좌표에 맞게 각도를 주지 않았습니다.
       그래서 목적구가 내 공에서 어느 쪽에 위치하였는가, 그리고 목적구가 x축의 값이 더 큰가, y축의 값이 더 큰가를 따져보아
       각각 다르게 angle 값을 결정하여 상황에 맞게 맞추도록 노력하였습니다.
       
       
    4. 4번 문제 해결법
     - 코드를 짜다보니 이상하게 1번공만 찾아가려고 하는 습성이 있었습니다.
       처음에는 for문을 통해 목적구를 할당하려고 하였으나, 아에 1번공도 안맞추는 경우가 발생했습니다.
       예상컨데, 모든 공의 값이 1번에 들어오고, 1턴당 코드를 1번씩 실행해서 for문으로 할 수 없지 않았나? 생각했습니다.
       따라서 주어지는 order의 값에 따라, 시작구를 두고, 홀로 골인하면 좌표값이 -1, -1로 바뀌는 특징을 찾아내어
       현재 추적하는공의 좌표가 -1, -1이라면, 현재 추적하는 공의 번호에 따라 다음 목적구를 할당하는 방식으로 설계하였습니다.
       
       
    단점? : 해당 알고리즘을 통해 실시한 결과 아쉽게도 5~6단계에서는 제대로 작동하지 않았습니다
    예상하는 문제점을 몇개 생각해보았습니다.
    1. 처음 1번 공이 주어질 때, 홀에서 가장 가까운 값이 애매해지자, 이상한 곳으로 날라가버리기 시작했습니다.
    2. 목적구만 주어질 때, 그리고 목적구 이외의 공이 주어질 때를 판단하지 못했습니다. 즉 비목적구와의 충돌이 발생할 우려가 있었습니다.
    3. 목적구의 x,y 값이 비슷할 때? 정확한 위치를 찾아내지 못하였습니다.
    
    후기 : 생각보다 초반에 많이 헤매서 못할 줄 알았는데 그나마 pass 할 수 있어서 다행입니다.
    남은 시간동안 5~6번 문제를 풀어보도록 하겠습니다.
    
    '''

    # 주어진 데이터(공의 좌표)를 활용하여 두 개의 값을 최종 결정하고 나면,
    # 나머지 코드에서 일타싸피로 값을 보내 자동으로 플레이를 진행하게 합니다.
    #   - angle: 흰 공을 때려서 보낼 방향(각도)
    #   - power: 흰 공을 때릴 힘의 세기
    # 
    # 이 때 주의할 점은 power는 100을 초과할 수 없으며,
    # power = 0인 경우 힘이 제로(0)이므로 아무런 반응이 나타나지 않습니다.
    #
    # 아래는 일타싸피와 통신하는 나머지 부분이므로 수정하면 안됩니다.
    ##############################

    merged_data = '%f/%f/' % (angle, power)
    sock.send(merged_data.encode('utf-8'))
    print('Data Sent: %s' % merged_data)

sock.close()
print('Connection Closed.\n--------------------')