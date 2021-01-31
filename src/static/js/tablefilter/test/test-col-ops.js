
var id = function (id){ return document.getElementById(id); };
var table = id('demo');
var totRowIndex = table.getElementsByTagName('tr').length;

var tf = new TableFilter('demo', {
    base_path: '../dist/tablefilter/',
    rows_always_visible: [
        totRowIndex-6,
        totRowIndex-5,
        totRowIndex-4,
        totRowIndex-3,
        totRowIndex-2,
        totRowIndex-1,
        totRowIndex,
    ],
    extensions: [{
        name: 'colOps',
        id: [
            'sum1', 'sum2',
            'mean1', 'mean2',
            'min1', 'min2',
            'max1', 'max2',
            'median1', 'median2',
            'q1-1', 'q1-2',
            'q3-1', 'q3-2'
        ],
        col: [
            2, 3,
            2, 3,
            2, 3,
            2, 3,
            2, 3,
            2, 3,
            2, 3
        ],
        operation: [
            'sum', 'sum',
            'mean', 'mean',
            'min', 'min',
            'max', 'max',
            'median', 'median',
            'q1', 'q1',
            'q3', 'q3'
        ],
        write_method: [
            'innerhtml', 'innerhtml',
            'innerhtml', 'innerhtml',
            'innerhtml', 'innerhtml',
            'innerhtml', 'innerhtml',
            'innerhtml', 'innerhtml',
            'innerhtml', 'innerhtml',
            'innerhtml', 'innerhtml'
        ],
        exclude_row: [
            totRowIndex-6,
            totRowIndex-5,
            totRowIndex-4,
            totRowIndex-3,
            totRowIndex-2,
            totRowIndex-1,
            totRowIndex
        ],
        decimal_precision: [
            0, 2,
            0, 2,
            0, 2,
            0, 2,
            0, 2,
            0, 2,
            0, 2
        ],
        tot_row_index: [
            totRowIndex-6, totRowIndex-6,
            totRowIndex-5, totRowIndex-5,
            totRowIndex-4, totRowIndex-4,
            totRowIndex-3, totRowIndex-3,
            totRowIndex-2, totRowIndex-2,
            totRowIndex-1, totRowIndex-1,
            totRowIndex, totRowIndex
        ]
    }]
});
tf.init();

module('Sanity checks');
test('Column operations', function() {
    var colOps = tf.extension('colOps');
    deepEqual(typeof colOps, 'object', 'ColOps instanciated');
    equal(id('sum1').innerHTML, 9911, 'Sum result');
    equal(id('sum2').innerHTML, 11.85, 'Sum result');
    equal(id('mean1').innerHTML, 1416, 'Mean result');
    equal(id('mean2').innerHTML, 1.69, 'Mean result');
    equal(id('min1').innerHTML, 286, 'Min result');
    equal(id('min2').innerHTML, 0.60, 'Min result');
    equal(id('max1').innerHTML, 2781, 'Max result');
    equal(id('max2').innerHTML, 3.10, 'Max result');
    equal(id('median1').innerHTML, 1412, 'Median result');
    equal(id('median2').innerHTML, 1.50, 'Median result');
    equal(id('q1-1').innerHTML, 872, 'Q1 result');
    equal(id('q1-2').innerHTML, 1.10, 'Q1 result');
    equal(id('q3-1').innerHTML, 2045, 'Q3 result');
    equal(id('q3-2').innerHTML, 2.15, 'Q3 result');
    tf.clearFilters();
});

module('Behaviour checks');
test('Column operations after filtering', function() {
    tf.setFilterValue(0, 'syd');
    tf.filter();
    equal(id('sum1').innerHTML, 3552, 'Sum result');
    equal(id('sum2').innerHTML, 4.60, 'Sum result');
    equal(id('mean1').innerHTML, 888, 'Mean result');
    equal(id('mean2').innerHTML, 1.15, 'Mean result');
    equal(id('min1').innerHTML, 286, 'Min result');
    equal(id('min2').innerHTML, 0.60, 'Min result');
    equal(id('max1').innerHTML, 1412, 'Max result');
    equal(id('max2').innerHTML, 1.50, 'Max result');
    equal(id('median1').innerHTML, 927, 'Median result');
    equal(id('median2').innerHTML, 1.25, 'Median result');
    equal(id('q1-1').innerHTML, 579, 'Q1 result');
    equal(id('q1-2').innerHTML, 0.85, 'Q1 result');
    equal(id('q3-1').innerHTML, 1197, 'Q3 result');
    equal(id('q3-2').innerHTML, 1.45, 'Q3 result');
    tf.clearFilters();
});

test('Can make column calculations', function() {
    // setup
    var colOps = tf.extension('colOps');

    // act
    var result0 = colOps.columnCalc(2, 'mean', 1);
    var result1 = colOps.columnCalc(2, 'min', 2);
    var result2 = colOps.columnCalc(2, 'max', 0);

    // assert
    deepEqual(result0, 1415.9, 'columnCalc mean');
    deepEqual(result1, 286.00, 'columnCalc min');
    deepEqual(result2, 2781, 'columnCalc max');
});

test('Can make column calculations with formated results', function() {
    // setup
    var colOps = tf.extension('colOps');
    colOps.formatResults[2] = { suffix: ' Km' };
    colOps.formatResults[4] = { suffix: ' Km' };
    colOps.formatResults[6] = { suffix: ' Km' };
    tf.colTypes[2] = { type: 'formatted-number', decimal: '.', thousands: ',' };

    // act
    colOps.calcAll();

    // assert
    deepEqual(id('mean1').innerHTML, '1,416 Km', 'Formatted mean result');
    deepEqual(id('min1').innerHTML, '286 Km', 'Formatted min result');
    deepEqual(id('max1').innerHTML, '2,781 Km', 'Formatted max result');

    colOps.formatResults[2] = undefined;
    colOps.formatResults[4] = undefined;
    colOps.formatResults[6] = undefined;
    tf.colTypes[2] = undefined;
});

test('Can configure result format', function() {
    // setup
    var colOps = tf.extension('colOps');
    var format = { prefix: '$', suffix: '/item' };

    // act
    var format = colOps.configureFormat(2, format);

    // assert
    deepEqual(format.prefix, '$', 'prefix');
    deepEqual(format.suffix, '/item', 'suffix');
    deepEqual(format.decimal, '', 'decimal separator');
    deepEqual(format.integerSeparator, '', 'thousands separator');
});

test('Can configure result format for formatted number column', function() {
    // setup
    var colOps = tf.extension('colOps');
    var format = { prefix: '$', suffix: '/item' };
    tf.colTypes = [null, null, null, null, null];
    tf.colTypes[3] = { type: 'formatted-number', decimal: ',', thousands: '.' };

    // act
    var format = colOps.configureFormat(3, format);

    // assert
    deepEqual(format.prefix, '$', 'prefix');
    deepEqual(format.suffix, '/item', 'suffix');
    deepEqual(format.decimal, ',', 'decimal separator');
    deepEqual(format.integerSeparator, '.', 'thousands separator');
    tf.colTypes[3] = undefined;
});

module('Tear-down');
test('can destroy', function() {
    tf.destroy();
    deepEqual(tf.isInitialized(), false, 'Filters removed');
});
