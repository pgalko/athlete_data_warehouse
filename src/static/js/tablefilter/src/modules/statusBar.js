import {Feature} from '../feature';
import {root} from '../root';
import {createElm, createText, elm, removeElm} from '../dom';
import {EMPTY_FN, isNull} from '../types';
import {defaultsStr, defaultsFn} from '../settings';
import {LEFT} from './toolbar';

const EVENTS = [
    'after-filtering',
    'after-populating-filter',
    'after-page-change',
    'after-clearing-filters',
    'after-page-length-change',
    'after-reset-page',
    'after-reset-page-length',
    'after-loading-extensions',
    'after-loading-themes'
];

/**
 * Status bar UI component
 * @export
 * @class StatusBar
 * @extends {Feature}
 */
export class StatusBar extends Feature {

    /**
     * Creates an instance of StatusBar
     * @param {TableFilter} tf TableFilter instance
     */
    constructor(tf) {
        super(tf, StatusBar);

        // Configuration object
        let f = this.config.status_bar || {};

        /**
         * ID of custom container element
         * @type {String}
         */
        this.targetId = defaultsStr(f.target_id, null);

        /**
         * Container DOM element
         * @type {DOMElement}
         * @private
         */
        this.container = null;

        /**
         * Message container DOM element
         * @type {DOMElement}
         * @private
         */
        this.msgContainer = null;

        /**
         * Label container DOM element
         * @type {DOMElement}
         * @private
         */
        this.labelContainer = null;

        /**
         * Text preceding status message
         * @type {String}
         */
        this.text = defaultsStr(f.text, '');

        /**
         * Css class for container element
         * @type {String}
         */
        this.cssClass = defaultsStr(f.css_class, 'status');

        /**
         * Message visibility duration in milliseconds
         * @type {Number}
         * @private
         */
        this.delay = 250;

        /**
         * Callback fired before the message is displayed
         * @type {Function}
         */
        this.onBeforeShowMsg = defaultsFn(f.on_before_show_msg, EMPTY_FN);

        /**
         * Callback fired after the message is displayed
         * @type {Function}
         */
        this.onAfterShowMsg = defaultsFn(f.on_after_show_msg, EMPTY_FN);

        /**
         * Message appearing upon filtering
         * @type {String}
         */
        this.msgFilter = defaultsStr(f.msg_filter, 'Filtering data...');

        /**
         * Message appearing when a drop-down filter is populated
         * @type {String}
         */
        this.msgPopulate = defaultsStr(f.msg_populate, 'Populating filter...');

        /**
         * Message appearing when a checklist filter is populated
         * @type {String}
         */
        this.msgPopulateCheckList = defaultsStr(f.msg_populate_checklist,
            'Populating list...');

        /**
         * Message appearing when a pagination page is changed
         * @type {String}
         */
        this.msgChangePage = defaultsStr(f.msg_change_page,
            'Collecting paging data...');

        /**
         * Message appearing when filters are cleared
         * @type {String}
         */
        this.msgClear = defaultsStr(f.msg_clear, 'Clearing filters...');

        /**
         * Message appearing when the page length is changed
         * @type {String}
         */
        this.msgChangeResults = defaultsStr(f.msg_change_results,
            'Changing results per page...');

        /**
         * Message appearing when the page is re-set
         * @type {String}
         */
        this.msgResetPage = defaultsStr(f.msg_reset_page, 'Re-setting page...');

        /**
         * Message appearing when the page length is re-set
         * @type {String}
         */
        this.msgResetPageLength = defaultsStr(f.msg_reset_page_length,
            'Re-setting page length...');

        /**
         * Message appearing upon column sorting
         * @type {String}
         */
        this.msgSort = defaultsStr(f.msg_sort, 'Sorting data...');

        /**
         * Message appearing when extensions are loading
         * @type {String}
         */
        this.msgLoadExtensions = defaultsStr(f.msg_load_extensions,
            'Loading extensions...');

        /**
         * Message appearing when themes are loading
         * @type {String}
         */
        this.msgLoadThemes = defaultsStr(f.msg_load_themes,
            'Loading theme(s)...');

        /**
         * Default position in toolbar ('left'|'center'|'right')
         * @type {String}
         */
        this.toolbarPosition = defaultsStr(f.toolbar_position, LEFT);
    }

