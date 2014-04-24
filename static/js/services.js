'use strict';

/* Services */

var builderServices = angular.module('builderServices', ['ngResource']);


builderServices.factory('BuildConf', ['$resource',
    function ($resource) {
        return $resource('/api/build_confs/', {}, {
            query: {method: 'GET', isArray: true}
        });
    }]);

builderServices.factory('Branch', ['$resource',
    function ($resource) {
        return $resource('/api/branches/', {}, {
            query: {method: 'GET', isArray: true}
        });
    }]);

builderServices.factory('Mapping', ['$resource',
    function ($resource) {
        return $resource('/api/mapping/', {}, {
            query: {method: 'GET', isArray: true}
        });
    }]);