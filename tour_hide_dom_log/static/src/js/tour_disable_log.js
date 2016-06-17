(function () {
    'use strict';
    // The code patched is located at `odoo/addons/web/static/src/js/Tour.js`
    var error = function (step, message) {
            var state = openerp.Tour.getState();
            console.log(state.tour.steps.slice());
            message += '\n tour: ' + state.id
                + (step ? '\n step: ' + step.id + ": '" + (step._title || step.title) + "'" : '' )
                + '\n href: ' + window.location.href
                + '\n referrer: ' + document.referrer
                + (step ? '\n element: ' + Boolean(!step.element || ($(step.element).size() && $(step.element).is(":visible") && !$(step.element).is(":hidden"))) : '' )
                + (step ? '\n waitNot: ' + Boolean(!step.waitNot || !$(step.waitNot).size()) : '' )
                + (step ? '\n waitFor: ' + Boolean(!step.waitFor || $(step.waitFor).size()) : '' )
                + "\n localStorage: " + JSON.stringify(localStorage);
            openerp.Tour.log(message, true);
            openerp.Tour.endTour();
        };
    openerp.Tour.error = error;

}());
