# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.8 (default, Jun 30 2014, 16:08:48) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: scripts/common/battle_results_shared.py
import struct
from itertools import izip
from battle_results_constants import BATTLE_RESULT_ENTRY_TYPE as ENTRY_TYPE
from battle_results_constants import VEHICLE_DEVICE_TYPE_NAMES, VEHICLE_TANKMAN_TYPE_NAMES, FLAG_ACTION
from dictpackers import *
from badges_common import BadgesCommon

def _buildMapsForExt(fields):
    return (
     Meta(fields),
     tuple((v[0], v[2]) for v in fields), {v[0]:i for i, v in enumerate(fields)})

class PREMIUM_TYPE:
    NONE = 0
    BASIC = 1
    PLUS = 2
    VIP = 4
    TYPES_SORTED = (
     BASIC, PLUS, VIP)
    ANY = BASIC | PLUS | VIP
    AFFECTING_TYPES = PLUS | VIP

    @classmethod
    def activePremium(cls, premMask):
        for premType in reversed(cls.TYPES_SORTED):
            if premMask & premType:
                return premType

        return cls.NONE

    @classmethod
    def initialData(cls):
        return {cls.BASIC: 0, 
           cls.PLUS: 0, 
           cls.VIP: 0, 
           'premMask': 0}

class PREM_BONUS_TYPES:
    CREDITS = 0
    XP = 1
    TMEN_XP = 2

VEH_INTERACTION_DETAILS = (
 ('spotted', 'B', 1, 0),
 ('deathReason', 'b', 10, -1),
 ('directHits', 'H', 65535, 0),
 ('directEnemyHits', 'H', 65535, 0),
 ('explosionHits', 'H', 65535, 0),
 ('piercings', 'H', 65535, 0),
 ('piercingEnemyHits', 'H', 65535, 0),
 ('damageDealt', 'I', 4294967295L, 0),
 ('damageAssistedTrack', 'H', 65535, 0),
 ('damageAssistedRadio', 'H', 65535, 0),
 ('damageAssistedStun', 'H', 65535, 0),
 ('damageAssistedSmoke', 'H', 65535, 0),
 ('damageAssistedInspire', 'H', 65535, 0),
 ('crits', 'I', 4294967295L, 0),
 ('fire', 'H', 65535, 0),
 ('stunNum', 'H', 65535, 0),
 ('stunDuration', 'f', 65535.0, 0.0),
 ('damageBlockedByArmor', 'I', 4294967295L, 0),
 ('damageReceived', 'H', 65535, 0),
 ('rickochetsReceived', 'H', 65535, 0),
 ('noDamageDirectHitsReceived', 'H', 65535, 0),
 ('targetKills', 'B', 255, 0))
VEH_INTERACTION_DETAILS_NAMES = [ x[0] for x in VEH_INTERACTION_DETAILS ]
VEH_INTERACTION_DETAILS_MAX_VALUES = dict((x[0], x[2]) for x in VEH_INTERACTION_DETAILS)
VEH_INTERACTION_DETAILS_INIT_VALUES = [ x[3] for x in VEH_INTERACTION_DETAILS ]
VEH_INTERACTION_DETAILS_LAYOUT = ('').join([ x[1] for x in VEH_INTERACTION_DETAILS ])
VEH_INTERACTION_DETAILS_INDICES = dict((x[1][0], x[0]) for x in enumerate(VEH_INTERACTION_DETAILS))
VEH_INTERACTION_DETAILS_TYPES = dict((x[0], x[1]) for x in VEH_INTERACTION_DETAILS)
VEH_INTERACTIVE_STATS = ('xp', 'damageDealt', 'capturePts', 'flagActions', 'winPoints',
                         'deathCount', 'resourceAbsorbed', 'stopRespawn', 'equipmentDamage',
                         'equipmentKills')
