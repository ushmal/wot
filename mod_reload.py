import BigWorld
import Keys
import ResMgr
import Vehicle
import ProjectileMover
from messenger import MessengerEntry
from Avatar import PlayerAvatar
from gui.app_loader import g_appLoader
from gui.Scaleform.daapi.view.lobby.LobbyView import LobbyView
from Account import PlayerAccount
from gui import SystemMessages
#from gui.Scaleform.Minimap import Minimap
from gui.Scaleform.Battle import Battle
import constants
from constants import ARENA_PERIOD
from debug_utils import *
from functools import partial
SWF_FILE_NAME = 'marker_red.swf'

class MarkerReLoad(object):

    def __init__(self):
        self.application = __name__
        self.arenaPeriod = False
        self.startTime = 0
        self.arenaGuiTyps = 0
        self.extTanks = {}
        self.visible_list = []
        self.enemies_list = {}
        self.allies_list = {}
        self.timer_list = {}
        self.mod_markers = {}
        self.shoot_timer_list = {}
        self.timeOutReload = {}
        self.FlagTXT = True
        self.configModule()
        self.moduleMarker()

    def configModule(self):
        self.modEnable = True
        self.startAlliesEnable = True
        self.minimapEnable = False
        self.bonusBrotherhood = True
        self.bonusStimulator = False
        self.bonusAuto = True
        self.timeOutAutoReload = True
        self.timeOutReloadDelay = 3.0
        self.timeReloadCorrect = 0.0
        self.toggleKey = 'KEY_NUMPAD4'
        self.modOFFKey = 'KEY_NUMPAD6'
        self.modOFF = False
        self.unVisibleReload = False
        self.alliesEnable = True
        self.SWF_FILE_NAME_ENEMIES = 'marker_red.swf'
        self.SWF_FILE_NAME_ALLIES = 'marker_green.swf'
        self.marker_timeUpdate = 0.1
        self.marker_timeCorrect = 1.0
        self.configMarker = ResMgr.openSection('scripts/client/gui/mods/mod_reload.xml')
        if self.configMarker != None:
            self.modEnable = self.configMarker.readBool('modEnable')
            self.startAlliesEnable = self.configMarker.readBool('startAlliesEnable')
            self.minimapEnable = self.configMarker.readBool('minimapEnable')
            self.bonusBrotherhood = self.configMarker.readBool('bonusBrotherhood')
            self.bonusStimulator = self.configMarker.readBool('bonusStimulator')
            self.bonusAuto = self.configMarker.readBool('bonusAuto')
            self.timeOutAutoReload = self.configMarker.readBool('timeOutAutoReload')
            self.timeOutReloadDelay = self.configMarker.readInt('timeOutReloadDelay')
            self.timeReloadCorrect = self.configMarker.readInt('timeReloadCorrect')
            self.toggleKey = self.configMarker.readString('toggleKey')
            self.modOFFKey = self.configMarker.readString('modOFFKey')
            self.unVisibleReload = self.configMarker.readBool('unVisibleReload')
            self.alliesEnable = self.configMarker.readBool('alliesEnable')
            self.SWF_FILE_NAME_ENEMIES = self.configMarker.readString('SWF_FILE_NAME_ENEMIES')
            self.SWF_FILE_NAME_ALLIES = self.configMarker.readString('SWF_FILE_NAME_ALLIES')
            self.marker_timeUpdate = self.configMarker.readFloat('reload_tout')
            self.marker_timeCorrect = self.configMarker.readFloat('self.marker_timeCorrect')
            LOG_NOTE('XML config successfully loaded');
        return

    def moduleMarker(self):

        def new_showTracer(current, shooterID, shotID, isRicochet, effectsIndex, refStartPoint, velocity, gravity, maxShotDist):
            pre_showTracer(current, shooterID, shotID, isRicochet, effectsIndex, refStartPoint, velocity, gravity, maxShotDist)
            if self.modOFF:
                return
            else:
                #shooter = BigWorld.entity(shooterID)
                #if shooter is not None and self.minimapEnable:
                #    __MiniMapAndMarkReload(shooterID)
                __Reloading__Marker_Action(shooterID)
                return

        #def __MiniMapAndMarkReload(id, rlFlag = False):
        #    return

        def __Reloading__Marker_Action(id):
            global SWF_FILE_NAME
            if self.modOFF:
                return
            else:
                if __Remaining(id):
                    reload_time = __calculateReload(id)
                    if reload_time > 1.0 and self.modEnable:
                        flashID = str(''.join([str(id), 'vehicleMarkersManager']))
                        if not __getIsFriendly(id):
                            SWF_FILE_NAME = self.SWF_FILE_NAME_ENEMIES
                        else:
                            SWF_FILE_NAME = self.SWF_FILE_NAME_ALLIES
                        Mod_Marker = _VehicleMarkersManager()
                        self.mod_markers[flashID] = Mod_Marker
                        Mod_Marker.start(flashID)
                        try:
                            mm_handle = Mod_Marker.createMarker(BigWorld.entity(id))
                            if mm_handle is not None:
                                enout = BigWorld.time() + reload_time + self.marker_timeCorrect
                                Mod_Marker.showActionMarker(mm_handle, 'attack', int(reload_time))
                        except:
                            return
                        finally:

                            def marker_check():
                                try:
                                    stop_mark = True
                                    if __Remaining(id) and self.modEnable and not (__getIsFriendly(id) and not self.alliesEnable):
                                        if BigWorld.time() < enout:
                                            if self.mod_markers[flashID] == Mod_Marker:
                                                stop_mark = False
                                    if stop_mark or self.modOFF or not self.unVisibleReload and id not in self.visible_list:
                                        Mod_Marker.destroy_light(flashID)
                                    else:
                                        BigWorld.callback(self.marker_timeUpdate, marker_check)
                                except:
                                    Mod_Marker.destroy_light(flashID)

                            marker_check()

                return

        def __GetBonus(id):
            try:
                ventil_bonus = False
                rammer_bonus = False
                comander = 100
                loader = 100
                veh = BigWorld.player().arena.vehicles.get(id)
                for item in veh['vehicleType'].optionalDevices:
                    if item is not None and 'improvedVentilation' in item.name:
                        ventil_bonus = True
                    if item is not None and 'Rammer' in item.name:
                        rammer_bonus = True
                        continue

                bonusVBS = 0
                if ventil_bonus:
                    bonusVBS += 5
                if self.bonusBrotherhood or self.bonusAuto and BigWorld.player().arena.guiType == constants.ARENA_GUI_TYPE.COMPANY:
                    bonusVBS += 5
                if self.bonusStimulator or self.bonusAuto and BigWorld.player().arena.guiType == constants.ARENA_GUI_TYPE.COMPANY:
                    bonusVBS += 10
                comander_bonus = comander + bonusVBS
                loader_bonus = comander_bonus * 0.1 + bonusVBS + loader
                bonus = 1 / (1 + (loader_bonus - 100) * 0.00434294482)
                if rammer_bonus:
                    bonus *= 0.9
                return bonus
            except:
                return 1

        def __timeOutNoShoot(id):
            if id in self.timeOutReload:
                del self.timeOutReload[id]
            if id in self.shoot_timer_list:
                timer = BigWorld.time() - self.shoot_timer_list[id]
                veh = BigWorld.player().arena.vehicles.get(id)
                shortUserString = veh['vehicleType'].type.shortUserString
                reloadTime = veh['vehicleType'].gun['reloadTime']
                ammo = self.extTanks[id]['ammo']
                if not __getIsFriendly(id):
                    self.enemies_list.update({id: {'ammo': ammo,
                          'time': self.shoot_timer_list[id]}})
                else:
                    self.allies_list.update({id: {'ammo': ammo,
                          'time': self.shoot_timer_list[id]}})
                #__MiniMapAndMarkReload(id, True)

        def __calculateReload(id):
            try:
                veh = BigWorld.player().arena.vehicles.get(id)
                shortUserString = veh['vehicleType'].type.shortUserString
                reloadTime = veh['vehicleType'].gun['reloadTime']
                bonusReloadTime = reloadTime * __GetBonus(id)
                time = BigWorld.time()
                battleTime = time - self.startTime
                if bonusReloadTime > battleTime:
                    bonusReloadTime -= battleTime
                    return bonusReloadTime
                if id in self.timer_list:
                    if not self.timer_list[id]['shootFlag']:
                        reloadTimeResidue = bonusReloadTime - (time - self.timer_list[id]['time'])
                        if reloadTimeResidue > 0:
                            if id in self.timer_list:
                                del self.timer_list[id]
                            return reloadTimeResidue
                if id not in self.extTanks:
                    if not __getIsFriendly(id):
                        self.enemies_list[id]['time'] = time
                    else:
                        self.allies_list[id]['time'] = time
                    self.timer_list.update({id: {'time': time,
                          'shootFlag': True}})
                    return bonusReloadTime
                if self.timeOutAutoReload:
                    self.shoot_timer_list.update({id: time})
                    if id in self.timeOutReload:
                        BigWorld.cancelCallback(self.timeOutReload[id])
                    self.timeOutReload.update({id: BigWorld.callback(self.extTanks[id]['reloadTime'] * __GetBonus(id) + self.timeOutReloadDelay, partial(__timeOutNoShoot, id))})
                if not __getIsFriendly(id):
                    ammo = self.enemies_list[id]['ammo']
                    if ammo > 1:
                        ammo -= 1
                        bonusReloadTime = self.extTanks[id]['clipReloadTime']
                    else:
                        self.timer_list.update({id: {'time': time,
                              'shootFlag': True}})
                        ammo = self.extTanks[id]['ammo']
                        if id in self.shoot_timer_list:
                            del self.shoot_timer_list[id]
                    self.enemies_list.update({id: {'ammo': ammo,
                          'time': time}})
                if __getIsFriendly(id):
                    ammo = self.allies_list[id]['ammo']
                    if ammo > 1:
                        ammo -= 1
                        bonusReloadTime = self.extTanks[id]['clipReloadTime']
                    else:
                        self.timer_list.update({id: {'time': time,
                              'shootFlag': True}})
                        ammo = self.extTanks[id]['ammo']
                        if id in self.shoot_timer_list:
                            del self.shoot_timer_list[id]
                    self.allies_list.update({id: {'ammo': ammo,
                          'time': time}})
                return bonusReloadTime
            except:
                return 0

        def __Remaining(id):
            return __getBattleOn() and __getIsLive(id) and not __isPlayer(id)

        def __isPlayer(id):
            return BigWorld.player().playerVehicleID == id

        def __getBattleOn():
            return hasattr(BigWorld.player(), 'arena')

        def __getIsLive(id):
            return __getBattleOn() and BigWorld.player().arena.vehicles.get(id)['isAlive']

        def __getIsFriendly(id):
            return __getBattleOn() and BigWorld.player().arena.vehicles[BigWorld.player().playerVehicleID]['team'] == BigWorld.player().arena.vehicles[id]['team']

        def new_vehicle_onEnterWorld(current, vehicle):
            pre_vehicle_onEnterWorld(current, vehicle)
            if self.modOFF:
                return
            if not self.arenaPeriod:
                return
            if not __getIsLive(vehicle.id) or __isPlayer(vehicle.id):
                return
            id = vehicle.id
            if id not in self.visible_list:
                self.visible_list.append(id)
            veh = BigWorld.player().arena.vehicles.get(id)
            shortUserString = veh['vehicleType'].type.shortUserString
            reloadTime = veh['vehicleType'].gun['reloadTime']
            clip = veh['vehicleType'].gun['clip']
            burst = veh['vehicleType'].gun['burst']
            if clip[0] > 1:
                if id not in self.extTanks:
                    self.extTanks.update({id: {'reloadTime': reloadTime,
                          'clipReloadTime': clip[1],
                          'ammo': clip[0]}})
            time = BigWorld.time()
            battleTime = time - self.startTime
            bonusReloadTime = reloadTime * __GetBonus(id)
            if id in self.timer_list:
                reloadTimeResidue = bonusReloadTime - (time - self.timer_list[id]['time'])
                if reloadTimeResidue > 0:
                    self.timer_list[id]['shootFlag'] = False
                    __Reloading__Marker_Action(id)
                    return
            if not __getIsFriendly(id):
                if id not in self.enemies_list:
                    ammo = 1
                    self.enemies_list.update({id: {'ammo': ammo,
                          'time': time - bonusReloadTime}})
                if id in self.extTanks:
                    rlt = bonusReloadTime
                    bonusReloadTime = self.extTanks[id]['clipReloadTime']
                    timer = time - self.enemies_list[id]['time']
                    if timer >= bonusReloadTime - self.timeReloadCorrect:
                        ammo = self.extTanks[id]['ammo']
                        self.enemies_list[id]['ammo'] = ammo
                        bonusReloadTime = rlt
            if __getIsFriendly(id):
                if id not in self.allies_list:
                    ammo = 1
                    self.allies_list.update({id: {'ammo': ammo,
                          'time': time - bonusReloadTime}})
                if id in self.extTanks:
                    rlt = bonusReloadTime
                    bonusReloadTime = self.extTanks[id]['clipReloadTime']
                    timer = time - self.allies_list[id]['time']
                    if timer >= bonusReloadTime - self.timeReloadCorrect:
                        ammo = self.extTanks[id]['ammo']
                        self.allies_list[id]['ammo'] = ammo
                        bonusReloadTime = rlt
            if bonusReloadTime > battleTime:
                __Reloading__Marker_Action(id)

        def new_vehicle_onLeaveWorld(current, vehicle):
            pre_vehicle_onLeaveWorld(current, vehicle)
            id = vehicle.id
            if id in self.visible_list:
                self.visible_list.remove(id)

        def __onVehicleKilled(targetID, atackerID, *args):
            if self.modOFF:
                return
            id = targetID
            if id in self.visible_list:
                self.visible_list.remove(id)
            if self.enemies_list.has_key(id):
                del self.enemies_list[id]
            if self.allies_list.has_key(id):
                del self.allies_list[id]
            if self.timer_list.has_key(id):
                del self.timer_list[id]
            if self.shoot_timer_list.has_key(id):
                del self.shoot_timer_list[id]

        def __clearVars():
            self.visible_list = []
            self.enemies_list = {}
            self.allies_list = {}
            self.timer_list = {}
            self.mod_markers = {}
            self.extTanks = {}
            self.shoot_timer_list = {}
            self.timeOutReload = {}
            self.startTime = 0

        def new_startBattle(current):
            BigWorld.player().arena.onVehicleKilled += __onVehicleKilled
            self.arenaPeriod = False
            __clearVars()
            LOG_NOTE('Battle.afterCreate')
            old_startBattle(current)

        def new_stopBattle(current):
            BigWorld.player().arena.onVehicleKilled -= __onVehicleKilled
            self.arenaPeriod = False
            __clearVars()
            LOG_NOTE('Battle.beforeDelete')
            old_stopBattle(current)

        old_startBattle = Battle.afterCreate
        Battle.afterCreate = new_startBattle
        old_stopBattle = Battle.beforeDelete
        Battle.beforeDelete = new_stopBattle

        def vehicles_to_list():
            for id, entityVehicle in BigWorld.entities.items():
                if isinstance(entityVehicle, Vehicle.Vehicle) and not __isPlayer(id):
                    veh = BigWorld.player().arena.vehicles.get(id)
                    shortUserString = veh['vehicleType'].type.shortUserString
                    reloadTime = veh['vehicleType'].gun['reloadTime']
                    clip = veh['vehicleType'].gun['clip']
                    if clip[0] > 1:
                        self.extTanks.update({id: {'reloadTime': reloadTime,
                              'clipReloadTime': clip[1],
                              'ammo': clip[0]}})
                    if id not in self.visible_list:
                        self.visible_list.append(id)
                    if not __getIsFriendly(id):
                        if id not in self.enemies_list:
                            ammo = 1
                            self.enemies_list.update({id: {'ammo': ammo,
                                  'time': 0}})
                        if id in self.extTanks:
                            ammo = self.extTanks[id]['ammo']
                            self.enemies_list[id]['ammo'] = ammo
                    if __getIsFriendly(id):
                        if id not in self.allies_list:
                            ammo = 1
                            self.allies_list.update({id: {'ammo': ammo,
                                  'time': 0}})
                        if id in self.extTanks:
                            ammo = self.extTanks[id]['ammo']
                            self.allies_list[id]['ammo'] = ammo

        def new_onArenaPeriodChange(current, period, periodEndTime, periodLength, periodAdditionalInfo):
            pre_onArenaPeriodChange(current, period, periodEndTime, periodLength, periodAdditionalInfo)
            if period == ARENA_PERIOD.PREBATTLE:
                vehicles_to_list()
            if period == ARENA_PERIOD.BATTLE:
                self.arenaPeriod = True
                self.startTime = BigWorld.time()
                if self.startAlliesEnable:
                    for id in self.allies_list:
                        __Reloading__Marker_Action(id)

        pre_onArenaPeriodChange = PlayerAvatar._PlayerAvatar__onArenaPeriodChange
        PlayerAvatar._PlayerAvatar__onArenaPeriodChange = new_onArenaPeriodChange

        def new_PlayerHandleKey(current, isDown, key, mods):
            global g_appLoader
            if g_appLoader.getDefBattleApp() is not None:
                if self.modOFF and key == getattr(Keys, self.toggleKey, None) and isDown:
                    g_appLoader.getDefBattleApp().call('battle.PlayerMessagesPanel.ShowMessage', ['0', self.application + '  MOD-OFF', 'red'])
                    return True
                if not self.modOFF and key == getattr(Keys, self.modOFFKey, None) and isDown:
                    g_appLoader.getDefBattleApp().call('battle.PlayerMessagesPanel.ShowMessage', ['0', self.application + '  MOD-OFF', 'red'])
                    self.modOFF = True
                    __clearVars()
                    return True
                if self.modOFF and key == getattr(Keys, self.modOFFKey, None) and isDown:
                    g_appLoader.getDefBattleApp().call('battle.PlayerMessagesPanel.ShowMessage', ['0', self.application + '  MOD-ON', 'gold'])
                    self.modOFF = False
                    vehicles_to_list()
                if not self.modEnable and key == getattr(Keys, self.toggleKey, None) and isDown:
                    self.modEnable = True
                    g_appLoader.getDefBattleApp().call('battle.PlayerMessagesPanel.ShowMessage', ['0', self.application + '  ON', 'gold'])
                    return True
                if self.modEnable and key == getattr(Keys, self.toggleKey, None) and isDown:
                    if not self.alliesEnable:
                        self.alliesEnable = True
                        g_appLoader.getDefBattleApp().call('battle.PlayerMessagesPanel.ShowMessage', ['0', self.application + ' + allies  ON', 'gold'])
                        return True
                    self.alliesEnable = False
                    self.modEnable = False
                    g_appLoader.getDefBattleApp().call('battle.PlayerMessagesPanel.ShowMessage', ['0', self.application + '  OFF', 'red'])
            return old_PlayerHandleKey(current, isDown, key, mods)

        old_PlayerHandleKey = PlayerAvatar.handleKey
        PlayerAvatar.handleKey = new_PlayerHandleKey

        def new_LobbyView_populate(current):
            old_LobbyView_populate(current)
            if self.configMarker == None:
                SystemMessages.pushI18nMessage('<font color="#ff9933"><B>' + self.application + '</B></font><br><br><font color="#cc0000">        Config loading failure!</font>', type=SystemMessages.SM_TYPE.Warning)
            elif self.FlagTXT:
                SystemMessages.pushI18nMessage('<font color="#ff9933"><B>' + self.application + '</B></font><br><br><font color="#33cc00">     XML config successfully loaded.</font>', type=SystemMessages.SM_TYPE.Warning)
                self.FlagTXT = False
            return

        old_LobbyView_populate = LobbyView._populate
        LobbyView._populate = new_LobbyView_populate
        pre_vehicle_onEnterWorld = PlayerAvatar.vehicle_onEnterWorld
        PlayerAvatar.vehicle_onEnterWorld = new_vehicle_onEnterWorld
        pre_vehicle_onLeaveWorld = PlayerAvatar.vehicle_onLeaveWorld
        PlayerAvatar.vehicle_onLeaveWorld = new_vehicle_onLeaveWorld
        pre_showTracer = PlayerAvatar.showTracer
        PlayerAvatar.showTracer = new_showTracer


