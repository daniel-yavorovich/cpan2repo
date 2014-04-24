angular.module('builderFilters', []).
    filter('status_display',function () {
        return function (status_id) {
            var name;
            var css_style;
            switch (status_id) {
                case 0:
                    name = "None";
                    break
                case 1:
                    name = "Pending";
                    break
                case 2:
                    name = "In progress";
                    break
                case 3:
                    name = "Success";
                    break;
                case 4:
                    name = "Error";
                    break
                default:
                    name = "None";
                    break
            }
            return name;
        };
    }).
    filter('status_label_type',function () {
        return function (status_id) {
            var name;
            var css_style;
            switch (status_id) {
                case 0:
                    css_style = "default";
                    break
                case 1:
                    css_style = "default";
                    break
                case 2:
                    css_style = "info";
                    break
                case 3:
                    css_style = "success";
                    break;
                case 4:
                    css_style = "danger";
                    break
                default:
                    css_style = "default";
                    break
            }
            return css_style;
        };
    }).
    filter('play_pause', function () {
        return function (on_off) {
            return on_off ? 'pause' : 'play';
        }
    }).
    filter('play_pause_tr', function () {
        return function (on_off) {
            return on_off ? 'danger' : '';
        }
    });