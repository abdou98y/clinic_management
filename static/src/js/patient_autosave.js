odoo.define('clinic_management.patient_autosave', function (require) {
    "use strict";

    const { onMounted } = owl;
    const FormRenderer = require("@web/views/form/form_renderer").FormRenderer;

    // Patch FormRenderer
    FormRenderer.prototype.setup = function () {
        this._super.apply(this, arguments);

        onMounted(() => {
            // Listen for any one2many list "record created" event
            this.el.addEventListener("o2m_record_created", () => {
                // Force form reload (simulates autosave-like behavior)
                this.env.bus.trigger("RELOAD");
            });
        });
    };
});