VM = MarkerReLoad()


init = lambda : None
fini = lambda : None
onAccountBecomePlayer = lambda : None
onAccountBecomeNonPlayer = lambda : None
onAvatarBecomePlayer = lambda : None
onAccountShowGUI = lambda ctx : None


import weakref
import GUI
from gui.Scaleform.Flash import Flash

class _VehicleMarkersManager(Flash):
    __FLASH_CLASS = 'Flash'
    __FLASH_PATH = 'objects/reload'
    __FLASH_ARGS = None

    def __init__(self):
        Flash.__init__(self, SWF_FILE_NAME, self.__FLASH_CLASS, self.__FLASH_ARGS, self.__FLASH_PATH)
        self.component.wg_inputKeyMode = 2
        self.component.drawWithRestrictedViewPort = False
        self.movie.backgroundAlpha = 0
        self.__parentUI = weakref.proxy(g_appLoader.getDefBattleApp())
        self.__parentUIcomp = self.__parentUI.component
        self.__ownUI = None
        return

    def start(self, flashID):
        self.active(True)
        self.__ownUI = GUI.WGVehicleMarkersCanvasFlash(self.movie)
        self.__ownUI.wg_inputKeyMode = 2
        self.__ownUIProxy = weakref.proxy(self.__ownUI)
        self.__parentUIcomp.addChild(self.__ownUI, flashID)

    def destroy_light(self, flashID):
        self.__parentUI = None
        self.__ownUI = None
        self.close()
        return

    def destroy(self, flashID):
        if self.__parentUIcomp is not None:
            if hasattr(self.__parentUIcomp, flashID):
                setattr(self.__parentUIcomp, flashID, None)
        self.__parentUI = None
        self.__ownUI = None
        self.close()
        return

    def createMarker(self, vProxy):
        mProv = vProxy.model.node('HP_gui')
        handle = self.__ownUI.addMarker(mProv, 'VehicleMarkerEnemy')
        self.invokeMarker(handle, 'init', [])
        return handle

    def showActionMarker(self, handle, newState = '', time_value = 0):
        self.invokeMarker(handle, 'showActionMarker', [newState, time_value])

    def invokeMarker(self, handle, function, args = None):
        if handle != -1:
            if args is None:
                args = []
            self.__ownUI.markerInvoke(handle, (function, args))
        return


