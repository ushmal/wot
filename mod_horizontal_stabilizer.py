from AvatarInputHandler.AimingSystems.SniperAimingSystem import SniperAimingSystem

def new_enableHorizontalStabilizerRuntime(self, enable):
    old_enableHorizontalStabilizerRuntime(self, True)

old_enableHorizontalStabilizerRuntime = SniperAimingSystem.enableHorizontalStabilizerRuntime
SniperAimingSystem.enableHorizontalStabilizerRuntime = new_enableHorizontalStabilizerRuntime

print 'Mod "%s" loaded' % __file__