VEH_INTERACTIVE_STATS_INDICES = dict((x[1], x[0]) for x in enumerate(VEH_INTERACTIVE_STATS))
AVATAR_PRIVATE_STATS = ('ragePoints', )
AVATAR_PRIVATE_STATS_INDICES = dict((x[1], x[0]) for x in enumerate(AVATAR_PRIVATE_STATS))
_PREM_TYPE_TO_FACTOR100_NAMES = {PREM_BONUS_TYPES.CREDITS: {PREMIUM_TYPE.BASIC: 'premiumCreditsFactor100', 
                              PREMIUM_TYPE.PLUS: 'premiumPlusCreditsFactor100', 
                              PREMIUM_TYPE.VIP: 'premiumVipCreditsFactor100'}, 
   PREM_BONUS_TYPES.XP: {PREMIUM_TYPE.BASIC: 'premiumXPFactor100', 
                         PREMIUM_TYPE.PLUS: 'premiumPlusXPFactor100', 
                         PREMIUM_TYPE.VIP: 'premiumVipXPFactor100'}, 
   PREM_BONUS_TYPES.TMEN_XP: {PREMIUM_TYPE.BASIC: 'premiumTmenXPFactor100', 
                              PREMIUM_TYPE.PLUS: 'premiumPlusTmenXPFactor100', 
                              PREMIUM_TYPE.VIP: 'premiumVipXPTmenFactor100'}}

