from pySMART import DeviceList
from checks import AgentCheck

class SmartMon(AgentCheck):

    """ This check is for monitoring S.M.A.R.T data from hard drives
        IMPORTANT: the smartctl binary must have setuid permissions to
        work from a non-privileged id. chmod +s /usr/sbin/smartctl
    """

    def check(self, instance):
        devlist = DeviceList()
        labels = instance.get("labels")

        for dev in range(len(devlist.devices)):
            device = devlist.devices[dev]
            tags = [f"device:/dev/{device.name}",
                    f"capacity:{device.capacity}",
                    f"interface:{device.interface}",
                    f"serial:{device.serial}",
                    f"model:{device.model}",
                    f"is_ssd:{device.is_ssd}",]

            if labels is not None and device.name in labels:
                tags.append(f"label:{labels[device.name]}")

            # overall pass/fail check
            self.gauge("smartmon.Assessment", int(device.assessment == 'PASS'), tags=tags)

            for attribute in range(len(device.attributes)):
                if device.attributes[attribute] is not None:
                    attr = device.attributes[attribute]
                    self.gauge(f"smartmon.{attr.name.lower()}", attr.raw, tags=tags)