    /**
     * Initializes StatusBar instance
     */
    init() {
        if (this.initialized) {
            return;
        }

        let tf = this.tf;
        let emitter = this.emitter;

        emitter.emit('initializing-feature', this, !isNull(this.targetId));

        // status bar container
        let statusDiv = createElm('div');
        statusDiv.className = this.cssClass;

        // status bar label
        let statusSpan = createElm('span');
        // preceding text
        let statusSpanText = createElm('span');
        statusSpanText.appendChild(createText(this.text));

        // target element container
        let targetEl = (!this.targetId) ?
            tf.feature('toolbar').container(this.toolbarPosition) :
            elm(this.targetId);

        // default container
        if (!this.targetId) {
            statusDiv.appendChild(statusSpanText);
            statusDiv.appendChild(statusSpan);
            targetEl.appendChild(statusDiv);
        } else {
            // custom container, no need to append statusDiv
            targetEl.appendChild(statusSpanText);
            targetEl.appendChild(statusSpan);
        }

        this.container = statusDiv;
        this.msgContainer = statusSpan;
        this.labelContainer = statusSpanText;

        // subscribe to events
        emitter.on(['before-filtering'], () => this.message(this.msgFilter));
        emitter.on(['before-populating-filter'],
            () => this.message(this.msgPopulate));
        emitter.on(['before-page-change'],
            () => this.message(this.msgChangePage));
        emitter.on(['before-clearing-filters'], () =>
            this.message(this.msgClear));
        emitter.on(['before-page-length-change'],
            () => this.message(this.msgChangeResults));
        emitter.on(['before-reset-page'],
            () => this.message(this.msgResetPage));
        emitter.on(['before-reset-page-length'],
            () => this.message(this.msgResetPageLength));
        emitter.on(['before-loading-extensions'],
            () => this.message(this.msgLoadExtensions));
        emitter.on(['before-loading-themes'],
            () => this.message(this.msgLoadThemes));

        emitter.on(EVENTS, () => this.message(''));

        /** @inherited */
        this.initialized = true;

        emitter.emit('feature-initialized', this);
    }

    /**
     * Display status message
     * @param {String} [t=''] Message to be displayed
     */
    message(t = '') {
        if (!this.isEnabled()) {
            return;
        }

        this.onBeforeShowMsg(this.tf, t);

        let d = t === '' ? this.delay : 1;
        root.setTimeout(() => {
            if (!this.initialized) {
                return;
            }
            this.msgContainer.innerHTML = t;

            this.onAfterShowMsg(this.tf, t);
        }, d);
    }

    /**
     * Destroy StatusBar instance
     */
    destroy() {
        if (!this.initialized) {
            return;
        }

        let emitter = this.emitter;

        this.container.innerHTML = '';
        if (!this.targetId) {
            removeElm(this.container);
        }
        this.labelContainer = null;
        this.msgContainer = null;
        this.container = null;

        // Unsubscribe to events
        emitter.off(['before-filtering'], () => this.message(this.msgFilter));
        emitter.off(['before-populating-filter'],
            () => this.message(this.msgPopulate));
        emitter.off(['before-page-change'],
            () => this.message(this.msgChangePage));
        emitter.off(['before-clearing-filters'],
            () => this.message(this.msgClear));
        emitter.off(['before-page-length-change'],
            () => this.message(this.msgChangeResults));
        emitter.off(['before-reset-page'], () =>
            this.message(this.msgResetPage));
        emitter.off(['before-reset-page-length'],
            () => this.message(this.msgResetPageLength));
        emitter.off(['before-loading-extensions'],
            () => this.message(this.msgLoadExtensions));
        emitter.off(['before-loading-themes'],
            () => this.message(this.msgLoadThemes));

        emitter.off(EVENTS, () => this.message(''));

        this.initialized = false;
    }
}
