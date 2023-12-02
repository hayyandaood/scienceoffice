// Copyright (c) 2023, Diamond pharma and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Office Targets Report"] = {
	"filters": [
		{
			fieldname: "based_on",
			label: __("Based On"),
			fieldtype: "Select",
			options: [
				"Target Items",
				"Target Samples",
			],
			default: "Target Items",
			reqd: 1,
		},
		{
			fieldname: "sc_city",
			label: __("Scientfic Office"),
			fieldtype: "Link",
			options: "Branch",
		},
		{
			fieldname: "product_group",
			label: __("Product Group"),
			fieldtype: "Link",
			options: "Item Group",
		},
		{
			fieldname: "year",
			label: __("Year"),
			fieldtype: "Data",
		},
		{
			fieldname: "group_by_sc_city",
			label: __("Group By Sceintific Office"),
			fieldtype: "Check",
		},
		{
			fieldname: "group_by_item_group",
			label: __("Group By Item Group"),
			fieldtype: "Check",
		},

		{
			fieldname: "group_by_year",
			label: __("Group By By Year"),
			fieldtype: "Check",
		},
		{
			fieldname: "group_by_month",
			label: __("Group By Month"),
			fieldtype: "Check",
		},




	]
};
