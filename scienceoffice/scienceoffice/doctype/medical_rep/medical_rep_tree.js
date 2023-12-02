frappe.treeview_settings["Medical Rep"] = {
	fields: [
		{fieldtype:'Data', fieldname: 'rep_name',
			label:__('New Representative Name'), reqd:true},
		{fieldtype:'Link', fieldname:'employee',
			label:__('Employee'), options:'Employee',
			description: __("Please enter Employee Id of this Medical Rep")},
		{fieldtype:'Check', fieldname:'is_group', label:__('Group Node'),
			description: __("Further nodes can be only created under 'Group' type nodes")}
	],
}
