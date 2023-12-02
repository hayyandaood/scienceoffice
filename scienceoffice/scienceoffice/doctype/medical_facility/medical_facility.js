// Copyright (c) 2022, Diamond pharma and contributors
// For license information, please see license.txt

frappe.ui.form.on('Medical Facility', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on("Medical Facility Classification", {
	no_of_patients: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
//		if(!d.speciality) return;

		frappe.call({
			"method": "scienceoffice.scienceoffice.doctype.medical_facility.medical_facility.get_classification",
			args: {
				speciality: d.specialty,
				no_of_patients: d.no_of_patients
			},
			callback: function (data) {
				
				console.log(data);

				d.classification_value = data.message[0].classification_number;
				frm.refresh_field("classification")
			}
		});
	}
	}	
);





