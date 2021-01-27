from AvatarInputHandler.DynamicCameras.SniperCamera import SniperCamera

def hook_SniperCamera_enable(self, targetPos, saveZoom):
    prev_SniperCamera_enable(self, targetPos, False)

prev_SniperCamera_enable = SniperCamera.enable
SniperCamera.enable = hook_SniperCamera_enable
