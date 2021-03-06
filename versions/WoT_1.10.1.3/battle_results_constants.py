# uncompyle6 version 3.7.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (v2.7.18:8d21aa21f2, Apr 20 2020, 13:19:08) [MSC v.1500 32 bit (Intel)]
# Embedded file name: scripts/common/battle_results/battle_results_constants.py
from constants import ARENA_BONUS_TYPE
PATH_TO_CONFIG = {ARENA_BONUS_TYPE.REGULAR: 'random', 
   ARENA_BONUS_TYPE.EPIC_RANDOM: 'random', 
   ARENA_BONUS_TYPE.EPIC_RANDOM_TRAINING: 'random', 
   ARENA_BONUS_TYPE.RANKED: 'ranked', 
   ARENA_BONUS_TYPE.EPIC_BATTLE: 'frontline', 
   ARENA_BONUS_TYPE.EPIC_BATTLE_TRAINING: 'frontline', 
   ARENA_BONUS_TYPE.EVENT_BATTLES: 'event'}
POSSIBLE_TYPES = (
 int, float, str, bool, list, tuple, dict, set, None)

class BATTLE_RESULT_ENTRY_TYPE:
    COMMON = 1
    ACCOUNT_SELF = 2
    ACCOUNT_ALL = 3
    VEHICLE_SELF = 4
    VEHICLE_ALL = 5
    PLAYER_INFO = 6
    SERVER = 7
    ALL = (
     COMMON, ACCOUNT_SELF, ACCOUNT_ALL, VEHICLE_SELF, VEHICLE_ALL, PLAYER_INFO, SERVER)