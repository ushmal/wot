import BigWorld
import Keys
import GUI
import constants
import ResMgr
from Avatar import PlayerAvatar
from Vehicle import Vehicle
from VehicleAppearance import VehicleAppearance, StippleManager, _VEHICLE_DISAPPEAR_TIME
from gui.app_loader import g_appLoader
from debug_utils import *
from functools import partial

g_active = True
g_key = Keys.KEY_NUMPAD5
g_delay = 20
g_xmlConfig = ResMgr.openSection('scripts/client/gui/mods/mod_shadow.xml')
if g_xmlConfig:
    g_delay = g_xmlConfig.readInt('delay', g_delay)
    if g_delay > 0:
        g_active = g_xmlConfig.readBool('active', True)
    else:
        g_active = False
    g_key = getattr(Keys, g_xmlConfig.readString('key', 'KEY_NUMPAD5'))
    LOG_DEBUG('config is loaded')

def new_handleKey(self, isDown, key, mods):
    global g_active
    if key == g_key and mods == 0 and isDown:
        if g_appLoader.getDefBattleApp() is not None:
            if g_active:
                g_appLoader.getDefBattleApp().call('battle.PlayerMessagesPanel.ShowMessage', ['0', 'Shadow OFF', 'red'])
                g_active = False
            else:
                g_appLoader.getDefBattleApp().call('battle.PlayerMessagesPanel.ShowMessage', ['0', 'Shadow ON', 'gold'])
                g_active = True
            self.soundNotifications.play('chat_shortcut_common_fx')
            return True
    return old_handleKey(self, isDown, key, mods)

old_handleKey = PlayerAvatar.handleKey
PlayerAvatar.handleKey = new_handleKey

g_shadows_list = []

def new_addStippleModel(self, vehID):
    global g_shadows_list
    model = self._StippleManager__stippleToAddDescs[vehID][0]
    if model.attached:
        callbackID = BigWorld.callback(0.0, partial(self._StippleManager__addStippleModel, vehID))
        self._StippleManager__stippleToAddDescs[vehID] = (model, callbackID)
        return
    del self._StippleManager__stippleToAddDescs[vehID]
    BigWorld.player().addModel(model)
    vehicle = BigWorld.player().arena.vehicles.get(vehID)
    if g_active and vehicle['isAlive'] and BigWorld.player().team != vehicle['team']:
        vehicleType = unicode(vehicle['vehicleType'].type.shortUserString, 'utf-8')
        TransBoundingBox = GUI.BoundingBox('objects/shadow/null.dds')
        TransBoundingBox.size = (0.05, 0.05)
        my_info = '\\cFF4949FF;' + vehicleType
        TransBoundingBox.my_string = GUI.Text(my_info)
        TransBoundingBox.my_string.colourFormatting = True
        TransBoundingBox.my_string.colour = (255, 0, 0, 255)
        TransBoundingBox.my_string.font = 'hpmp_panel.font'
        TransBoundingBox.my_string.horizontalPositionMode = TransBoundingBox.my_string.verticalPositionMode = 'CLIP'
        TransBoundingBox.my_string.widthMode = TransBoundingBox.my_string.heightMode = 'PIXEL'
        TransBoundingBox.my_string.verticalAnchor = 'CENTER'
        TransBoundingBox.my_string.horizontalAnchor = 'CENTER'
        TransBoundingBox.source = model.bounds
        TransBoundingBox.my_string.position = (0.5, 0.75, 0)
        GUI.addRoot(TransBoundingBox)
        LOG_DEBUG('add shadow: id=%d' % vehID)
        g_shadows_list.append({'time': BigWorld.time(), 'bb': TransBoundingBox, 'id': vehID})
        BigWorld.callback(g_delay, delBoundingBox)
        callbackID = BigWorld.callback(g_delay, partial(self._StippleManager__removeStippleModel, vehID))
    else:
        callbackID = BigWorld.callback(_VEHICLE_DISAPPEAR_TIME, partial(self._StippleManager__removeStippleModel, vehID))
    self._StippleManager__stippleDescs[vehID] = (model, callbackID)

def delBoundingBox():
    global g_shadows_list
    for value in g_shadows_list:
        if BigWorld.time() - value['time'] >= g_delay:
            LOG_DEBUG('timer: remove: id=%d' % value['id'])
            GUI.delRoot(value['bb'])
            g_shadows_list.remove(value)

VehicleAppearance = StippleManager._StippleManager__addStippleModel
StippleManager._StippleManager__addStippleModel = new_addStippleModel

'''
from gui.Scaleform.Battle import Battle

def onVehicleKilled(targetID, atackerID, *args):
    global g_shadows_list
    LOG_DEBUG('killed: id=%d' % targetID)
    for value in g_shadows_list:
        if value['id'] == targetID:
            LOG_DEBUG('killed: remove: id=%d' % value['id'])
            GUI.delRoot(value['bb'])
            g_shadows_list.remove(value)
            return

def new_startBattle(current):
    BigWorld.player().arena.onVehicleKilled += onVehicleKilled
    old_startBattle(current)

old_startBattle = Battle.afterCreate
Battle.afterCreate = new_startBattle

def new_stopBattle(current):
    BigWorld.player().arena.onVehicleKilled -= onVehicleKilled
    old_stopBattle(current)

old_stopBattle = Battle.beforeDelete
Battle.beforeDelete = new_stopBattle
'''
