import {Feature} from '../feature';
import {createElm, elm, removeElm} from '../dom';
import {isEmpty, EMPTY_FN} from '../types';
import {NONE} from '../const';
import {defaultsStr, defaultsFn} from '../settings';

/**
 * UI when filtering yields no matches
 * @export
 * @class NoResults
 * @extends {Feature}
 */
export class NoResults extends Feature {

    /**
     * Creates an instance of NoResults
     * @param {TableFilter} tf TableFilter instance
     */
    constructor(tf) {
        super(tf, NoResults);

        //configuration object
        let f = this.config.no_results_message || {};

        /**
         * Text (accepts HTML)
         * @type {String}
         */
        this.content = defaultsStr(f.content, 'No results');

        /**
         * Custom container DOM element
         * @type {DOMElement}
         */
        this.customContainer = defaultsStr(f.custom_container, null);

        /**
         * ID of custom container element
         * @type {String}
         */
        this.customContainerId = defaultsStr(f.custom_container_id, null);

        /**
         * Indicates if UI is contained in a external element
         * @type {Boolean}
         * @private
         */
        this.isExternal = !isEmpty(this.customContainer) ||
            !isEmpty(this.customContainerId);

        /**
         * Css class assigned to container element
         * @type {String}
         */
        this.cssClass = defaultsStr(f.css_class, 'no-results');

        /**
         * Stores container DOM element
         * @type {DOMElement}
         */
        this.cont = null;

        /**
         * Callback fired before the message is displayed
         * @type {Function}
         */
        this.onBeforeShow = defaultsFn(f.on_before_show_msg, EMPTY_FN);

        /**
         * Callback fired after the message is displayed
         * @type {Function}
         */
        this.onAfterShow = defaultsFn(f.on_after_show_msg, EMPTY_FN);

        /**
         * Callback fired before the message is hidden
         * @type {Function}
         */
        this.onBeforeHide = defaultsFn(f.on_before_hide_msg, EMPTY_FN);

        /**
         * Callback fired after the message is hidden
         * @type {Function}
         */
        this.onAfterHide = defaultsFn(f.on_after_hide_msg, EMPTY_FN);
    }

    /**
     * Initializes NoResults instance
     */
    init() {
        if (this.initialized) {
            return;
        }
        let tf = this.tf;
        let target = this.customContainer || elm(this.customContainerId) ||
            tf.dom();

        //container
        let cont = createElm('div');
        cont.className = this.cssClass;
        cont.innerHTML = this.content;

        if (this.isExternal) {
            target.appendChild(cont);
        } else {
            target.parentNode.insertBefore(cont, target.nextSibling);
        }

        this.cont = cont;

        // subscribe to after-filtering event
        this.emitter.on(
            ['initialized', 'after-filtering'],
            () => this.toggle()
        );

        /** @inherited */
        this.initialized = true;
    }

    /**
     * Toggle no results message
     */
    toggle() {
        if (this.tf.getValidRowsNb() > 0) {
            this.hide();
        } else {
            this.show();
        }
    }

    /**
     * Show no results message
     */
    show() {
        if (!this.initialized || !this.isEnabled()) {
            return;
        }
        this.onBeforeShow(this.tf, this);

        this.setWidth();
        this.cont.style.display = 'block';

        this.onAfterShow(this.tf, this);
    }

    /**
     * Hide no results message
     */
    hide() {
        if (!this.initialized || !this.isEnabled()) {
            return;
        }
        this.onBeforeHide(this.tf, this);

        this.cont.style.display = NONE;

        this.onAfterHide(this.tf, this);
    }

    /**
     * Sets no results container width
     * @private
     */
    setWidth() {
        if (!this.initialized || this.isExternal || !this.isEnabled()) {
            return;
        }
        let tf = this.tf;
        if (tf.gridLayout) {
            let gridLayout = tf.feature('gridLayout');
            this.cont.style.width = gridLayout.headTbl.clientWidth + 'px';
        } else {
            this.cont.style.width = (tf.dom().tHead ?
                tf.dom().tHead.clientWidth :
                tf.dom().tBodies[0].clientWidth) + 'px';
        }
    }

    /** Remove feature */
    destroy() {
        if (!this.initialized) {
            return;
        }
        removeElm(this.cont);
        this.cont = null;
        // unsubscribe to after-filtering event
        this.emitter.off(['after-filtering'], () => this.toggle());

        this.initialized = false;
    }
}
