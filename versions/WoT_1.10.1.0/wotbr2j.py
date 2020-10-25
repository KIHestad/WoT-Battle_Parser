#################################################### 
# World of Tanks Battle Results to JSON            # 
# by BadButton at wotnumbers.com                   # 
# originally by Phalynx www.vbaddict.net (retired) # 
#################################################### 
import struct, json, time, sys, os, zlib, traceback, datetime
import cPickle, StringIO
import battle_results_shared
import battle_results_common
from itertools import izip 

VEH_INTERACTION_DETAILS_LEGACY = ('spotted', 'killed', 'hits', 'he_hits', 'pierced', 'damageDealt', 'damageAssisted', 'crits', 'fire') 
VEH_INTERACTION_DETAILS_INDICES_LEGACY = dict(((x[1], x[0]) for x in enumerate(VEH_INTERACTION_DETAILS_LEGACY))) 

VEHICLE_DEVICE_TYPE_NAMES = ('engine', 'ammoBay', 'fuelTank', 'radio', 'track', 'gun', 'turretRotator', 'surveyingDevice')
VEHICLE_TANKMAN_TYPE_NAMES = ('commander', 'driver', 'radioman', 'gunner', 'loader')

VEH_INTERACTION_DETAILS = (
 ('spotted', 'B', 1, 0),
 ('deathReason', 'b', 10, -1),
 ('directHits', 'H', 65535, 0),
 ('secondaryDirectHits', 'H', 65535, 0),
 ('explosionHits', 'H', 65535, 0),
 ('piercings', 'H', 65535, 0),
 ('secondaryPiercings', 'H', 65535, 0),
 ('damageDealt', 'H', 65535, 0),
 ('damageAssistedTrack', 'H', 65535, 0),
 ('damageAssistedRadio', 'H', 65535, 0),
 ('damageAssistedStun', 'H', 65535, 0),
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
VEH_INTERACTION_DETAILS_MAX_VALUES = dict(((x[0], x[2]) for x in VEH_INTERACTION_DETAILS))
VEH_INTERACTION_DETAILS_INIT_VALUES = [ x[3] for x in VEH_INTERACTION_DETAILS ]
VEH_INTERACTION_DETAILS_LAYOUT = ''.join([ x[1] for x in VEH_INTERACTION_DETAILS ])
VEH_INTERACTION_DETAILS_INDICES = dict(((x[1][0], x[0]) for x in enumerate(VEH_INTERACTION_DETAILS)))
VEH_INTERACTION_DETAILS_TYPES = dict(((x[0], x[1]) for x in VEH_INTERACTION_DETAILS))
  
  
parser = dict()
parser['version'] = "1.10.1.0"
parser['name'] = 'http://wotnumbers.com'
parser['processingTime'] = int(time.mktime(time.localtime()))

def usage(): 
    print str(sys.argv[0]) + 'battleresult-filename.dat [options]'
    print 'Options:'
    print '-f Formats output result to JSON pretty print (includes line breaks and indents)'
    print '-l Logging to file enabled, output to file: wotbr2j_log.txt'

  
def main(): 

    #import struct, json, time, sys, os, shutil, datetime
    global filename_source, filename_target, option_format, parser, option_logging, log_file
    global cachefile 
    
    cachefile = None
    option_format = 0
    option_logging = 0

    if len(sys.argv) == 1: 
        usage() 
        sys.exit(2) 

    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    for argument in sys.argv:
        #ironpython modified
        if argument == "-f": 
            option_format = 1
        if argument == "-l": 
            option_logging = 1
            log_file = os.path.join(script_dir, "wotbr2j_log.txt")

    filename_source = str(sys.argv[1])

    printmessage('', 1)
    printmessage('### WoT Battle Result to Json - version ' + parser['version'] + ' ###', 1) 
    printmessage('Time: ' + str(datetime.datetime.now()), 1)
    printmessage('Encoding: ' + str(sys.getdefaultencoding()) + ' - ' + str(sys.getfilesystemencoding()), 1)
    if argument == "-l":
        printmessage('Logging to file: ' + log_file, 0) 
    printmessage('Processing file: ' + filename_source, 1) 
      
    filename_target = os.path.splitext(filename_source)[0] 
    filename_target = filename_target + '.json' 
    
    if not os.path.exists(filename_source) or not os.path.isfile(filename_source):
        exitwitherror('Battle Result does not exists! file: ' + filename_source)
    if not os.access(filename_source, os.R_OK):
        exitwitherror('Cannot read Battle result, read-access was denied for file: ' + filename_source)

    cachefile = open(filename_source, 'rb') 
              
    try: 
        legacyBattleResultVersion, battleResults = cPickle.load(cachefile)
    except Exception, e: 
        exitwitherror('Battle Result cannot be read (pickle could not be read) ' + e.message) 

    if not 'battleResults' in locals(): 
        exitwitherror('Battle Result cannot be read (battleResults class does not exist)') 
        
    # Process file
    printmessage('Start processing', 1)
    issuccess, bresult = convertToFullForm(battleResults) 
    if issuccess == 0:
        printmessage("Failed processing battle: %s" % (bresult), 1)
        exitwitherror('Battle result cannot be read')
    
    if not 'personal' in bresult:
        exitwitherror('Battle Result cannot be read (personal class does not exist)')
    
    if len(list(bresult['personal'].keys())) < 10:
        for vehTypeCompDescr, ownResults in bresult['personal'].copy().iteritems():
            if type(ownResults) is dict:
                if 'details' in ownResults:
                    ownResults['details'] = handleDetailsCrits(ownResults['details'])
                
                for field in ('damageEventList', 'xpReplay', 'creditsReplay', 'tmenXPReplay', 'fortResourceReplay', 'goldReplay', 'freeXPReplay'):
                    ownResults[field] = None
                
            bresult['personal'][vehTypeCompDescr] = ownResults
    
    parser['result'] = 'ok'
    bresult['parser'] = parser
    
    # write json file now
    dumpjson(bresult) 

    printmessage('### Done ###', 1) 
    printmessage('', 0) 
    cachefile.close()
    # sys.exit(0) 

def convertToFullForm(compactForm): 
    # data structures copied to classes with short name
    brs = battle_results_shared #version 1.10.0.4
    brc = battle_results_common #from version 1.10.1.0

    #read raw binary data from battle file
    arenaUniqueID, avatarResults, battle_results, pickled = compactForm
    
    #convert to readable data
    battle_results = Unpickler.loads(zlib.decompress(battle_results))
    avatarResults = Unpickler.loads(zlib.decompress(avatarResults))

    #split battle_result 
    battle_results = battle_results.items()[0]
    tankId = battle_results[0]
    battle_results = battle_results[1]

    
    try:
        #prepare result class, add some initial values
        personal = {}
        br2jResult = {
            'arenaUniqueID': arenaUniqueID,
            'tankId': tankId,
            'personal': personal,
            'common': {},
            'players': {},
            'vehicles': {},
            'avatars': {}
        }

        #check for valid battle result   
        if len(brc.BATTLE_RESULTS) + 1 != len(battle_results):
           structLen = str(len(brc.BATTLE_RESULTS) + 1) 
           dataLen = str(len(battle_results))
           return 0, {'error': 'Wrong number of items in class: BATTLE_RESULTS (found: {}, expecting {})'.format(dataLen, structLen)}
           
        
        personal['avatar'] = battle_results = brc.BATTLE_RESULTS_META.unpackWthoutChecksum(battle_results)

        # for vehTypeCompDescr, ownResults in fullResultsList.iteritems():
        #     vehPersonal = personal[vehTypeCompDescr] = battle_results_data.VEH_FULL_RESULTS.unpackWthoutChecksum(ownResults)
        #     if type(vehPersonal) is dict:
        #         try:
        #             vehPersonal['details'] = brc.VehicleInteractionDetails.fromPacked(vehPersonal['details']).toDict()
        #         except Exception: 
        #             return 0, {}
        #         vehPersonal['isPrematureLeave'] = avatarResults['isPrematureLeave']
        #         vehPersonal['fairplayViolations'] = avatarResults['fairplayViolations']

        # commonAsList, playersAsList, vehiclesAsList, avatarsAsList = Unpickler.loads(zlib.decompress(pickled))
                
        # fullForm['common'] = brc.COMMON_RESULTS.unpackWthoutChecksum(commonAsList)
        # #Fix from WoT 1.9.1.0
        # if 'accountCompDescr' in fullForm['common']:
        #     del fullForm['common']['accountCompDescr']

        # for accountDBID, playerAsList in playersAsList.iteritems():
        #     fullForm['players'][accountDBID] = battle_results_data.PLAYER_INFO.unpack(playerAsList)

        # for accountDBID, avatarAsList in avatarsAsList.iteritems():
        #     fullForm['avatars'][accountDBID] = battle_results_data.AVATAR_PUBLIC_RESULTS.unpackWthoutChecksum(avatarAsList)

        # for vehicleID, vehiclesInfo in vehiclesAsList.iteritems():
        #     fullForm['vehicles'][vehicleID] = []
        #     for vehTypeCompDescr, vehicleInfo in vehiclesInfo.iteritems():
        #         fullForm['vehicles'][vehicleID].append(battle_results_data.VEH_PUBLIC_RESULTS.unpackWthoutChecksum(vehicleInfo))
        return 1, br2jResult 
    except IndexError, i:
        printmessage(traceback.format_exc(i), 1)
        return 0, {'error': '%s' % i.message}
    except KeyError, i:
        printmessage(traceback.format_exc(i), 1)
        return 0, {'error': 'Missing key in data: %s' % i.message}
    except Exception, e:
        printmessage(traceback.format_exc(e), 1)
        return 0, {'error': e}
    

def prepareForJSON(bresult):
    ## Fix values in personal class for non-valid json parameters
    if 'personal' in bresult:
        for subLevel, subLevelValues in bresult['personal'].copy().iteritems():

            #Remove unwanted entries
            if subLevel == 'avatar': 
                if 'avatarDamageEventList' in bresult['personal'][subLevel]:
                    del bresult['personal'][subLevel]['avatarDamageEventList']
                if 'squadBonusInfo' in bresult['personal'][subLevel]:
                    del bresult['personal'][subLevel]['squadBonusInfo']
            else:
                if 'c11nProgress' in bresult['personal'][subLevel]:
                    del bresult['personal'][subLevel]['c11nProgress']

            #Inspect and clean up values
            if subLevelValues is not None:
                #MC: This is a hack to remove suspicious entries ending with "The resulting string is not a valid number", typically removing binary 
                for detail in subLevelValues:
                    if (type(subLevelValues[detail]) is str):
                        subLevelValues[detail] = 0
                #Fix detail section having array as key
                if 'details' in subLevelValues:
                    newValues = arrayDictToString(subLevelValues['details'])
                    bresult['personal'][subLevel]['details'] = newValues
                #Fix for club section, old code from Phalynx, unsure if relevant any more or what it does ^_^
                if 'club' in subLevelValues:
                    if subLevelValues['club'] is not None:
                        if 'club' in subLevelValues:
                            if 'clubDossierPopUps' in subLevelValues['club']:
                                oldClubDossier = subLevelValues['club']['clubDossierPopUps'].copy()
                                subLevelValues['club']['clubDossierPopUps'] = dict()
                                for achievement, amount in oldClubDossier.iteritems():
                                    bresult['personal'][subLevel]['club']['clubDossierPopUps'][str(list(achievement)[0]) + '-' + str(list(achievement)[1])] = amount
        
        if len(bresult['personal'].copy())>1 and len(bresult['personal'].copy())<10 :
            pass
        
        #for subLevel, subLevelValues in bresult['personal'].copy().iteritems():
        #    if subLevelValues is not None:
        #        for detail in subLevelValues:
        #            if (type(subLevelValues[detail]) is str): # MC: This is a hack to remove suspicious entries. The resulting string is not a valid number.
        #                subLevelValues[detail] = 0
                    
        #        if 'details' in subLevelValues:
        #            newValues = detailsDictToString(subLevelValues['details'])
        #            bresult['personal'][subLevel]['details'] = newValues
    return bresult
            
def arrayDictToString(mydict):
    mydictcopy = dict()
    
    if not type(mydict) is dict:
        return mydictcopy    
    
    for key, value in mydict.iteritems():
        value['vehicleid'] = key[0]
        value['typeCompDescr'] = key[1]
        mydictcopy[str(key[0]) + '-' + str(key[1])] = value
    return mydictcopy
    
def exitwitherror(message, e=None, abort=False):
    global parser, cachefile
    if e is None:
        printmessage(message, 1)
    else:
        printmessage(message + e.message, 1)
        printmessage(traceback.format_exc(e), 1)
    if not abort:
        dossierheader = dict() 
        dossierheader['parser'] = dict() 
        dossierheader['parser']['result'] = "error"
        dossierheader['parser']['message'] = message 
        dumpjson(dossierheader) 
    if cachefile is not None:
        cachefile.close() 
    sys.exit(1) 

def dumpjson(bresult): 
    global option_logging, option_format, filename_target
    bresult = prepareForJSON(bresult)
    try:
        finalfile = open(filename_target, 'w') 
        
        # Debug section
        #test = json.dumps(bresult['arenaUniqueID'], ensure_ascii=False)
        #test = json.dumps(bresult['avatars'], ensure_ascii=False)
        #test = json.dumps(bresult['common'], ensure_ascii=False)
        #test = json.dumps(bresult['parser'], ensure_ascii=False)
        #test = json.dumps(bresult['players'], ensure_ascii=False)
        #test = json.dumps(bresult['vehicles'], ensure_ascii=False)
        #vehTypeCompDescr, ownResults = bresult['personal']
        #vehTypeCompDescrData = bresult['personal'][vehTypeCompDescr]
        #ownResultsData = bresult['personal'][ownResults]
        #test = json.dumps(vehTypeCompDescrData, ensure_ascii=False)
        #test = json.dumps(ownResultsData, ensure_ascii=False)
        
        if option_format == 1: 
            finalfile.write(json.dumps(bresult, ensure_ascii=False, skipkeys=True, sort_keys=True, indent=4)) 
        else: 
            finalfile.write(json.dumps(bresult, ensure_ascii=False, skipkeys=True))        
        # IRONPYTHON MODIFIED: close dossier output file
        finalfile.close()
    except Exception, e:
        if finalfile is not None: 
            finalfile.close() # IRONPYTHON MODIFIED: close dossier output file
        exitwitherror("Exception: ", e, abort=True)

def dictToList(indices, d): 
    l = [None] * len(indices) 
    for name, index in indices.iteritems(): 
        l[index] = d[name] 
    return l 

def listToDict(names, l): 
    d = {} 
    for x in enumerate(names): 
        d[x[1]] = l[x[0]] 
    return d 

def print_array(oarray):
    print json.dumps(oarray, sort_keys=True, indent=4)

def handleDetailsCrits(details):
    if type(details) is dict and len(details) > 0: 
        for vehicleid, detail_values in details.items(): 
            details[vehicleid]['critsDestroyedTankmenList'] = getDestroyedTankmen(detail_values)
            details[vehicleid]['critsCriticalDevicesList'] = getCriticalDevicesList(detail_values)
            details[vehicleid]['critsDestroyedDevicesList'] = getDestroyedDevicesList(detail_values)
            details[vehicleid]['critsCount'] = len(details[vehicleid]['critsDestroyedTankmenList']) + len(details[vehicleid]['critsDestroyedTankmenList']) + len(details[vehicleid]['critsDestroyedTankmenList'])
    return details

def getDestroyedTankmen(detail_values):
    destroyedTankmenList = [] 
    if detail_values['crits']  >0: 
        destroyedTankmen = detail_values['crits'] >> 24 & 255
          
        for shift in range(len(VEHICLE_TANKMAN_TYPE_NAMES)): 
            if 1 << shift & destroyedTankmen: 
                destroyedTankmenList.append(VEHICLE_TANKMAN_TYPE_NAMES[shift]) 
    return destroyedTankmenList  

def getCriticalDevicesList(detail_values):
    criticalDevicesList = [] 
    if detail_values['crits'] > 0: 
        criticalDevices = detail_values['crits'] & 4095
          
        for shift in range(len(VEHICLE_DEVICE_TYPE_NAMES)): 
            if 1 << shift & criticalDevices: 
                criticalDevicesList.append(VEHICLE_DEVICE_TYPE_NAMES[shift]) 
    return criticalDevicesList
        
def getDestroyedDevicesList(detail_values):
    destroyedDevicesList = [] 
    if detail_values['crits'] > 0: 
        destroyedDevices = detail_values['crits'] >> 12 & 4095
        for shift in range(len(VEHICLE_DEVICE_TYPE_NAMES)): 
        
            if 1 << shift & destroyedDevices: 
                destroyedDevicesList.append(VEHICLE_DEVICE_TYPE_NAMES[shift]) 
    return destroyedDevicesList 
  
def printmessage(logtext, to_console): 
    #import datetime, os 

    if to_console == 1:
        print str(logtext)
        
    if option_logging == 1:
        now = datetime.datetime.now() 
        message = str(now.strftime("%Y-%m-%d %H:%M:%S")) + " - " + str(logtext) + "\r\n"
        logFile = open(log_file, "a+b") 
        logFile.write(message) 
        logFile.close() 
    
class _VehicleInteractionDetailsItem(object): 
    
    def __init__(self, values, offset): 
        self.__values = values 
        self.__offset = offset 
    def __getitem__(self, key): 
        return self.__values[self.__offset + VEH_INTERACTION_DETAILS_INDICES[key]] 
    def __setitem__(self, key, value): 
        self.__values[self.__offset + VEH_INTERACTION_DETAILS_INDICES[key]] = min(int(value), VEH_INTERACTION_DETAILS_MAX_VALUES[key]) 
    def __iter__(self): 
        return izip(VEH_INTERACTION_DETAILS_NAMES, self.__values[self.__offset:]) 


class VehicleInteractionDetails(object): 
  
    def __init__(self, vehicleIDs, values): 
        self.__vehicleIDs = vehicleIDs 
        self.__values = values 
        size = len(VEH_INTERACTION_DETAILS) 
        self.__offsets = dict(((x[1], x[0] * size) for x in enumerate(self.__vehicleIDs))) 
  
    @staticmethod
    def fromPacked(packed): 
        count = len(packed) / struct.calcsize(''.join(['<I', VEH_INTERACTION_DETAILS_LAYOUT])) 
        packedVehIDsLayout = '<%dI' % (count,) 
        packedVehIDsLen = struct.calcsize(packedVehIDsLayout) 
        vehicleIDs = struct.unpack(packedVehIDsLayout, packed[:packedVehIDsLen]) 
        values = struct.unpack('<' + VEH_INTERACTION_DETAILS_LAYOUT * count, packed[packedVehIDsLen:]) 
        return VehicleInteractionDetails(vehicleIDs, values) 
  
    def __getitem__(self, vehicleID): 
        offset = self.__offsets.get(vehicleID, None) 
        if offset is None: 
            self.__vehicleIDs.append(vehicleID) 
            offset = len(self.__values) 
            self.__values += VEH_INTERACTION_DETAILS_INIT_VALUES 
  
            self.__offsets[vehicleID] = offset 
        return _VehicleInteractionDetailsItem(self.__values, offset) 
  
    def __contains__(self, vehicleID): 
        return vehicleID in self.__offsets 
  
    def __str__(self): 
        return str(self.toDict()) 
  
    def pack(self): 
        count = len(self.__vehicleIDs) 
        packed = struct.pack(('<%dI' % count), *self.__vehicleIDs) + struct.pack(('<' + VEH_INTERACTION_DETAILS_LAYOUT * count), *self.__values) 
  
        return packed 
  
    def toDict(self): 
        return dict([ (vehID, dict(_VehicleInteractionDetailsItem(self.__values, offset))) for vehID, offset in self.__offsets.iteritems() ]) 
  
class _VehicleInteractionDetailsItem_LEGACY(object): 
  
    def __init__(self, values, offset): 
        self.__values = values 
        self.__offset = offset 
  
    def __getitem__(self, key): 
        return self.__values[self.__offset + VEH_INTERACTION_DETAILS_INDICES_LEGACY[key]] 
  
    def __setitem__(self, key, value): 
        self.__values[self.__offset + VEH_INTERACTION_DETAILS_INDICES_LEGACY[key]] = min(int(value), 65535) 
  
    def __str__(self): 
        return str(dict(self)) 
  
    def __iter__(self): 
        return izip(VEH_INTERACTION_DETAILS_LEGACY, self.__values[self.__offset:]) 
  
  
class VehicleInteractionDetails_LEGACY(object): 
  
    def __init__(self, vehicleIDs, values): 
        self.__vehicleIDs = vehicleIDs 
        self.__values = values 
        size = len(VEH_INTERACTION_DETAILS_LEGACY) 
        self.__offsets = dict(((x[1], x[0] * size) for x in enumerate(self.__vehicleIDs))) 
  
    @staticmethod
    def fromPacked(packed): 
        size = len(VEH_INTERACTION_DETAILS_LEGACY) 
        count = len(packed) / struct.calcsize('I%dH' % size) 
        unpacked = struct.unpack('%dI%dH' % (count, count * size), packed) 
        vehicleIDs = unpacked[:count] 
        values = unpacked[count:] 
        return VehicleInteractionDetails_LEGACY(vehicleIDs, values) 
  
    def __getitem__(self, vehicleID): 
        offset = self.__offsets.get(vehicleID, None) 
        if offset is None: 
            self.__vehicleIDs.append(vehicleID) 
            offset = len(self.__values) 
            size = len(VEH_INTERACTION_DETAILS_LEGACY) 
            self.__values += [0] * size 
            self.__offsets[vehicleID] = offset 
        return _VehicleInteractionDetailsItem_LEGACY(self.__values, offset) 
  
    def __contains__(self, vehicleID): 
        return vehicleID in self.__offsets 
  
    def __str__(self): 
        return str(self.toDict()) 
  
    def pack(self): 
        count = len(self.__vehicleIDs) 
        size = len(VEH_INTERACTION_DETAILS_LEGACY) 
        packed = struct.pack(('%dI' % count), *self.__vehicleIDs) + struct.pack(('%dH' % count * size), *self.__values) 
        return packed 
  
    def toDict(self): 
        return dict([ (vehID, dict(_VehicleInteractionDetailsItem_LEGACY(self.__values, offset))) for vehID, offset in self.__offsets.iteritems() ]) 


class Unpickler(object): 
    @classmethod
    def loads(cls, pickle_string):
        try:
            unpickler = cPickle.Unpickler(StringIO.StringIO(pickle_string))
            return unpickler.load()
        except Exception, e:
            cachefile.close()
            raise cPickle.UnpicklingError('Unpickler Error: ' + e.message)
            
    @classmethod
    def load(cls, pickle_file):
        try:
            unpickler = cPickle.Unpickler(pickle_file)
            return unpickler.load()
        
        except EOFError, er:
            # IRONPYTHON MODIFIED: close dossier input file
            cachefile.close()
            raise cPickle.UnpicklingError('Unpickler EOF Error: ' + er.message)
        
        except Exception, e:
            # IRONPYTHON MODIFIED: close dossier input file
            cachefile.close()
            raise cPickle.UnpicklingError('Unpickler Error: ' + e.message)

if __name__ == '__main__': 
    main() 