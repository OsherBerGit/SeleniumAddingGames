import selGetGames
import selSendGames
import time

if __name__ == "__main__":
    selGetGames.interact_with_form()
    time.sleep(3)
    selSendGames.interact_with_form()