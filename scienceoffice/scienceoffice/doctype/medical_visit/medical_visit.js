// Copyright (c) 2022, Diamond pharma and contributors
// For license information, please see license.txt


// helping code 




frappe.ui.form.on('Medical Visit', {
	 refresh: function(frm) {
		if (frm.doc.status !== "Draft") {
				frm.add_custom_button(__("Reopen Visit"), () => {
//					frm.remove_custom_button("Reopen Visit","Actions");
					frm.trigger("reopen_visit");
				}, __("Actions"));
	
		} 
		else {
			frm.add_custom_button(__("Close Visit"), () => {
				frm.trigger("close_visit");
			}, __("Actions"));
			frm.add_custom_button(__("Cancel Visit"), () => {
				frm.trigger("cancel_visit");
			}, __("Actions"));
		} 
	},

	close_visit: function(frm){
	//	if ( frappe.user.has_role(['Administrator', 'System Manager'])){
			frm.set_value("status","Closed")
			frm.save();
	//	};
	},
		
	cancel_visit: function(frm){
		frm.set_value("status","Cancelled");
		frm.save();
	},	

	reopen_visit: function(frm){
		frm.set_value("status","Draft")
		frm.save();
	},

	onload: function(frm) {


		frm.set_query('item', 'message', function() {
			return {
				filters: {
					'item_group' : "Products"
				}
			};
		});

		frm.set_query('product', 'samples', function() {
			return {
				query: "scienceoffice.scienceoffice.doctype.med_visit_plan.med_visit_plan.get_item_query",
				// filters: {
				
				// }
			};
		});


		frm.set_query('item_code','publication', function(){
			return{
				filters: {
					'item_group' : "Marketing Items"
				}
			};
		});
	},	


});
