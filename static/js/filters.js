angular.module('builderFilters', []).
    filter('status_display',function () {
        return function (status_id) {
            var name;
            switch (status_id) {
                case 0:
                    name = "None";
                    break
                case 1:
                    name = "Success";
                    break
                case 2:
                    name = "In progress";
                    break
                case 3:
                    name = "Pending";
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
            var css_style;
            switch (status_id) {
                case 0:
                    css_style = "default";
                    break
                case 1:
                    css_style = "success";
                    break
                case 2:
                    css_style = "info";
                    break
                case 3:
                    css_style = "default";
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
    filter('play_pause',function () {
        return function (on_off) {
            return on_off ? 'pause' : 'play';
        }
    }).
    filter('play_pause_tr', function () {
        return function (on_off) {
            return on_off ? 'danger' : '';
        }
    })
    .filter("timeago", function () {
        //time: the time
        //local: compared to what time? default: now
        //raw: wheter you want in a format of "5 minutes ago", or "5 minutes"
        return function (time, local, raw) {
            if (!time) return "never";

            if (!local) {
                (local = Date.now())
            }

            if (angular.isDate(time)) {
                time = time.getTime();
            } else if (typeof time === "string") {
                time = new Date(time).getTime();
            }

            if (angular.isDate(local)) {
                local = local.getTime();
            } else if (typeof local === "string") {
                local = new Date(local).getTime();
            }

            if (typeof time !== 'number' || typeof local !== 'number') {
                return;
            }

            var
                offset = Math.abs((local - time) / 1000),
                span = [],
                MINUTE = 60,
                HOUR = 3600,
                DAY = 86400,
                WEEK = 604800,
                MONTH = 2629744,
                YEAR = 31556926,
                DECADE = 315569260;

            if (offset <= MINUTE)              span = [ '', raw ? 'now' : 'less than a minute' ];
            else if (offset < (MINUTE * 60))   span = [ Math.round(Math.abs(offset / MINUTE)), 'min' ];
            else if (offset < (HOUR * 24))     span = [ Math.round(Math.abs(offset / HOUR)), 'hr' ];
            else if (offset < (DAY * 7))       span = [ Math.round(Math.abs(offset / DAY)), 'day' ];
            else if (offset < (WEEK * 52))     span = [ Math.round(Math.abs(offset / WEEK)), 'week' ];
            else if (offset < (YEAR * 10))     span = [ Math.round(Math.abs(offset / YEAR)), 'year' ];
            else if (offset < (DECADE * 100))  span = [ Math.round(Math.abs(offset / DECADE)), 'decade' ];
            else                               span = [ '', 'a long time' ];

            span[1] += (span[0] === 0 || span[0] > 1) ? 's' : '';
            span = span.join(' ');

            if (raw === true) {
                return span;
            }
            return (time <= local) ? span + ' ago' : 'in ' + span;
        }
    });