# Copyright (c) 2022, Diamond pharma and contributors
# For license information, please see license.txt

import frappe

from frappe.model.document import Document
from frappe.utils import add_days, cint, cstr, date_diff, formatdate, getdate,get_weekday, get_time

from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee
from datetime import datetime, timedelta
import json




class MedVisitPlan(Document):
	@frappe.whitelist()
	def generate_schedule(self):
		if self.docstatus != 0:
			return
		self.set("schedules", [])
		count = 1
		for d in self.get("visit_generation_data"):
			s_list = []
			s_list = self.create_schedule_list(d.start_date, d.end_date, d.no_of_visits, d.team_leader)

			for i in range(d.no_of_visits):
				child = self.append("schedules")
				child.practitioner= d.practitioner
				child.facility = d.facility
				child.scheduled_date = s_list[i].strftime("%Y-%m-%d")
				child.visit_time = datetime.strptime(d.visit_time,"%H:%M:%S").time()
				child.idx = count
				count = count + 1
				child.team_leader = d.team_leader
				child.medical_representative = d.medical_representative


	@frappe.whitelist()
	def validate_end_date_visits(self):
		

		days_in_period = {
				"Weekly": 7,
				"BiWeekly":14,
				"ThreeWeeks": 21, 
				"Monthly": 30, 
				"Quarterly": 91, 
				"Half Yearly": 182, 
				"Yearly": 365}
		for item in self.visit_generation_data:
			

			if item.periodicity and item.periodicity != "Random" and item.start_date:
				if not item.end_date:
					if item.no_of_visits:
						item.end_date = add_days(
							item.start_date, item.no_of_visits * days_in_period[item.periodicity]
						)
					else:
						item.end_date = add_days(item.start_date, days_in_period[item.periodicity])

				diff = date_diff(item.end_date, item.start_date) + 1
				no_of_visits = cint(diff / days_in_period[item.periodicity])

				if not item.no_of_visits or item.no_of_visits == 0:
					item.end_date = add_days(item.start_date, days_in_period[item.periodicity])
					diff = date_diff(item.end_date, item.start_date) + 1
					item.no_of_visits = cint(diff / days_in_period[item.periodicity])
					
					

				elif item.no_of_visits > no_of_visits:
					item.end_date = add_days(
						item.start_date, item.no_of_visits * days_in_period[item.periodicity]
					)

				elif item.no_of_visits < no_of_visits:
					item.end_date = add_days(
						item.start_date, item.no_of_visits * days_in_period[item.periodicity]
					)

	def create_schedule_list(self, start_date, end_date, no_of_visit, team_leader):

		schedule_list = []
		start_date_copy = start_date
		date_diff = (getdate(end_date) - getdate(start_date)).days
		add_by = date_diff / no_of_visit

		for visit in range(cint(no_of_visit)):
			if getdate(start_date_copy) < getdate(end_date):
				start_date_copy = add_days(start_date_copy, add_by)
				if len(schedule_list) < cint(no_of_visit):
					schedule_date = self.validate_schedule_date_for_holiday_list(
						getdate(start_date_copy), team_leader
					)
					if schedule_date > getdate(end_date):
						schedule_date = getdate(end_date)
					schedule_list.append(schedule_date)

		return schedule_list

	def validate_schedule_date_for_holiday_list(self, schedule_date, team_leader):
	
		validated = False
		employee = frappe.db.get_value("Medical Rep", team_leader, "employee")


		if employee:
			holiday_list = get_holiday_list_for_employee(employee)
		else:
			holiday_list = frappe.get_cached_value("Company", self.company, "default_holiday_list")

		holidays = frappe.db.sql_list(
			"""select holiday_date from `tabHoliday` where parent=%s""", holiday_list
		)

		if not validated and holidays:

			# max iterations = len(holidays)
			for i in range(len(holidays)):
				if schedule_date in holidays:
					schedule_date = add_days(schedule_date, -1)
				else:
					validated = True
					break
		return schedule_date


	@frappe.whitelist()
	def create_visit(self):

		duration = 30

		for visit in self.schedules:

			Medical_visit = frappe.get_doc(
				{
					"doctype": "Medical Visit",
					"status":"Draft",
					"scientific_office": self.scientific_office,
					"company": self.company,
					"date_of_visit":visit.scheduled_date,
					"visit_time": visit.visit_time,
					"visit_duration":duration,
					"team_leader" : visit.team_leader,
					"medical_representative" : visit.medical_representative,
					"doctor" : visit.practitioner,
					"residentspeciality": "Resident",
					"medical_facility": visit.facility,
					"visit_plan" : self.name,
				})
			
			for d in self.get("message"):
				m = frappe.get_doc(
 					{
						"doctype" : "Med Visit Call",
						"message": d.message,
						"buying_cycle": d.buying_cycle,
						"item": d.item,
						"item_name": d.item_name,
 					}
				)
				Medical_visit.append("message",m)
			for d in self.get("samples"):
				s = frappe.get_doc(
					{
						"doctype":"Med Visit Samples",	
						"product": d.product,
						"product_group":d.product_group,
						"composition":d.composition,
						"package":d.package,
						"planned_qty":d.target,
					}
				)
				Medical_visit.append("samples",s)

			for d in self.get("publication"):
				p = frappe.get_doc(
					{
						"doctype":"Med Visit Publication",
 						"item_code": d.item_code ,
						"item_name": d.item_name ,
						"planned_qty":d.qty,
					}
				)
				Medical_visit.append("publication",p)
			Medical_visit.insert(ignore_permissions=1)

			description = frappe._("Reference: {0}-{1}, Facility : {2} and Doctor: {3}").format(
					visit.team_leader, visit.medical_representative,visit.facility, visit.practitioner
				)
			


			start_time = datetime.combine(
				getdate(visit.scheduled_date),get_time(visit.visit_time))
			
			end_time = start_time + timedelta(minutes=duration)
			
			event = frappe.get_doc(
				{
					"doctype": "Event",
					"subject": description,
					"description": description,
					"starts_on": cstr(start_time) ,
					"ends_on": end_time,
					"event_type": "Private",
				}
			)
			
			event.add_participant("Medical Rep", visit.team_leader)
			event.add_participant("Medical Rep", visit.medical_representative)

			event.insert(ignore_permissions=1)
		frappe.db.commit()

