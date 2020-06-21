from connectfour.connectfourRL import connectfourgym
from connectfour.connectfourRL.aiplayers import qlearnedPlayer, humanPlayer

player1 = qlearnedPlayer.QLearnedPlayer()
player2 = qlearnedPlayer.QLearnedPlayer()
playerHuman = humanPlayer.HumanPlayer()
gym = connectfourgym.ConnectFourGym(10, player1, player2)