// Copyright (c) 2022, Diamond pharma and contributors
// For license information, please see license.txt


// frappe.user
// frappe.user.has_role(['Administrator', 'System Manager', 'Report Manager']);
//  check docstatus
// 		
//	if (!frm.is_new() && frm.doc.docstatus === 0) 
//	docstatus = 0  in save save
//	docstatus = 1  in submit state
//	docstatus = 2  in deleted state
//


frappe.ui.form.on('Med Visit Plan', {
	refresh: function(frm) {
		if (!frm.is_new() && frm.doc.docstatus === 0) {
			frm.add_custom_button(__("Genrate Visits"), () => {
				frm.events.generate_visits(frm);
			});
			frm.add_custom_button(__("Select Practionars"), () => {
				select_practionars(frm);
			});

		} ;
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


	generate_visits: function(frm){
		if (!frm.is_new() && frm.doc.docstatus === 0) {
			frm.call('validate_end_date_visits').then(r => {
				frm.call('generate_schedule').then(r => {
					frm.call('create_visit');
				});
			});	
		}
	},
});



// d.$wrapper.find('.modal-content').css("left", "-200px");
// d.$wrapper.find('.modal-content').css("width", "900px");


// for Table MultiSelect check the report profit_and_lose_statement
var select_practionars = function(frm){
	var me = this;
	let selected_speciality = '';
	var dialog = new frappe.ui.Dialog({
		title: __("Select Practionars"),
		fields:[
			{ 
			  	fieldtype: 'Link', 
			  	options: 'Territory', 
			  	label: 'Territory', 
			  	fieldname: "territory_name", 
			},
			{ 
				fieldtype: 'Link', 
				options: 'Speciality', 
				label: 'Speciality', 
				fieldname: "speciality", 
			},
			{ fieldtype: 'Section Break' },
			{ fieldtype: 'HTML', fieldname: 'results_area' }
		]
	});

	var $wrapper; 
	var $results;
	var $placeholder;

	dialog.fields_dict["speciality"].df.onchange = () => {

		var speciality = dialog.fields_dict.speciality.input.value;
		var territory = dialog.fields_dict.territory_name.input.value;
		
		if(speciality && speciality!=selected_speciality){
			selected_speciality = speciality;
			var columns = ([
				"practitioner_name","from_time","to_time",
				"medical_facility", "speciality", "territory"
			]);
			var args = {
				speciality: speciality,
				territory:territory
			};
			get_practionars(frm,$results, $placeholder, args, columns);
		}
		else if(!speciality){
			selected_speciality = '';
			$results.empty();
			$results.append($placeholder);
		}
	};
	$wrapper = dialog.fields_dict.results_area.$wrapper.append(`<div class="results"
		style="border: 1px solid #d1d8dd; border-radius: 3px; height: 300px; overflow: auto;"></div>`);
	$results = $wrapper.find('.results');
	$placeholder = $(`<div class="multiselect-empty-state">
				<span class="text-center" style="margin-top: -40px;">
					<i class="fa fa-2x fa-heartbeat text-extra-muted"></i>
					<p class="text-extra-muted">No Practionars found</p>
				</span>
			</div>`);
	$results.on('click', '.list-item--head :checkbox', (e) => {
		$results.find('.list-item-container .list-row-check')
			.prop("checked", ($(e.target).is(':checked')));
	});

	dialog.set_primary_action(__('Add'), function() {
		let checked_values = get_checked_values($results);
		if(checked_values.length > 0){
			// frm.set_value("visit_generation_data", []);
			add_to_item_line(frm, checked_values);
			// dialog.hide();
		}
		else frappe.msgprint(__("Please select Practionar"));
	});

	dialog.get_close_btn().on('click', () => {
		dialog.hide();
	});


	// set width of the dialog

	dialog.$wrapper.find('.modal-content').css("width", "800px");
	
	dialog.show();
};


var get_practionars = function(frm, $results, $placeholder, args, columns) {

	$results.empty();
	frappe.call({
		method: "scienceoffice.scienceoffice.doctype.med_visit_plan.med_visit_plan.get_practionars",
		args: args, 
		callback: function(data) {
			if(data.message){
				$results.append(make_list_row(columns));
				for(let i=0; i<data.message.length; i++){
					$results.append(make_list_row(columns,data.message[i]));
				}
			}else {
				$results.append($placeholder);
			}
		}
	});
}


var make_list_row= function(columns, result={}) {

	// Make a head row by default (if result not passed)
	let head = Object.keys(result).length === 0;
	let contents = ``;

	columns.forEach(function(column) {
		contents += `<div class="list-item__content ellipsis">
			${
				head ? `<span class="ellipsis">${__(frappe.model.unscrub(column))}</span>`

				:(column !== "name" ? `<span class="ellipsis">${__(result[column])}</span>`
					: `<a class="list-id ellipsis">
						${__(result[column])}</a>`)
			}
		</div>`;
	})

	let $row = $(`<div class="list-item">
		<div class="list-item__content" style="flex: 0 0 10px;">
			<input type="checkbox" class="list-row-check" ${result.checked ? 'checked' : ''}>
		</div>
		${contents}
	</div>`);

	$row = list_row_data_items(head, $row, result);
	return $row;
};


var list_row_data_items = function(head, $row, result) {

	head ? $row.addClass('list-item--head')
		: $row = $(`<div class="list-item-container"
			data-practitioner_name= "${result.practitioner_name}"
			data-from = "${result.from_time}"
			data-to = "${result.to_time}"
			data-medical_facility = "${result.medical_facility}"
			data-speciality = "${result.speciality}"
			data-territory = "${result.territory}">
			</div>`).append($row);

	return $row
};



var get_checked_values= function($results) {
	return $results.find('.list-item-container').map(function() {
		let checked_values = {};
		if ($(this).find('.list-row-check:checkbox:checked').length > 0 ) {
			checked_values['practitioner_name'] = $(this).attr('data-practitioner_name');
			checked_values['medical_facility'] = $(this).attr('data-medical_facility');
			return checked_values;
		}
	}).get();
};

var add_to_item_line = function(frm, checked_values){


	for(let i=0; i<checked_values.length; i++){
		var si_item = frappe.model.add_child(frm.doc,
			 'Visit Generation Data', 'visit_generation_data');

		frappe.model.set_value(si_item.doctype, si_item.name, 'practitioner', checked_values[i]['practitioner_name']);
		frappe.model.set_value(si_item.doctype, si_item.name, 'facility', checked_values[i]['medical_facility']);
		frappe.model.set_value(si_item.doctype, si_item.name, 'visit_time', 
					frappe.format("10:00:00", { fieldtype: 'Time'} ));
	}
	frm.refresh_fields();

};





