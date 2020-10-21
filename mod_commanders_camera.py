from AvatarInputHandler.DynamicCameras.ArcadeCamera import ArcadeCamera, MinMax
from AvatarInputHandler.DynamicCameras.StrategicCamera import StrategicCamera

def hook_ArcadeCamera_readConfigs(self, dataSec):
    prev_ArcadeCamera_readConfigs(self, dataSec)
    distRange = MinMax(2, 150)
    self._userCfg['distRange'] = self._cfg['distRange'] = distRange

prev_ArcadeCamera_readConfigs = ArcadeCamera._readConfigs
ArcadeCamera._readConfigs = hook_ArcadeCamera_readConfigs

def hook_StrategicCamera_readConfigs(self, dataSec):
    prev_StrategicCamera_readConfigs(self, dataSec)
    self._userCfg['distRange'] = self._cfg['distRange'] = (40, 200)

prev_StrategicCamera_readConfigs = StrategicCamera._readConfigs
StrategicCamera._readConfigs = hook_StrategicCamera_readConfigs
