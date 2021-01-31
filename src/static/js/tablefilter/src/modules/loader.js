import {Feature} from '../feature';
import {createElm, createText, elm, removeElm} from '../dom';
import {EMPTY_FN} from '../types';
import {root} from '../root';
import {NONE} from '../const';
import {defaultsStr, defaultsFn} from '../settings';

const BEFORE_ACTION_EVENTS = [
    'before-filtering',
    'before-populating-filter',
    'before-page-change',
    'before-clearing-filters',
    'before-page-length-change',
    'before-reset-page',
    'before-reset-page-length',
    'before-loading-extensions',
    'before-loading-themes'
];

const AFTER_ACTION_EVENTS = [
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
 * Activity indicator
 *
 * @export
 * @class Loader
 * @extends {Feature}
 */
export class Loader extends Feature {

    /**
     * Creates an instance of Loader.
     *
     * @param {TableFilter} tf TableFilter instance
     */
    constructor(tf) {
        super(tf, Loader);

        let f = this.config.loader || {};

        /**
         * ID of custom container element
         * @type {String}
         */
        this.targetId = defaultsStr(f.target_id, null);

        /**
         * Loader container DOM element
         * @type {DOMElement}
         */
        this.cont = null;

        /**
         * Text displayed when indicator is visible
         * @type {String}
         */
        this.text = defaultsStr(f.text, 'Loading...');

        /**
         * Custom HTML injected in Loader's container element
         * @type {String}
         */
        this.html = defaultsStr(f.html, null);

        /**
         * Css class for Loader's container element
         * @type {String}
         */
        this.cssClass = defaultsStr(f.css_class, 'loader');

        /**
         * Close delay in milliseconds
         * @type {Number}
         */
        this.closeDelay = 250;

        /**
         * Callback fired when loader is displayed
         * @type {Function}
         */
        this.onShow = defaultsFn(f.on_show_loader, EMPTY_FN);

        /**
         * Callback fired when loader is closed
         * @type {Function}
         */
        this.onHide = defaultsFn(f.on_hide_loader, EMPTY_FN);
    }

    /**
     * Initializes Loader instance
     */
    init() {
        if (this.initialized) {
            return;
        }

        let tf = this.tf;
        let emitter = this.emitter;

        let containerDiv = createElm('div');
        containerDiv.className = this.cssClass;

        let targetEl = !this.targetId ?
            tf.dom().parentNode : elm(this.targetId);
        if (!this.targetId) {
            targetEl.insertBefore(containerDiv, tf.dom());
        } else {
            targetEl.appendChild(containerDiv);
        }
        this.cont = containerDiv;
        if (!this.html) {
            this.cont.appendChild(createText(this.text));
        } else {
            this.cont.innerHTML = this.html;
        }

        this.show(NONE);

        // Subscribe to events
        emitter.on(BEFORE_ACTION_EVENTS, () => this.show(''));
        emitter.on(AFTER_ACTION_EVENTS, () => this.show(NONE));

        /** @inherited */
        this.initialized = true;
    }

    /**
     * Shows or hides activity indicator
     * @param {String} Two possible values: '' or 'none'
     */
    show(p) {
        if (!this.isEnabled()) {
            return;
        }

        function displayLoader() {
            if (!this.cont) {
                return;
            }
            if (p !== NONE) {
                this.onShow(this);
            }
            this.cont.style.display = p;
            if (p === NONE) {
                this.onHide(this);
            }
        };

        let t = p === NONE ? this.closeDelay : 1;
        root.setTimeout(displayLoader.bind(this), t);
    }

    /**
     * Removes feature
     */
    destroy() {
        if (!this.initialized) {
            return;
        }

        let emitter = this.emitter;

        removeElm(this.cont);
        this.cont = null;

        // Unsubscribe to events
        emitter.off(BEFORE_ACTION_EVENTS, () => this.show(''));
        emitter.off(AFTER_ACTION_EVENTS, () => this.show(NONE));

        this.initialized = false;
    }
}
