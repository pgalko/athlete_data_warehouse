(function(win, TableFilter){

    var tf = new TableFilter('demo', {
        base_path: '../dist/tablefilter/',
        auto_filter: {
            delay: 1000
        }
    });
    tf.init();
    window.tf = tf;

    module('Sanity checks');
    test('Auto filter feature', function() {
        deepEqual(tf instanceof TableFilter, true, 'TableFilter instanciated');
        deepEqual(tf.autoFilter, true, 'Auto filtering enabled');
        deepEqual(tf.autoFilterDelay, 1000, 'Expected filtering delay');
    });
    test('Blur input filter', function() {
        // setup
        var filter = tf.getFilterElement(0);
        filter.focus();

        // act
        filter.blur();

        // assert
        deepEqual(tf.isUserTyping, false, 'User not typing');
        deepEqual(tf.autoFilterTimer, null, 'Auto filter timer cleared');
    });

    module('Remove feature');
    test('Auto filter feature disabled', function() {
        tf.destroy();
        tf = new TableFilter('demo', {
            base_path: '../dist/tablefilter/',
            auto_filter: false
        });

        deepEqual(tf.autoFilter, false, 'Auto filtering disabled');
        deepEqual(tf.autoFilterDelay, 750, 'Expected filtering delay');
    });

})(window, TableFilter);
