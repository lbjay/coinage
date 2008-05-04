var CollectorInit = function() {

    // redirect console.log for non-firebug browsers
    if (typeof console == 'undefined')
        window.console = { log: function() {}, trace: function() {} };

    return {
        init: function() {
            document.write('<script type="text/javascript" src="' + COINAGE_BASEURL + '/media/js/jquery.js"></script>');
            document.write('<script type="text/javascript" src="' + COINAGE_BASEURL + '/media/js/collector_engine.js"></script>');
        },
        siteId: function() {
            return _site;
        },
        baseUrl: function() {
            return _baseUrl;
        }
    };
}();

CollectorInit.init();

