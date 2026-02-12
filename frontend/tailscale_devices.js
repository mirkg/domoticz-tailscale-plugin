define(['app', 'app/devices/Devices.js'], function(app) {

    app.component('tailscaleDevices', {
        bindings: {
            tailscaleDevices: '<',
            domoticzDevices: '<',
            onUpdate: '&',
            onUpdateDomoticzDevice: '&',
        },
        templateUrl: 'app/tailscale/devices.html',
        controller: tailscaleDevicesController
    });

    app.component('tailscaleDevicesTable', {
        bindings: {
            devices: '<',
            onSelect: '&',
            onUpdate: '&'
        },
        template: '<table id="tailscale-devices" class="display" width="100%"></table>',
        controller: tailscaleDevicesTableController,
    });

    function tailscaleDevicesController($scope, $uibModal, tailscale) {
        var $ctrl = this;

        $ctrl.selecttailscaleDevice = selecttailscaleDevice;

        $ctrl.$onInit = function() {
            $ctrl.associatedDevices = []
        };

        $ctrl.$onChanges = function(changes) {
            if (changes.domoticzDevices) {
                $ctrl.selecttailscaleDevice($ctrl.selectedtailscaleDevice)
            }
        };

        function selecttailscaleDevice(tailscaleDevice) {
            $ctrl.selectedtailscaleDevice = tailscaleDevice;

            if (!tailscaleDevice) {
                $ctrl.associatedDevices = []
            } else {
                $ctrl.associatedDevices = $ctrl.domoticzDevices.filter(function(device) {
                    return device.ID.indexOf(tailscaleDevice.ieee_address) === 0;
                });
            }
        }
    }

    function tailscaleDevicesTableController($element, $scope, $timeout, $uibModal, tailscale, bootbox, dzSettings, dataTableDefaultSettings) {
        var $ctrl = this;
        var table;

        $ctrl.$onInit = function() {
            table = $element.find('table').dataTable(Object.assign({}, dataTableDefaultSettings, {
                order: [[0, 'asc']],
                columns: [
                    { title: 'ID', data: 'ID' },
                    { title: 'HostName', width: '150px', data: 'HostName' },
                    { title: 'DNSName', data: 'DNSName' },
                    { title: 'OS', data: 'OS' },
                    { title: 'TailscaleIPs', data: 'TailscaleIPs', render: jsonRenderer },
                    { title: 'LastSeen', data: 'LastSeen' },
                    { title: 'Online', data: 'Online' },
                ],
            }));

            table.on('select.dt', function(event, row) {
                $ctrl.onSelect({ device: row.data() });
                $scope.$apply();
            });

            table.on('deselect.dt', function() {
                //Timeout to prevent flickering when we select another item in the table
                $timeout(function() {
                    if (table.api().rows({ selected: true }).count() > 0) {
                        return;
                    }

                    $ctrl.onSelect({ device: null });
                });

                $scope.$apply();
            });

            render($ctrl.devices);
        };

        $ctrl.$onChanges = function(changes) {
            if (changes.devices) {
                render($ctrl.devices);
            }
        };

        function render(items) {
            if (!table || !items) {
                return;
            }

            table.api().clear();
            table.api().rows
                .add(items)
                .draw();
        }

        function jsonRenderer(data, type, row) {
            return JSON.stringify(data);
        }
    }
});