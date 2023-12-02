// Copyright (c) 2022, Diamond pharma and contributors
// For license information, please see license.txt

frappe.ui.form.on('Medical Practitioner', {
	refresh: function(frm) {
		frm.add_custom_button(__("Update Facilities"), () => {
			frm.call("update_facilities");
		}, __("Utilities"));
	},

	before_save: function(frm){
		let speciality = frm.doc.specialities[0].practitioner_specialty;
		for(let i = 0; i < frm.doc.practitioner_schedule.length; i++){
			if (! frm.doc.practitioner_schedule[i].speciality) {
				frm.doc.practitioner_schedule[i].speciality = speciality
			}	
		}
	}

});


frappe.ui.form.on("Medical Practitioner Classification", {
	no_of_patients: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];

		frappe.call({
			"method": "scienceoffice.scienceoffice.doctype.medical_facility.medical_facility.get_classification",
			args: {
				speciality: d.specialty,
				no_of_patients: d.no_of_patients
			},
			callback: function (data) {
				d.classification_value = data.message[0].classification_number;
				frm.refresh_field("classification")
			}
		});
	}
	}	
);

frappe.ui.form.on("Medical Practitioner Schedule", {
	
	// speciality

	medical_facility_add: function(frm,cdt,cdn) {
		var d = locals[cdt][cdn]

		if(!d.medical_facility)
			return;
		frappe.db.get_value("Medical Facility", 
							{"name": d.medical_facility}, 
							"territory", 
							function(value) {
								d.territory = value.territory;
							});

	}
	}
);


