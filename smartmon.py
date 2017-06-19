from pySMART import DeviceList
from checks import AgentCheck

class SmartMon(AgentCheck):

    """ This check is for monitoring S.M.A.R.T data from hard drives
        IMPORTANT: the smartctl binary must have setuid permissions to
        work from a non-privileged id. chmod +s /usr/sbin/smartctl
    """

    def check(self, instance):
        devlist = DeviceList()

        for dev in range(len(devlist.devices)):
            try:
                self.gauge("smartmon.Reallocated_Sector_Ct", devlist.devices[dev].diags['Reallocated_Sector_Ct'], device_name=devlist.devices[dev].name)
            except KeyError:
                pass
            try:
                self.gauge("smartmon.Power_On_Hours", devlist.devices[dev].diags['Power_On_Hours'], device_name=devlist.devices[dev].name)
            except KeyError:
                pass
            self.gauge("smartmon.Assessment", int(devlist.devices[dev].assessment == 'PASS'), device_name=devlist.devices[dev].name)
            for attribute in range(len(devlist.devices[dev].attributes)):
                if devlist.devices[dev].attributes[attribute] is not None:
                    check_namespace = "smartmon.%s" % (devlist.devices[dev].attributes[attribute].name,)
                    self.gauge(check_namespace, devlist.devices[dev].attributes[attribute].raw, device_name=devlist.devices[dev].name)
