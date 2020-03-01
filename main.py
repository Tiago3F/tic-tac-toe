import random
import gym
import gym_tictactoe
from math import inf as infinity

# Configurações
O = -1  # Usuário
X = 1  # IA
env = gym.make("TicTacToe-v1", symbols=[X, O])
env.reset()

def vitoria(last_state, jogador):
    win_state = [
        [last_state[0], last_state[1], last_state[2]],
        [last_state[3], last_state[4], last_state[5]],
        [last_state[6], last_state[7], last_state[8]],
        [last_state[0], last_state[3], last_state[6]],
        [last_state[1], last_state[4], last_state[7]],
        [last_state[2], last_state[5], last_state[8]],
        [last_state[0], last_state[4], last_state[8]],
        [last_state[2], last_state[4], last_state[6]],
    ]
    
    if [jogador, jogador, jogador] in win_state:
        return True
    else:
        return False

def fim(last_state):
    return vitoria(last_state, O) or vitoria(last_state, X)

def pontos(last_state):
    
    if vitoria(last_state, X):
        ponto = +1
    elif vitoria(last_state, O):
        ponto = -1
    else:
        ponto = 0

    return ponto


def espacoVazio(last_state):
    espacos = []
    for i in range(len(last_state)):
        if last_state[i] == 0:
            espacos.append(i)
    return espacos
            

def minmax(jogador, last_state, depth):
    
    if jogador == X:
        melhor = [-1, -infinity]
    else:
        melhor = [-1, +infinity]

    if depth == 0 or fim(last_state):
        ponto = pontos(last_state)
        return [-1, ponto]

    for espaco in espacoVazio(last_state):
        last_state[espaco] = jogador
        ponto = minmax(-jogador, last_state, depth - 1)
        last_state[espaco] = 0
        ponto[0] = espaco

        if jogador == X:
            if ponto[1] > melhor[1]:
                melhor = ponto
        else:
            if ponto[1] < melhor[1]:
                melhor = ponto
    
    return melhor


def action_O(last_state):
    '''
        Gera a ação do usuário.
        last_state = lista de ações realizadas
    '''
    options = [i for i in range(len(last_state)) if last_state[i] == 0]
    print('Options: %s' % options)
    action = int(input('Select a option: '))
    while not action in options:
        action = int(input('Select a option: '))
    return action


def action_X(last_state):

    depth = len(espacoVazio(last_state))

    if depth == 0 or fim(last_state):
        return

    if depth == 9:
        options = [i for i in range(len(last_state)) if last_state[i] == 0]
        return random.choice(options)
    else:
        setMove = minmax(X, last_state, depth)
        action = setMove[0]
    return action      
    
# Define o usuário da vez
user = O
# Ultimo estado
last_state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
# Inicia o jogo
env.render(mode=None)
while True:
    # Cada usuário tem estratégias diferentes
    if user == O:
        action = action_O(last_state)
    else:
        action = action_X(last_state)

    print('Play: %s Action: %s' % ('O' if user == O else 'X', action))
    state, reward, done, infos = env.step(action, user)
    print(state, reward, done, infos)
    env.render(mode=None)

    # Se terminou mostra o placar
    if done:
        if reward == 10:
            print("Draw !")
        else:
            print("User %s wins! Reward : %s" % ('O' if user == O else 'X', reward, ))
        env.reset()
        break
    # Muda o usuário
    user = O if user == X else X
    last_state = state
env.close()
