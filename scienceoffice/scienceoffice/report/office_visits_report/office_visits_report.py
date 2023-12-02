# Copyright (c) 2023, Diamond pharma and contributors
# For license information, please see license.txt

# import frappe

from __future__ import unicode_literals

import json

import frappe
import pandas as pd
from frappe import _, scrub, qb

from frappe.utils import (
	add_days,
	add_months,
	cint,
	date_diff,
	flt,
	get_first_day,
	get_last_day,
	get_link_to_form,
	getdate,
	rounded,
	today,
)




def execute(filters=None):

	if filters.based_on == "Visits" :
		return get_visits(filters)
	if filters.based_on == "Visit Messages" :
		return get_visits_messages(filters)
	if filters.based_on == "Visit Samples" :
		return get_visits_samples(filters)
	

	return [],[]
	
def get_visits(filters = None):

	data = frappe.db.sql(
		"""
		select status, scientific_office, team_leader, medical_representative,
		date_of_visit, visit_time,medical_facility,
		doctor, residentspeciality, 1 as Number_Of_Cases
		
		from `tabMedical Visit`  
		""",
		as_dict=True,
		)
	return get_visits_only(data,filters)

def get_visits_only(data, filters=None):

	gnames = []
	df = pd.DataFrame.from_records(data)
	df["date_of_visit"] = pd.to_datetime(df["date_of_visit"])
	df = get_basic_filters(df,filters)
	gnames = get_basic_grouping(gnames,filters)
	if len(gnames) > 0: 
		df = df.groupby(gnames).agg({"Number_Of_Cases":'count'}).reset_index()
		df['Percentage'] = 100 * df['Number_Of_Cases']  / df['Number_Of_Cases'].sum()

	return df.columns.tolist(), df.values.tolist()   

def get_visits_messages(filters=None):

	data = frappe.db.sql(
		"""
		select vi.status, vi.scientific_office, vi.team_leader, vi.medical_representative,
		vi.date_of_visit, vi.visit_time, vi.medical_facility, vi.doctor, vi.residentspeciality, 
		mes.message, mes.buying_cycle, mes.attitude, mes.item, mes.item_name, mes.reason,
		1 as Number_Of_Cases
		from `tabMedical Visit` vi, `tabMed Visit Call`  mes
		where mes.parent = vi.name
		""",
		as_dict=True,
		)
	return get_visits_messages_data(data,filters)

def get_visits_messages_data(data,filters = None):

	gnames = []
	extra_gropus = ["message", "buying_cycle", "item"]


	df = pd.DataFrame.from_records(data)
	df["date_of_visit"] = pd.to_datetime(df["date_of_visit"])
	df = get_basic_filters(df,filters)
	gnames = get_basic_grouping(gnames,filters)

	# if filters.group_by_messages == 1:
	# 	gnames.append(extra_gropus[0])

	if len(gnames) > 0: 
		df = df.groupby(gnames).agg({"Number_Of_Cases":'count'}).reset_index()
		df['Percentage'] = 100 * df['Number_Of_Cases']  / df['Number_Of_Cases'].sum()

	return df.columns.tolist(), df.values.tolist()   

def	get_visits_samples(filters):

	data = frappe.db.sql(
		"""
		select vi.status, vi.scientific_office, vi.team_leader, vi.medical_representative,
		vi.date_of_visit, vi.visit_time, vi.medical_facility, vi.doctor, vi.residentspeciality, 
		samp.product, samp.product_group, samp.composition, samp.package, samp.planned_qty, 
		samp.delivered_qty, 
		1 as Number_Of_Cases
		from `tabMedical Visit` vi, `tabMed Visit Samples`  samp
		where samp.parent = vi.name
		""",
		as_dict=True,
		)
	return get_visits_samples_data(data,filters)
	

def get_visits_samples_data(data,filters = None):

	gnames = []
	extra_gropus = ["planned_qty", "delivered_qty", "product"]


	df = pd.DataFrame.from_records(data)
	df["date_of_visit"] = pd.to_datetime(df["date_of_visit"])
	df = get_basic_filters(df,filters)
	gnames = get_basic_grouping(gnames,filters)

	# if filters.group_by_messages == 1:
	# 	gnames.append(extra_gropus[0])

	if len(gnames) > 0: 
		df = df.groupby(gnames).agg({"Number_Of_Cases":'count'}).reset_index()
		df['Percentage'] = 100 * df['Number_Of_Cases']  / df['Number_Of_Cases'].sum()

	return df.columns.tolist(), df.values.tolist()   



def	get_basic_filters(df,filters=None):
	if filters.sc_city:
		df = df[df["scientific_office"]== filters.sc_city]
	if filters.team_leader:
		df = df[df["team_leader"]== filters.team_leader]
	if filters.medical_representative:
		df = df[df["medical_representative"]== filters.medical_representative]
	if filters.date_of_visit:
		df = df[df["date_of_visit"]== filters.date_of_visit]
	if filters.medical_facility:
		df = df[df["medical_facility"]== filters.medical_facility]
	if filters.doctor:
		df = df[df["doctor"]== filters.doctor]
	return df

def get_basic_grouping(gnames,filters = None):

	gropus = ["scientific_office", "team_leader", "medical_representative", 
	   		  "date_of_visit", "medical_facility", "doctor"]
	
	if filters.group_by_sc_city == 1:
		gnames.append(gropus[0])
	if filters.group_by_team_leader == 1:
		gnames.append(gropus[1])

	if filters.group_by_medical_representative == 1:
		gnames.append(gropus[2])

	if filters.group_by_date_of_visit == 1:
		gnames.append(gropus[3])

	if filters.group_by_medical_facility == 1:
		gnames.append(gropus[4])
	if filters.group_by_doctor == 1:
		gnames.append(gropus[5])
	
	return gnames