'use strict';

/* Controllers */

var builderControllers = angular.module('builderControllers', []);

builderControllers.controller('DebBuildListCtrl', ['$scope', '$http', 'BuildConf',
    function ($scope, $http, BuildConf) {
        $scope.build_confs = BuildConf.query();
        $scope.orderProp = '-fields.status';
        $scope.alerts = [];

        $scope.closeAlert = function (index) {
            $scope.alerts.splice(index, 1);
        };

        $scope.rebuild_pkg = function (build_conf_id) {
            $http.get('/api/rebuild_package/' + build_conf_id).success(function (data) {
                $scope.alerts.push(data);
            });
        }

        $scope.autobuild_on_off = function (build_conf_id) {
            $http.get('/api/autobuild_on_off/' + build_conf_id).success(function (data) {
                for (var build_conf in $scope.build_confs) {
                    if ($scope.build_confs[build_conf].pk == build_conf_id) {
                        $scope.build_confs[build_conf].fields.auto_build = data[0].fields.auto_build;
                    }
                }
            });
        }

        $scope.remove_build_conf = function (build_conf_id) {
            var is_confirm = confirm('Are you sure remove build config #' + build_conf_id + '?');
            if (is_confirm) {
                $http.get('/api/remove_build_conf/' + build_conf_id).success(function (data) {
                    $scope.alerts.push(data);
                });
            }
        }

        $scope.getData = function () {
            $http.get('/api/build_confs/').success(function (data) {
                if ($scope.build_confs.length != data.length) {
                    $scope.build_confs = data;
                }
            });
        };
        setInterval($scope.getData, 1000);
    }]);


builderControllers.controller('BranchestListCtrl', ['$scope', '$http', 'Branch',
    function ($scope, $http, Branch) {
        $scope.branches = Branch.query();
        $scope.alerts = [];

        $scope.closeAlert = function (index) {
            $scope.alerts.splice(index, 1);
        };

        $scope.remove_branch = function (branch_id) {
            var is_confirm = confirm('Are you sure remove branch #' + branch_id + '?');
            if (is_confirm) {
                $http.get('/api/remove_branch/' + branch_id).success(function (data) {
                    $scope.alerts.push(data);
                });
            }
        }

        $scope.getData = function () {
            $http.get('/api/branches/').success(function (data) {
                if ($scope.branches.length != data.length) {
                    $scope.branches = data;
                }
            });
        };
        setInterval($scope.getData, 1000);
    }]);

builderControllers.controller('MappingCtrl', ['$scope', '$http', 'Mapping',
    function ($scope, $http, Mapping) {
        $scope.mappings = Mapping.query();
        $scope.alerts = [];

        $scope.closeAlert = function (index) {
            $scope.alerts.splice(index, 1);
        };

        $scope.remove_mapping = function (mapping_id) {
            var is_confirm = confirm('Are you sure remove mapping #' + mapping_id + '?');
            if (is_confirm) {
                $http.get('/api/remove_mapping/' + mapping_id).success(function (data) {
                    $scope.alerts.push(data);
                });
            }
        }

        $scope.getData = function () {
            $http.get('/api/mapping/').success(function (data) {
                if ($scope.mappings.length != data.length) {
                    $scope.mappings = data;
                }
            });
        };
        setInterval($scope.getData, 1000);
    }]);
