'use strict';

/* Controllers */

var builderControllers = angular.module('builderControllers', []);

builderControllers.controller('DebBuildListCtrl', ['$scope', '$http',
    function ($scope, $http) {
        $http.get('/api/build_confs/').success(function (data) {
            $scope.build_confs = data;
        });

        $scope.orderProp = 'pk';
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
                        $scope.build_confs[build_conf].auto_build = data.autobuild_status;
                    }
                }
            });
        }

        $scope.global_autobuild_on = function () {
            $http.get('/api/global_autobuild_on/').success(function (data) {
                for (var build_conf in $scope.build_confs) {
                    $scope.build_confs[build_conf].auto_build = true;
                }
            });
        }

        $scope.global_autobuild_off = function () {
            $http.get('/api/global_autobuild_off/').success(function (data) {
                for (var build_conf in $scope.build_confs) {
                    $scope.build_confs[build_conf].auto_build = false;
                }
            });
        }

        $scope.remove_build_conf = function (build_conf_id) {
            var is_confirm = confirm('Are you sure remove build config #' + build_conf_id + '?');
            if (is_confirm) {
                for (var build_conf in $scope.build_confs) {
                    if ($scope.build_confs[build_conf].pk == build_conf_id) {
                        $scope.build_confs[build_conf].status = 3;
                    }
                }
                $http.get('/api/remove_build_conf/' + build_conf_id).success(function (data) {
                    $scope.alerts.push(data);
                });
            }
        }

        $scope.getData = function () {
            $http.get('/api/build_confs/').success(function (data) {
                $scope.build_confs = data;
            });
        };
        setInterval($scope.getData, 5000);
    }]);


builderControllers.controller('BranchestListCtrl', ['$scope', '$http',
    function ($scope, $http) {
        $http.get('/api/branches/').success(function (data) {
            if ($scope.branches != data) {
                $scope.branches = data;
            }
        });

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
                $scope.branches = data;
            });
        };
        setInterval($scope.getData, 5000);
    }]);

builderControllers.controller('MappingCtrl', ['$scope', '$http',
    function ($scope, $http) {
        $http.get('/api/mapping/').success(function (data) {
            if ($scope.mappings != data) {
                $scope.mappings = data;
            }
        });
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
                $scope.mappings = data;
            });
        };
        setInterval($scope.getData, 5000);
    }]);