_PRIVATE_EVENT_RESULTS = Meta([
 ('eventCredits', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('eventXP', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('eventFreeXP', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('eventTMenXP', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('eventGold', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('eventCrystal', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('eventEventCoin', int, 0, None, 'sum', ENTRY_TYPE.COMMON)])

_AVATAR_CELL_RESULTS_PRIVATE = Meta([
 ('avatarAmmo', list, [], None, 'skip', ENTRY_TYPE.COMMON), 
 ('avatarDamageEventList', set, set(), None, 'skip', ENTRY_TYPE.COMMON)])

_AVATAR_CELL_RESULTS_SERVER = Meta([
 ('avatarAmmoEquipped', set, set(), None, 'skip', ENTRY_TYPE.COMMON)])

_AVATAR_CELL_RESULTS_PUBLIC = Meta([
 ('avatarDamageDealt', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('avatarKills', int, 0, None, 'skip', ENTRY_TYPE.COMMON)])

_AVATAR_BASE_SERVER_RESULTS = Meta([
 ('cybersportRatingDeltas', tuple, (0.0, 0.0), None, 'skip', ENTRY_TYPE.COMMON), 
 ('vehRankRaised', int, 0, None, 'skip', ENTRY_TYPE.COMMON)])

_AVATAR_BASE_PRIVATE_RESULTS = Meta([
 ('accountDBID', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('team', int, 1, None, 'skip', ENTRY_TYPE.COMMON), 
 ('clanDBID', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('fortClanDBIDs', list, [], None, 'skip', ENTRY_TYPE.COMMON), 
 ('winnerIfDraw', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('isPrematureLeave', bool, False, None, 'skip', ENTRY_TYPE.COMMON), 
 ('watchedBattleToTheEnd', bool, False, None, 'skip', ENTRY_TYPE.COMMON), 
 ('squadBonusInfo', None, None,None, 'skip', ENTRY_TYPE.COMMON), 
 ('progressiveReward',None, None,None, 'skip', ENTRY_TYPE.COMMON), 
 ('rankChange', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('updatedRankChange', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('accRank', tuple, (0, 0), None, 'skip', ENTRY_TYPE.COMMON), 
 ('vehRank', tuple, (0, 0), None, 'skip', ENTRY_TYPE.COMMON), 
 ('prevAccRank', tuple, (0, 0), None, 'skip', ENTRY_TYPE.COMMON), 
 ('prevMaxRank', tuple, (0, 0), None, 'skip', ENTRY_TYPE.COMMON), 
 ('prevVehRank', tuple, (0, 0), None, 'skip', ENTRY_TYPE.COMMON), 
 ('shields', dict, {}, None, 'skip', ENTRY_TYPE.COMMON), 
 ('prevShields', dict, {}, None, 'skip', ENTRY_TYPE.COMMON), 
 ('rankedSeason', tuple, (0, 0), None, 'skip', ENTRY_TYPE.COMMON), 
 ('rankedSeasonNum', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('bonusBattleUsed', bool, False, None, 'skip', ENTRY_TYPE.COMMON), 
 ('efficiencyBonusBattles', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('stepsBonusBattles', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('eligibleForCrystalRewards', bool, False, None, 'skip', ENTRY_TYPE.COMMON), 
 ('activeRents', dict, {}, None, 'skip', ENTRY_TYPE.COMMON), 
 ('recruitsIDs', list, [], None, 'skip', ENTRY_TYPE.COMMON), 
 ('recruiterID', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('fareTeamXPPosition', int, 0, None, 'skip', ENTRY_TYPE.COMMON)])

_AVATAR_BASE_PUBLIC_RESULTS_EXTS = {
   'playerRank': _buildMapsForExt([
       ('rank', int, 0, None, 'skip', ENTRY_TYPE.COMMON)]), 
   'epicMetaGame': _buildMapsForExt([
       ('creditsAfterShellCosts', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
       ('unchargedShellCosts', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
       ('prevMetaLevel', tuple, (0, 1, 0), None, 'skip', ENTRY_TYPE.COMMON),
       ('metaLevel', tuple, (0, 1, 0), None, 'skip', ENTRY_TYPE.COMMON), 
       ('flXP', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
       ('originalFlXP', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
       ('subtotalFlXP', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
       ('boosterFlXP', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
       ('boosterFlXPFactor100', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
       ('flXPReplay', str, '', ValueReplayPacker(), 'skip', ENTRY_TYPE.COMMON)]), 
   'battlePass': _buildMapsForExt([
       ('basePointsDiff', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
       ('sumPoints', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
       ('hasBattlePass', bool, False, None, 'skip', ENTRY_TYPE.COMMON)])}

_AVATAR_BASE_PUBLIC_RESULTS = Meta([
 ('avatarDamaged', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('totalDamaged', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('fairplayViolations', tuple, (0, 0, 0), None, 'skip', ENTRY_TYPE.COMMON), 
 ('prevAccRank', tuple, (0, 0), None, 'skip', ENTRY_TYPE.COMMON), 
 ('badges', tuple, BadgesCommon.selectedBadgesEmpty(), None, 'skip', ENTRY_TYPE.COMMON), 
 ('ext', dict, {}, BunchProxyPacker(_AVATAR_BASE_PUBLIC_RESULTS_EXTS), 'joinExts', ENTRY_TYPE.COMMON)])

_AVATAR_FULL_RESULTS_PRIVATE = Meta([
 ('questsProgress', dict, {}, None, 'skip', ENTRY_TYPE.COMMON), 
 ('PM2Progress', dict, {}, None, 'skip', ENTRY_TYPE.COMMON)])

_AVATAR_DELETE_ME = Meta([
 ('credits', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('xp', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('freeXP', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('crystal', int, 0, None, 'skip', ENTRY_TYPE.COMMON)])

AVATAR_CELL_RESULTS = _AVATAR_CELL_RESULTS_PUBLIC + _AVATAR_CELL_RESULTS_PRIVATE + _AVATAR_CELL_RESULTS_SERVER
AVATAR_BASE_RESULTS = AVATAR_CELL_RESULTS + _AVATAR_BASE_PUBLIC_RESULTS + _AVATAR_BASE_SERVER_RESULTS + _AVATAR_BASE_PRIVATE_RESULTS
AVATAR_PUBLIC_RESULTS = _AVATAR_CELL_RESULTS_PUBLIC + _AVATAR_BASE_PUBLIC_RESULTS
AVATAR_FULL_RESULTS = _AVATAR_CELL_RESULTS_PUBLIC + _AVATAR_CELL_RESULTS_PRIVATE + _AVATAR_BASE_PUBLIC_RESULTS + _AVATAR_BASE_PRIVATE_RESULTS + _AVATAR_FULL_RESULTS_PRIVATE + _PRIVATE_EVENT_RESULTS + _AVATAR_DELETE_ME

PLAYER_INFO = [
 ('accountDBID', int, 0, None, 'any', ENTRY_TYPE.ACCOUNT_SELF),
 ('team', int, 1, None, 'skip', ENTRY_TYPE.ACCOUNT_SELF),
 ('clanDBID', int, 0, None, 'skip', ENTRY_TYPE.ACCOUNT_SELF),
 ('fortClanDBIDs', list, [], None, 'skip', ENTRY_TYPE.ACCOUNT_SELF),
 ('prebattleID', int, 0, None, 'skip', ENTRY_TYPE.PLAYER_INFO),
 ('team', int, 1, None, 'skip', ENTRY_TYPE.PLAYER_INFO),
 ('igrType', int, 0, None, 'skip', ENTRY_TYPE.PLAYER_INFO)]
PLAYER_INFO_META = Meta(PLAYER_INFO)

VEH_CELL_RESULTS_EXTS = {'extPublic': {
                 'recoveryMechanic': _buildMapsForExt([
                    ('numRecovered', int, 0, None, 'sum', ENTRY_TYPE.COMMON)]),
                 'sector': _buildMapsForExt([
                    ('numCaptured', int, 0, None, 'sum', ENTRY_TYPE.COMMON)]), 
                 'destructibleEntity': _buildMapsForExt([
                    ('numDestroyed', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
                    ('damageDealt', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
                    ('hits', int, 0, None, 'sum', ENTRY_TYPE.COMMON)]), 
                 'defenderBonus': _buildMapsForExt([
                    ('numDefended', int, 0, None, 'sum', ENTRY_TYPE.COMMON)])},
   'extPrivate': {}, 'extServer': {
                'achievementsData': _buildMapsForExt([
                    ('ironShieldDamage', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
                    ('occupyingForceDestruction', bool, False, None, 'max', ENTRY_TYPE.COMMON), 
                    ('occupyingForceBasePoints', int, 0, None, 'sum', ENTRY_TYPE.COMMON)])}}

_VEH_CELL_RESULTS_PUBLIC = Meta([
 ('health', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('maxHealth', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('credits', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('xp', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('xp/attack', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('xp/assist', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('xp/other', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('xpPenalty', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('achievementCredits', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('achievementXP', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('achievementFreeXP', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('shots', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('directHits', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('directTeamHits', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('explosionHits', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('piercings', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('damageDealt', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('sniperDamageDealt', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('equipmentDamageDealt', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('damageAssistedRadio', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('damageAssistedTrack', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('damageAssistedStun', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('damageAssistedSmoke', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('damageAssistedInspire', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('stunNum', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('stunDuration', float, 0.0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('damageReceived', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('damageReceivedFromInvisibles', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('damageBlockedByArmor', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('directHitsReceived', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('noDamageDirectHitsReceived', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('explosionHitsReceived', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('piercingsReceived', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('tdamageDealt', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('tdestroyedModules', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('tkills', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('isTeamKiller', bool, False, None, 'max', ENTRY_TYPE.COMMON), 
 ('capturePoints', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('capturingBase', None, None, None, 'any', ENTRY_TYPE.COMMON), 
 ('droppedCapturePoints', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('mileage', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('lifeTime', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('killerID', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('achievements', list, [], None, 'extend', ENTRY_TYPE.COMMON), 
 ('potentialDamageReceived', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('rolloutsCount', int, 0, None, 'sum', ENTRY_TYPE.COMMON),
 ('deathCount', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('flagActions', list, [0] * len(FLAG_ACTION.RANGE), None, 'sumInEachPos', ENTRY_TYPE.COMMON), 
 ('soloFlagCapture', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('flagCapture', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('winPoints', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('resourceAbsorbed', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('stopRespawn', bool, False, None, 'max', ENTRY_TYPE.COMMON), 
 ('extPublic', dict, {}, BunchProxyPacker(VEH_CELL_RESULTS_EXTS['extPublic']), 'joinExts', ENTRY_TYPE.COMMON)])

_VEH_CELL_RESULTS_PRIVATE = Meta([
 ('repair', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('freeXP', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('details', None, '', None, 'skip', ENTRY_TYPE.COMMON), 
 ('extPrivate', dict, {}, BunchProxyPacker(VEH_CELL_RESULTS_EXTS['extPrivate']), 'joinExts', ENTRY_TYPE.COMMON)])

_VEH_CELL_RESULTS_SERVER = Meta([
 ('canStun', bool, False, None, 'any', ENTRY_TYPE.COMMON), 
 ('potentialDamageDealt', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('soloHitsAssisted', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('isEnemyBaseCaptured', bool, False, None, 'max', ENTRY_TYPE.COMMON), 
 ('stucks', list, [], DeltaPacker(roundToInt), 'extend', ENTRY_TYPE.COMMON), 
 ('autoAimedShots', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('presenceTime', int, 0, None, 'max', ENTRY_TYPE.COMMON), 
 ('spotList', list, [], None, 'extend', ENTRY_TYPE.COMMON), 
 ('ammo', list, [], None, 'skip', ENTRY_TYPE.COMMON), 
 ('crewActivityFlags', list, [], None, 'skip', ENTRY_TYPE.COMMON), 
 ('series', dict, {}, None, 'skip', ENTRY_TYPE.COMMON), 
 ('tkillRating', float, 0.0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('thitPenalties', dict, {}, None, 'joinTHitPenalties', ENTRY_TYPE.COMMON), 
 ('destroyedObjects', dict, {}, None, 'sumByEackKey', ENTRY_TYPE.COMMON), 
 ('discloseShots', list, [], DeltaPacker(), 'extend', ENTRY_TYPE.COMMON), 
 ('critsCount', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('aimerSeries', int, 0, None, 'max', ENTRY_TYPE.COMMON), 
 ('observedByEnemyTime', int, -1, None, 'any', ENTRY_TYPE.COMMON), 
 ('critsByType', dict, {},
    DictPacker([
        ('destroyed', dict, {}, SimpleDictPacker(int, VEHICLE_DEVICE_TYPE_NAMES), 'skip', ENTRY_TYPE.COMMON), 
        ('critical', dict, {}, SimpleDictPacker(int, VEHICLE_DEVICE_TYPE_NAMES), 'skip', ENTRY_TYPE.COMMON), 
        ('tankman', dict, {}, SimpleDictPacker(int, VEHICLE_TANKMAN_TYPE_NAMES), 'skip', ENTRY_TYPE.COMMON)]),
 'joinCritsByType', ENTRY_TYPE.COMMON), 
 ('innerModuleCritCount', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('innerModuleDestrCount', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('isAnyOurCrittedInnerModules', int, 0, None, 'max', ENTRY_TYPE.COMMON), 
 ('killsAssistedTrack', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('killsAssistedRadio', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('killsAssistedStun', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('damagedVehicleCntAssistedTrack', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('damagedVehicleCntAssistedRadio', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('damagedVehicleCntAssistedStun', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('isNotSpotted', bool, True, None, 'max', ENTRY_TYPE.COMMON), 
 ('isAnyHitReceivedWhileCapturing', bool, False, None, 'max', ENTRY_TYPE.COMMON), 
 ('damageAssistedRadioWhileInvisible', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('damageAssistedTrackWhileInvisible', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('damageAssistedStunWhileInvisible', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('damageEventList', dict, {}, None, 'joinTargetEventLists', ENTRY_TYPE.COMMON), 
 ('stunEventList', dict, {}, None, 'joinTargetEventLists', ENTRY_TYPE.COMMON), 
 ('assistEventList', dict, {}, None, 'joinTargetEventLists', ENTRY_TYPE.COMMON), 
 ('damageFromEnemiesEventList', dict, {}, None, 'joinTargetEventLists', ENTRY_TYPE.COMMON), 
 ('multiDamageEvents', dict, {}, None, 'joinDicts', ENTRY_TYPE.COMMON), 
 ('multiStunEvents', dict, {}, None, 'joinDicts', ENTRY_TYPE.COMMON), 
 ('inBattleMaxSniperSeries', int, 0, None, 'max', ENTRY_TYPE.COMMON), 
 ('inBattleMaxKillingSeries', int, 0, None, 'max', ENTRY_TYPE.COMMON), 
 ('inBattleMaxPiercingSeries', int, 0, None, 'max', ENTRY_TYPE.COMMON), 
 ('firstDamageTime', int, 0, None, 'min', ENTRY_TYPE.COMMON), 
 ('consumedAmmo', None, None, None, 'skip', ENTRY_TYPE.COMMON), 
 ('extServer', dict, {}, BunchProxyPacker(VEH_CELL_RESULTS_EXTS['extServer']), 'joinExts', ENTRY_TYPE.COMMON), 
 ('directEnemyHits', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('explosionEnemyHits', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('piercingEnemyHits', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('indirectEnemyHits', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('enemyHits', int, 0, None, 'sum', ENTRY_TYPE.COMMON)])

VEH_CELL_RESULTS = _VEH_CELL_RESULTS_PUBLIC + _VEH_CELL_RESULTS_PRIVATE + _VEH_CELL_RESULTS_SERVER

_VEH_BASE_RESULTS_PUBLIC = Meta([
 ('accountDBID', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('typeCompDescr', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('index', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('deathReason', int, -1, None, 'skip', ENTRY_TYPE.COMMON), 
 ('team', int, 1, None, 'skip', ENTRY_TYPE.COMMON), 
 ('kills', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('spotted', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('damaged', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('stunned', int, 0, None, 'sum', ENTRY_TYPE.COMMON)])

_VEH_BASE_RESULTS_PRIVATE = Meta([
 ('xpPenalty', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('creditsPenalty', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('creditsContributionIn', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('creditsContributionOut', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('originalCreditsToDraw', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('creditsToDraw', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('damageBeforeTeamWasDamaged', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('killsBeforeTeamWasDamaged', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('percentFromTotalTeamDamage', float, 0.0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('percentFromSecondBestDamage', float, 0.0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('killedAndDamagedByAllSquadmates', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('damagedWhileMoving', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('damagedWhileEnemyMoving', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('committedSuicide', bool, False, None, 'max', ENTRY_TYPE.COMMON), 
 ('crystal', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('eventCoin', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('piggyBank', int, 0, None, 'sum', ENTRY_TYPE.COMMON)])

_VEH_BASE_RESULTS_SERVER = Meta([
 ('spottedBeforeWeBecameSpotted', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('spottedAndDamagedSPG', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('damageList', list, [], None, 'extend', ENTRY_TYPE.COMMON), 
 ('killList', list, [], None, 'extend', ENTRY_TYPE.COMMON), 
 ('vehLockTimeFactor', float, 0.0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('misc', dict, {}, None, 'any', ENTRY_TYPE.COMMON), 
 ('vehsByClass', dict, {}, None, 'any', ENTRY_TYPE.COMMON)])

VEH_FULL_RESULTS_UPDATE = Meta([
 ('originalCredits', int, 0, None, 'sum', ENTRY_TYPE.COMMON),  
 ('creditsReplay', str, '', ValueReplayPacker(), 'skip', ENTRY_TYPE.COMMON), 
 ('originalXP', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('xpReplay', str, '', ValueReplayPacker(), 'skip', ENTRY_TYPE.COMMON), 
 ('originalFreeXP', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('freeXPReplay', str, '', ValueReplayPacker(), 'skip', ENTRY_TYPE.COMMON), 
 ('originalTMenXP', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('tmenXPReplay', str, '', ValueReplayPacker(), 'skip', ENTRY_TYPE.COMMON), 
 ('tmenXP', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('originalGold', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('goldReplay', str, '', ValueReplayPacker(), 'skip', ENTRY_TYPE.COMMON), 
 ('gold', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('originalCrystal', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('crystalReplay', str, '', ValueReplayPacker(), 'skip', ENTRY_TYPE.COMMON), 
 ('originalEventCoin', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('eventCoinReplay', str, '', ValueReplayPacker(), 'skip', ENTRY_TYPE.COMMON), 
 ('factualXP', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('factualFreeXP', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('factualCredits', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('subtotalCredits', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('subtotalXP', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('subtotalFreeXP', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('subtotalTMenXP', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('subtotalGold', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('subtotalCrystal', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('subtotalEventCoin', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('eventCreditsList', list, [], None, 'skip', ENTRY_TYPE.COMMON), 
 ('eventXPList', list, [], None, 'skip', ENTRY_TYPE.COMMON), 
 ('eventFreeXPList', list, [], None, 'skip', ENTRY_TYPE.COMMON), 
 ('eventTMenXPList', list, [], None, 'skip', ENTRY_TYPE.COMMON), 
 ('eventGoldList', list, [], None, 'skip', ENTRY_TYPE.COMMON), 
 ('eventCrystalList', list, [], None, 'skip', ENTRY_TYPE.COMMON), 
 ('eventEventCoinList', list, [], None, 'skip', ENTRY_TYPE.COMMON), 
 ('eventCreditsFactor100List', list, [], None, 'skip', ENTRY_TYPE.COMMON), 
 ('eventXPFactor100List', list, [], None, 'skip', ENTRY_TYPE.COMMON), 
 ('eventFreeXPFactor100List', list, [], None, 'skip', ENTRY_TYPE.COMMON), 
 ('eventTMenXPFactor100List', list, [], None, 'skip', ENTRY_TYPE.COMMON), 
 ('eventGoldFactor100List', list, [], None, 'skip', ENTRY_TYPE.COMMON), 
 ('originalXPPenalty', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('originalCreditsPenalty', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('originalCreditsContributionIn', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('originalCreditsContributionOut', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('premiumVehicleXP', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('premiumVehicleXPFactor100', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('squadXP', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('squadXPFactor100', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('referral20XP', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('referral20XPFactor100', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('referral20Credits', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('referral20CreditsFactor100', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('premiumXPFactor100', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('premiumPlusXPFactor100', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('appliedPremiumXPFactor100', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('premiumTmenXPFactor100', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('premiumPlusTmenXPFactor100', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('appliedPremiumTmenXPFactor100', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('premiumCreditsFactor100', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('premiumPlusCreditsFactor100', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('appliedPremiumCreditsFactor100', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('premSquadCreditsFactor100', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('originalPremSquadCredits', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('premSquadCredits', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('dailyXPFactor10', int, 0, None, 'max', ENTRY_TYPE.COMMON), 
 ('additionalXPFactor10', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('igrXPFactor10', int, 0, None, 'max', ENTRY_TYPE.COMMON), 
 ('aogasFactor10', int, 0, None, 'max', ENTRY_TYPE.COMMON), 
 ('refSystemXPFactor10', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('fairplayFactor10', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('orderCredits', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('orderXP', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('orderFreeXP', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('orderTMenXP', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('orderCreditsFactor100', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('orderXPFactor100', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('orderFreeXPFactor100', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('orderTMenXPFactor100', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('boosterCredits', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('boosterXP', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('boosterFreeXP', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('boosterTMenXP', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('boosterCreditsFactor100', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('boosterXPFactor100', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('boosterFreeXPFactor100', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('boosterTMenXPFactor100', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('playerRankXP', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('playerRankXPFactor100', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('isPremium', bool, False, None, 'any', ENTRY_TYPE.COMMON), 
 ('premMask', int, 0, None, 'any', ENTRY_TYPE.COMMON), 
 ('xpByTmen', list, [], None, 'skip', ENTRY_TYPE.COMMON), 
 ('autoRepairCost', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('autoLoadCost', tuple, (0, 0), None, 'skip', ENTRY_TYPE.COMMON), 
 ('autoEquipCost', tuple, (0, 0, 0), None, 'skip', ENTRY_TYPE.COMMON), 
 ('prevMarkOfMastery', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('markOfMastery', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('dossierPopUps', list, [], None, 'skip', ENTRY_TYPE.COMMON), 
 ('vehTypeLockTime', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('serviceProviderID', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('marksOnGun', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('movingAvgDamage', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('damageRating', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('battleNum', int, 0, None, 'skip', ENTRY_TYPE.COMMON)]) + _PRIVATE_EVENT_RESULTS
 
_VEH_FULL_RESULTS_PRIVATE = Meta([
 ('questsProgress', dict, {}, None, 'joinDicts', ENTRY_TYPE.COMMON), 
 ('c11nProgress', dict, {}, None, 'skip', ENTRY_TYPE.COMMON), 
 ('originalCreditsToDrawSquad', int, 0, None, 'sum', ENTRY_TYPE.COMMON), 
 ('originalCreditsPenaltySquad', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('originalCreditsContributionInSquad', int, 0, None, 'skip', ENTRY_TYPE.COMMON), 
 ('originalCreditsContributionOutSquad', int, 0, None, 'sum', ENTRY_TYPE.COMMON)])

VEH_FULL_RESULTS_SERVER = Meta([
 ('eventGoldByEventID', dict, {}, None, 'skip', ENTRY_TYPE.COMMON)])

VEH_BASE_RESULTS = _VEH_CELL_RESULTS_PUBLIC + _VEH_BASE_RESULTS_PUBLIC + _VEH_CELL_RESULTS_PRIVATE + _VEH_BASE_RESULTS_PRIVATE + _VEH_CELL_RESULTS_SERVER + _VEH_BASE_RESULTS_SERVER
VEH_PUBLIC_RESULTS = _VEH_CELL_RESULTS_PUBLIC + _VEH_BASE_RESULTS_PUBLIC
VEH_FULL_RESULTS = _VEH_CELL_RESULTS_PUBLIC + _VEH_BASE_RESULTS_PUBLIC + _VEH_CELL_RESULTS_PRIVATE + _VEH_BASE_RESULTS_PRIVATE + VEH_FULL_RESULTS_UPDATE + _VEH_FULL_RESULTS_PRIVATE
VEH_PUBLIC_RESULTS = _VEH_CELL_RESULTS_PUBLIC + _VEH_BASE_RESULTS_PUBLIC

class UNIT_CLAN_MEMBERSHIP:
    NONE = 0
    ANY = 1
    SAME = 2


def dictToList(indices, d):
    l = [
     None] * len(indices)
    for name, index in indices.iteritems():
        l[index] = d[name]

    return l


def listToDict(names, l):
    d = {}
    for x in enumerate(names):
        d[x[1]] = l[x[0]]

    return d


class _VehicleInteractionDetailsItem(object):

    @staticmethod
    def __fmt2py(format):
        if format in ('f', ):
            return float
        return int

    def __init__(self, values, offset):
        self.__values = values
        self.__offset = offset

    def __getitem__(self, key):
        return self.__values[(self.__offset + VEH_INTERACTION_DETAILS_INDICES[key])]

    def __setitem__(self, key, value):
        self.__values[self.__offset + VEH_INTERACTION_DETAILS_INDICES[key]] = min(self.__fmt2py(VEH_INTERACTION_DETAILS_TYPES[key])(value), VEH_INTERACTION_DETAILS_MAX_VALUES[key])

    def __str__(self):
        return str(dict(self))

    def __iter__(self):
        return izip(VEH_INTERACTION_DETAILS_NAMES, self.__values[self.__offset:])


class VehicleInteractionDetails(object):

    def __init__(self, uniqueVehIDs, values):
        self.__uniqueVehIDs = uniqueVehIDs
        self.__values = values
        size = len(VEH_INTERACTION_DETAILS)
        self.__offsets = dict((x[1], x[0] * size) for x in enumerate(uniqueVehIDs))

    @staticmethod
    def fromPacked(packed):
        count = len(packed) / struct.calcsize(('').join(['<2I', VEH_INTERACTION_DETAILS_LAYOUT]))
        packedVehIDsLayout = '<%dI' % (2 * count,)
        packedVehIDsLen = struct.calcsize(packedVehIDsLayout)
        flatIDs = struct.unpack(packedVehIDsLayout, packed[:packedVehIDsLen])
        uniqueVehIDs = []
        for i in xrange(0, len(flatIDs), 2):
            uniqueVehIDs.append((flatIDs[i], flatIDs[(i + 1)]))

        values = struct.unpack('<' + VEH_INTERACTION_DETAILS_LAYOUT * count, packed[packedVehIDsLen:])
        return VehicleInteractionDetails(uniqueVehIDs, values)

    def __getitem__(self, uniqueVehID):
        if not isinstance(uniqueVehID, tuple):
            raise UserWarning(('Argument uniqueVehID should be tuple: {}').format(uniqueVehID))
        offset = self.__offsets.get(uniqueVehID, None)
        if offset is None:
            self.__uniqueVehIDs.append(uniqueVehID)
            offset = len(self.__values)
            self.__values += VEH_INTERACTION_DETAILS_INIT_VALUES
            self.__offsets[uniqueVehID] = offset
        return _VehicleInteractionDetailsItem(self.__values, offset)

    def __contains__(self, uniqueVehID):
        if not isinstance(uniqueVehID, tuple):
            raise UserWarning(('Argument uniqueVehID should be tuple: {}').format(uniqueVehID))
        return uniqueVehID in self.__offsets

    def __str__(self):
        return str(self.toDict())

    def pack(self):
        count = len(self.__uniqueVehIDs)
        flatIDs = []
        for uniqueID in self.__uniqueVehIDs:
            flatIDs.append(uniqueID[0])
            flatIDs.append(uniqueID[1])

        try:
            packed = struct.pack(('<%dI' % (2 * count)), *flatIDs) + struct.pack(('<' + VEH_INTERACTION_DETAILS_LAYOUT * count), *self.__values)
        except Exception as e:
            #from debug_utils import LOG_ERROR
            #LOG_ERROR('PACKING EXCEPTION', e, str(self))
            packed = ''

        return packed

    def toDict(self):
        return dict([ ((vehID, vehIdx), dict(_VehicleInteractionDetailsItem(self.__values, offset))) for (vehID, vehIdx), offset in self.__offsets.iteritems()
                    ])