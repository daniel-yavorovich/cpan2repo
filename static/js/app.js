'use strict';

/* App Module */

var builderApp = angular.module('builerApp', [
    'ngRoute',
    'builderControllers',
    'builderServices',
    'builderFilters',
]);

builderApp.config(['$routeProvider',
    function ($routeProvider) {
        $routeProvider.
            when('/deb-build', {
                templateUrl: '/static/partials/deb-build.html',
                controller: 'DebBuildListCtrl'
            }).
            when('/branches', {
                templateUrl: '/static/partials/branches.html',
                controller: 'BranchestListCtrl'
            }).
            when('/mapping', {
                templateUrl: '/static/partials/mapping.html',
                controller: 'MappingCtrl'
            }).
            otherwise({
                redirectTo: '/deb-build'
            });
    }]);