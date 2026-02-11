define(['app', 'ace', 'ace-language-tools'], function(app) {
    app.component('tailscaleStatus', {
        templateUrl: 'app/tailscale/tailscaleStatus.html',
        controller: tailscaleStatusController
    })

    function tailscaleStatusController($scope, $element, bootbox, tailscale) {
        var $ctrl = this;
        var aceEditor;

        $ctrl.isModified = false;
        $ctrl.$onInit = function() {
            fetchStatus();
        }

        function fetchStatus() {
            return tailscale.sendRequest('getstatus').then(function(status) {
                $ctrl.status = status;
                
                var element = $element.find('.js-script-content')[0];
                aceEditor = ace.edit(element);

                aceEditor.setOptions({
                    enableBasicAutocompletion: true,
                    enableSnippets: true,
                    enableLiveAutocompletion: true
                });

                ace.config.setModuleUrl("ace/mode/json", "/templates/tailscale/ace_json_mode.js");
                ace.config.setModuleUrl("ace/mode/json_worker", "/templates/tailscale/ace_worker_json.js");
                aceEditor.setTheme('ace/theme/xcode');
                aceEditor.setValue(JSON.stringify(status, null, '\t'));
                aceEditor.getSession().setMode('ace/mode/json');
                aceEditor.gotoLine(1);
                aceEditor.scrollToLine(1, true, true);
            }).catch(function() {
                bootbox.alert('Failed to load Status');
            })
        }
    }
});