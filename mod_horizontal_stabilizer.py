from AvatarInputHandler.AimingSystems.SniperAimingSystem import SniperAimingSystem

def hook_enableHorizontalStabilizerRuntime(self, enable):
    prev_enableHorizontalStabilizerRuntime(self, True)

prev_enableHorizontalStabilizerRuntime = SniperAimingSystem.enableHorizontalStabilizerRuntime
SniperAimingSystem.enableHorizontalStabilizerRuntime = hook_enableHorizontalStabilizerRuntime

print 'Mod "%s" loaded' % __file__
