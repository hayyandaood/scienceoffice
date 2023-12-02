// Copyright (c) 2023, Diamond pharma and contributors
// For license information, please see license.txt

frappe.ui.form.on('Asset Maintenance Schedule', {
	refresh: function(frm) {
			frm.add_custom_button(__("Copy Data"), () => {
				frm.events.copy_data(frm);
			});
	},

	copy_data: function(frm){
		console.log("In data Coping");
		frm.call('generate_schedule').then(r => {
			frm.call('create_visit');
		});
	}
});
