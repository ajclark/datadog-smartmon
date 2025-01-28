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
            self.gauge("smartmon.assessment", int(device.assessment == 'PASS'), tags=tags)

            if device.dev_interface == "nvme":
                nvme = device.if_attributes
                self.gauge(f"smartmon.available_spare", nvme.availableSpare ,tags=tags)
                self.gauge(f"smartmon.available_spare_threshold", nvme.availableSpareThreshold ,tags=tags)
                self.gauge(f"smartmon.bytes_read", nvme.bytesRead ,tags=tags)
                self.gauge(f"smartmon.bytes_written", nvme.bytesWritten ,tags=tags)
                self.gauge(f"smartmon.controller_busy_time", nvme.controllerBusyTime ,tags=tags)
                self.gauge(f"smartmon.critical_warning", nvme.criticalWarning ,tags=tags)
                self.gauge(f"smartmon.critical_temperature_time", nvme.criticalTemperatureTime ,tags=tags)
                self.gauge(f"smartmon.critical_warning", nvme.criticalWarning ,tags=tags)
                self.gauge(f"smartmon.data_units_read", nvme.dataUnitsRead ,tags=tags)
                self.gauge(f"smartmon.data_units_written", nvme.dataUnitsWritten ,tags=tags)
                self.gauge(f"smartmon.error_entries", nvme.errorEntries ,tags=tags)
                self.gauge(f"smartmon.errors", len(nvme.errors) ,tags=tags)
                self.gauge(f"smartmon.host_read_commands", nvme.hostReadCommands ,tags=tags)
                self.gauge(f"smartmon.host_write_commands", nvme.hostWriteCommands ,tags=tags)
                self.gauge(f"smartmon.integrity_errors", nvme.integrityErrors ,tags=tags)
                self.gauge(f"smartmon.percentage_used", nvme.percentageUsed ,tags=tags)
                self.gauge(f"smartmon.power_cycles", nvme.powerCycles ,tags=tags)
                self.gauge(f"smartmon.power_on_hours", nvme.powerOnHours ,tags=tags)
                self.gauge(f"smartmon.temperature", nvme.temperature ,tags=tags)
                self.gauge(f"smartmon.tests", len(nvme.tests) ,tags=tags)
                self.gauge(f"smartmon.unsafe_shutdowns", nvme.unsafeShutdowns ,tags=tags)
                self.gauge(f"smartmon.warning_temperature_time", nvme.warningTemperatureTime ,tags=tags)

            for attribute in range(len(device.attributes)):
                if device.attributes[attribute] is not None:
                    attr = device.attributes[attribute]
                    self.gauge(f"smartmon.{attr.name.lower()}", attr.raw.split()[0], tags=tags)