@frappe.whitelist()
def get_practionars(speciality, territory):

	result = frappe.db.sql(
		"""
			SELECT distinct p.practitioner_name,
				m.from_time,m.to_time,
				m.medical_facility, m.speciality, m.territory
			FROM `tabMedical Practitioner` p INNER JOIN
			`tabMedical Practitioner Schedule` m on
				m.parent = p.name
			WHERE p.active =1 and m.speciality = %s and m.territory= %s
		""", ( speciality,territory ),
		as_dict=1,
	)
	return result

@frappe.whitelist()
def get_item_query(doctype, txt, searchfield, start, page_len, filters):
	

	item_doctype = frappe.qb.DocType('Item')
	all_items = (
        frappe.qb.from_(item_doctype)
        .select('name','item_name')
        .where(item_doctype.name.like('%S%'))
		.where(item_doctype.item_name.like('%نماذج%'))
		).run(as_dict=False)
	
	return all_items


@frappe.whitelist()
def get_events(start, end, filters=None):

	events = []

	if isinstance(filters, str):
		filters = json.loads(filters)

	"""Returns events for Gantt / Calendar view rendering.

	:param start: Start date-time.
	:param end: End date-time.
	:param filters: Filters (JSON).
	"""
	from frappe.desk.calendar import get_event_conditions

	conditions = get_event_conditions("Medical Visit", filters)

	# if isinstance(conditions, str):
	# 	cond = "str"
	# if isinstance(conditions, dict):
	# 	cond = "dict"


	# user_roles = frappe.get_roles(), 
	# check doctype Medical Rep to get the detail of the User

	# team leader alloed to see all his members
	# Science Office manager allowed to see all the member of the office



	# if "Team Leader" in user_roles:
	# 	conditions["Team Leader"] = frappe.session.user
	# if "Team Member" in user_roles:
	# 	conditions["Team Member"] = frappe.session.user
	#	if "System Manager" not in user_roles:



	data = frappe.db.sql(
		"""
		select
		`tabMedical Visit`.name, `tabMedical Visit`.scientific_office,
		`tabMedical Visit`.doctor, `tabMedical Visit`.status,
		`tabMedical Visit`.medical_facility,`tabMedical Visit`.date_of_visit as 'start',
		`tabMedical Visit`.visit_time as 'start_time',
		`tabMedical Visit`.visit_duration,`tabMedical Visit`.team_leader,
		`tabMedical Visit`.medical_representative,`tabMedical Visit`.visit_time
		from
		`tabMedical Visit`
		where
		(`tabMedical Visit`.date_of_visit between %(start)s and %(end)s)
		and `tabMedical Visit`.status != 'Cancelled' and `tabMedical Visit`.docstatus < 2 {conditions}""".format(
			conditions=conditions
		),
		{"start": start, "end": end},
		as_dict=True,
	)


	for item in data:
		
		item.start_time = datetime.combine(getdate(item.start), get_time(item.start_time))
		item.end_time = item.start_time + timedelta(minutes=item.visit_duration)
		subject_data = []

#		subject_data.append(cond)

#		subject_data.append(cstr(item.start_time))
#		subject_data.append(cstr(item.end_time))

		subject_data.append(item.scientific_office)
		subject_data.append(item.doctor)
		subject_data.append(item.medical_facility)

		if item.team_leader :
			subject_data.append(item.team_leader)
		if item.medical_representative :
			subject_data.append(item.medical_representative)
		job_card_data = {
			"from_time": item.start_time,
			"to_time": item.end_time,
			"name": item.name,
			"subject": "\n".join(subject_data),
		}
		events.append(job_card_data)


	return events

