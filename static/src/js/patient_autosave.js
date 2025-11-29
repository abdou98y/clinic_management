/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { useBus } from "@web/core/utils/hooks";

patch(FormController.prototype, {
    setup() {
        super.setup();
        useBus(this.env.bus, "RECORD-UPDATED", this._onRecordUpdated.bind(this));
        console.log("Auto save patch loaded");  // For debugging: Check browser console to confirm loading
    },

    _onRecordUpdated(ev) {
        const record = ev.detail.record || ev.detail;  // Handle potential event structure variations
        if (record === this.model.root && this.mode === "edit") {
            // Optional: Restrict to your patient model only
            if (this.model.root.resModel === "clinic.patient") {
                this.saveButtonClicked({
                    stayInEdit: true,
                    noReload: true,
                });
            }
        }
    },
});







// odoo.define('clinic_management.patient_autosave', function (require) {
//     "use strict";
//
//     const { onMounted } = owl;
//     const FormRenderer = require("@web/views/form/form_renderer").FormRenderer;
//
//     // Patch FormRenderer
//     FormRenderer.prototype.setup = function () {
//         this._super.apply(this, arguments);
//
//         onMounted(() => {
//             // Listen for any one2many list "record created" event
//             this.el.addEventListener("o2m_record_created", () => {
//                 // Force form reload (simulates autosave-like behavior)
//                 this.env.bus.trigger("RELOAD");
//             });
//         });
//     };
// });
