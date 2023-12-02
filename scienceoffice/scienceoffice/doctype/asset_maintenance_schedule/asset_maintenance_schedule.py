# Copyright (c) 2023, Diamond pharma and contributors
# For license information, please see license.txt



import frappe

from frappe.model.document import Document
from frappe.utils import add_days, cint, cstr, date_diff, formatdate, getdate

from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee
import datetime

import erpnext

class AssetMaintenanceSchedule(Document):

	@frappe.whitelist()
	def generate_schedule(self):

		schedule_item_doctype = frappe.qb.DocType('Maintenance Schedule Item')
		asset_doctype = frappe.qb.DocType('Asset')
		schedule_item = (
        	frappe.qb.from_(schedule_item_doctype)
			.join(asset_doctype)
			.on(asset_doctype.item_code == schedule_item_doctype.item_code)
        	.select(asset_doctype.name,asset_doctype.asset_name,asset_doctype.asset_category,  
		 			schedule_item_doctype.item_code,schedule_item_doctype.item_name,
					schedule_item_doctype.start_date,
					schedule_item_doctype.end_date,
					schedule_item_doctype.periodicity,
					schedule_item_doctype.no_of_visits)
#        	.where((room_doctype.type.like('Guest') | room_doctype.members.like(f'%{email}%')))
		).run(as_dict=True)


		self.set("items", [])
		count = 1
		for d in schedule_item:
			child = self.append("items")
			child.asset = d.name
			child.asset_name = d.asset_name
			child.asset_category= d.asset_category
			child.item_code= d.item_code
			child.item_name= d.item_name
			child.start_date= d.start_date
			child.end_date= d.end_date
			child.periodicity= d.periodicity
			child.no_of_visits = d.no_of_visits
			child.idx = count
			count = count + 1


	@frappe.whitelist()
	def create_visit(self):

		company = erpnext.get_default_company()
		Maintenance_team = get_maintenance_team()

		for d in self.items:
			
			if not frappe.db.exists("Asset Maintenance",{"asset_name" : d.asset_name}):
				Asset_Maintenance = frappe.get_doc(
					{
						"doctype": "Asset Maintenance",
						"asset_name":d.asset_name,
						"asset_category": d.asset_category,
						"company": company,
						"item_code":d.item_code,
						"maintenance_team" : Maintenance_team,
						"maintenance_manager" : "",
						"maintenance_manager_name": "",
			
					}
				)
				Asset_Maintenance_task = frappe.get_doc(
					{
						"doctype": "Asset Maintenance Task",
						"maintenance_task":d.asset_name,
						"maintenance_type": "Preventive Maintenance",
						"maintenance_status": "Planned",
						"start_date":d.start_date,
						"periodicity" : d.periodicity,
						"end_date" : d.end_date,
						"certificate_required": 0,
						"assign_to" : "hkamalmaz@gmail.com",
					}
				)
				Asset_Maintenance.append("asset_maintenance_tasks",Asset_Maintenance_task)
				Asset_Maintenance.insert(ignore_permissions=1)

			else: 	
				if not frappe.db.exists("Asset Maintenance Task",
			    	{"parent" : d.asset_name, "periodicity" : d.periodicity}):

					Asset_maintenance = frappe.get_doc(
						'Asset Maintenance',d.asset_name
					)
					Asset_maintenance.append("asset_maintenance_tasks",{
							"doctype": "Asset Maintenance Task",
							"maintenance_task":d.asset_name,
							"maintenance_type": "Preventive Maintenance",
							"maintenance_status": "Planned",
							"start_date":d.start_date,
							"periodicity" : d.periodicity,
							"end_date" : d.end_date,
							"certificate_required": 0,
							"assign_to" : "hkamalmaz@gmail.com",
					})
					Asset_maintenance.save()


			frappe.db.commit()

def	get_maintenance_team():
	return "maintenance team"





