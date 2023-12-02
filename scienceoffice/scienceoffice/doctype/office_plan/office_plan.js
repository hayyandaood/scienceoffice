// Copyright (c) 2022, Diamond pharma and contributors
// For license information, please see license.txt

frappe.ui.form.on('Office Plan', {



	onload_post_render: function(frm) {
		frm.get_field("target_item").grid.set_multiple_add("product", "target");
		console.log("entered post_render");
	},

	// refresh: function(frm) {

	// }
});
