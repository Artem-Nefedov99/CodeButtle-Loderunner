import logging
import random

from loderunnerclient.internals.actions import LoderunnerAction
from loderunnerclient.internals.board import Board
from loderunnerclient.game_client import GameClient

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)

def turn(gcb: Board):
    # send random one of possible commands
    action_id = random.randint(0, len(LoderunnerAction) - 1)
    my_position = gcb.get_my_position()
    all_gold_position = gcb.get_gold_positions()
    all_ladder_position = gcb.get_ladder_positions()
    print(my_position)
    #проверка на возможность добраться до золота
    possible_flag = []
    for i in range(len(all_gold_position)):
        if gcb.has_wall_at(all_gold_position[i].get_x()-1,all_gold_position[i].get_y()+1) == True or gcb.has_wall_at(all_gold_position[i].get_x(),all_gold_position[i].get_y()+1) == True or gcb.has_wall_at(all_gold_position[i].get_x()+1,all_gold_position[i].get_y()+1)==True:
            possible_flag.append(True)
        else:
            possible_flag.append(False)
    near_gold = find_near_gold(all_gold_position, my_position, possible_flag)
    # определение лестниц ведущих наверх
    flag_for_up = []
    for i in range(len(all_ladder_position)):
        if (gcb.has_ladder_at(all_ladder_position[i].get_x(), all_ladder_position[i].get_y()-1)==True and gcb.has_wall_at(all_ladder_position[i].get_x(), all_ladder_position[i].get_y()-1)==False) or gcb.has_wall_at(all_ladder_position[i].get_x(), all_ladder_position[i].get_y()-1)==False:
            flag_for_up.append(True)
        else:
            flag_for_up.append(False)
    # определение лестниц ведущих вниз
    flag_for_down = []
    for i in range(len(all_ladder_position)):
        if gcb.has_ladder_at(all_ladder_position[i].get_x(),all_ladder_position[i].get_y() + 1) == True or gcb.has_wall_at(all_ladder_position[i].get_x(), all_ladder_position[i].get_y() + 1) == False:
            flag_for_down.append(True)
        else:
            flag_for_down.append(False)
    #если одна горизонталь
    if near_gold[0][0] < 0 and near_gold[0][1]==0:
        return LoderunnerAction.GO_RIGHT
    if near_gold[0][0] > 0 and near_gold[0][1]==0:
        return LoderunnerAction.GO_LEFT
    #если разная горизонталь
    near_ladder_up_position = find_near_ladder_up(all_ladder_position, my_position, flag_for_up)
    near_ladder_down_position = find_near_ladder_down(all_ladder_position, my_position, flag_for_down)
    if near_gold[0][1] != 0:
        if near_gold[0][1] < 0:
            if near_ladder_down_position[0][0] < 0:
                return LoderunnerAction.GO_RIGHT
            if near_ladder_down_position[0][0] > 0:
                return  LoderunnerAction.GO_LEFT
            if near_ladder_down_position[0][0] == 0:
                return LoderunnerAction.GO_DOWN
    if near_gold[0][1] != 0:
        if near_gold[0][1] > 0:
            if near_ladder_up_position[0][0] < 0:
                return LoderunnerAction.GO_RIGHT
            if near_ladder_up_position[0][0] > 0:
                return  LoderunnerAction.GO_LEFT
            if near_ladder_up_position[0][0] == 0 and gcb.has_wall_at(my_position.get_x(), my_position.get_y()-1)==False:
                return LoderunnerAction.GO_UP

    if gcb.has_wall_at(my_position.get_x()+1, my_position.get_y())==True:
        if gcb.has_wall_at(my_position.get_x(), my_position.get_y()+1)==False:
            return LoderunnerAction.GO_DOWN
        else:
            return LoderunnerAction.GO_UP
    if gcb.has_wall_at(my_position.get_x()-1, my_position.get_y())==True:
        if gcb.has_wall_at(my_position.get_x(), my_position.get_y()+1)==False:
            return LoderunnerAction.GO_DOWN
        else:
            return LoderunnerAction.GO_UP

    return LoderunnerAction.GO_LEFT

def my_x_y(my_position):
    my_x = my_position.get_x()
    my_y = my_position.get_y()
    return my_x,my_y

def find_near_gold(all_gold_position, my_position, possible_flag):
    near_gold_position = []
    flag_sqrt = 1000
    for i in range(len(all_gold_position)):
        my_x, my_y = my_x_y(my_position)
        x_gold_of_me = my_x - all_gold_position[i].get_x()
        y_gold_of_me = my_y - all_gold_position[i].get_y()
        #print(x_gold_of_me, y_gold_of_me)
        if pow(pow(x_gold_of_me,2)+pow(y_gold_of_me,2),0.5) <= flag_sqrt and possible_flag[i]==True:
            near_gold_position.clear()
            near_gold_position.append([x_gold_of_me,y_gold_of_me])
            #print(near_gold_position)
            flag_sqrt = pow(pow(x_gold_of_me,2)+pow(y_gold_of_me,2),0.5)
    print("Ближайшее золото", near_gold_position)
    #print(possible_flag)
    return near_gold_position

def find_near_ladder_up(all_ladder_position, my_position, flag_for_up):
    near_ladder_up_position = []
    flag_sqrt = 1000
    for i in range(len(all_ladder_position)):
        my_x, my_y = my_x_y(my_position)
        x_ladder_of_me = my_x - all_ladder_position[i].get_x()
        y_ladder_of_me = my_y - all_ladder_position[i].get_y()
        # print(x_gold_of_me, y_gold_of_me)
        if pow(pow(x_ladder_of_me, 2) + pow(y_ladder_of_me, 2), 0.5) <= flag_sqrt and all_ladder_position[i].get_y()-my_position.get_y() == 0 and flag_for_up[i]==True:
            near_ladder_up_position.clear()
            near_ladder_up_position.append([x_ladder_of_me, y_ladder_of_me])
            # print(near_gold_position)
            flag_sqrt = pow(pow(x_ladder_of_me, 2) + pow(y_ladder_of_me, 2), 0.5)
    print("Ближайшая труба вверх", near_ladder_up_position)
    return near_ladder_up_position

def find_near_ladder_down(all_ladder_position, my_position, flag_for_down):
    near_ladder_down_position = []
    flag_sqrt = 1000
    for i in range(len(all_ladder_position)):
        my_x, my_y = my_x_y(my_position)
        x_ladder_of_me = my_x - all_ladder_position[i].get_x()
        y_ladder_of_me = my_y - all_ladder_position[i].get_y()
        # print(x_gold_of_me, y_gold_of_me)
        if pow(pow(x_ladder_of_me, 2) + pow(y_ladder_of_me, 2), 0.5) <= flag_sqrt and all_ladder_position[i].get_y()-my_position.get_y() == 1 and flag_for_down[i]==True:
            near_ladder_down_position.clear()
            near_ladder_down_position.append([x_ladder_of_me, y_ladder_of_me])
            # print(near_gold_position)
            flag_sqrt = pow(pow(x_ladder_of_me, 2) + pow(y_ladder_of_me, 2), 0.5)
    print("Ближайшая труба вниз", near_ladder_down_position)
    return near_ladder_down_position

def main():
    gcb = GameClient(
        # change this url to your
        "https://dojorena.io/codenjoy-contest/board/player/dojorena447?code=6147118823891513738"
    )
    gcb.run(turn)


if __name__ == "__main__":
    main()
