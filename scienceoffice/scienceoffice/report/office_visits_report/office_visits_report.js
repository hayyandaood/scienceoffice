// Copyright (c) 2023, Diamond pharma and contributors
// For license information, please see license.txt
/* eslint-disable */



//		frappe.query_report.set_filter_value('payment_terms', "");


// frappe.query_reports["Balance Sheet"]["filters"].push({
// 	"fieldname": "accumulated_values",
// 	"label": __("Accumulated Values"),
// 	"fieldtype": "Check",
// 	"default": 1
// });


frappe.query_reports["Office Visits Report"] = {
	"filters": [
		{
			fieldname: "based_on",
			label: __("Based On"),
			fieldtype: "Select",
			options: [
				"Visits",
				"Visit Messages",
				"Visit Samples",
				"Visit Publication",
				"Visit Resident Practioner",
				"Visit Persuasion Techniques",
				""
			],
			default: "Visits",
			reqd: 1,

			on_change: () => {
			 	var based_on = frappe.query_report.get_filter_value('based_on');
				if (based_on =="Visit Messages"){
					// will show/hide required fields by using show()/hide()
//			 		frappe.query_report.filters[0].$wrapper.hide();)
				};
			},	
		},
		{
			fieldname: "sc_city",
			label: __("Scientfic Office"),
			fieldtype: "Link",
			options: "Branch",
		},
		{
			fieldname: "team_leader",
			label: __("Team Leader"),
			fieldtype: "Link",
			options: "Medical Rep",
		},
		{
			fieldname: "medical_representative",
			label: __("Medical Representative"),
			fieldtype: "Link",
			options: "Medical Rep",
		},
		{
			fieldname: "date_of_visit",
			label: __("Date Of Visit"),
			fieldtype: "Date",
		},
		{
			fieldname: "medical_facility",
			label: __("Medical Facility Name"),
			fieldtype: "Link",
			options:"Medical Facility"
		},
		{
			fieldname: "doctor",
			label: __("doctor_name"),
			fieldtype: "Link",
			options:"Medical Practitioner"

		},

		{
			fieldname: "group_by_sc_city",
			label: __("Group By Sceintific Office"),
			fieldtype: "Check",
		},
		{
			fieldname: "group_by_team_leader",
			label: __("Group By Team Leader"),
			fieldtype: "Check",
		},
		{
			fieldname: "group_by_medical_representative",
			label: __("Group By Medical Representative"),
			fieldtype: "Check",
		},

		{
			fieldname: "group_by_date_of_visit",
			label: __("Group By Date Of Visit"),
			fieldtype: "Check",
		},
		{
			fieldname: "group_by_medical_facility",
			label: __("Group By Medical Facility"),
			fieldtype: "Check",
		},
		{
			fieldname: "group_by_doctor",
			label: __("Group By Doctor"),
			fieldtype: "Check",
		},

	]
};
