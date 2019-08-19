from AvatarInputHandler.DynamicCameras.ArcadeCamera import ArcadeCamera, MinMax
from AvatarInputHandler.DynamicCameras.StrategicCamera import StrategicCamera

def hook_ArcadeCamera_readCfg(self, dataSec):
    prev_ArcadeCamera_readCfg(self, dataSec)
    distRange = MinMax(2, 125)
    self._ArcadeCamera__userCfg['distRange'] = self._ArcadeCamera__cfg['distRange'] = distRange

prev_ArcadeCamera_readCfg = ArcadeCamera._ArcadeCamera__readCfg
ArcadeCamera._ArcadeCamera__readCfg = hook_ArcadeCamera_readCfg

def hook_StrategicCamera_readCfg(self, dataSec):
    prev_StrategicCamera_readCfg(self, dataSec)
    self._StrategicCamera__userCfg['distRange'] = self._StrategicCamera__cfg['distRange'] = (40, 150)

prev_StrategicCamera_readCfg = StrategicCamera._StrategicCamera__readCfg
StrategicCamera._StrategicCamera__readCfg = hook_StrategicCamera_readCfg

print 'Mod "%s" loaded' % __file__
