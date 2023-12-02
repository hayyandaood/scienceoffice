# Copyright (c) 2023, Diamond pharma and contributors
# For license information, please see license.txt


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

	if filters.based_on == "Target Items" :
		return get_target_items(filters)
	if filters.based_on == "Target Samples" :
		return get_target_samples(filters)

	return [],[]
	
def get_target_items(filters=None):

	data = frappe.db.sql(
		"""
		select distinct plan.sc_city as 'Sceintific Office', plan.year as 'Year',
		item.month as 'Month', item.product_group as 'Product Group',
		item.product as 'Product', 
		item.composition,item.package,item.target as 'Target',
		item.target_price as 'Target Price', item.target_value as 'Target Value'
		from `tabOffice Plan` plan, `tabOffice Plan Item` item
		where plan.name = item.parent 
		""",
		as_dict=True,
		)

	return get_items_plan(data, filters)


def get_items_plan(data, filters=None):

	gnames = []

	df = pd.DataFrame.from_records(data)

	if filters.sc_city:
		df = df[df["Sceintific Office"]== filters.sc_city]
	if filters.product_group:
		df = df[df["Product Group"]== filters.product_group]
	if filters.year:
		df = df[df["Year"]==cint(filters.year)]


	gropus = ["Sceintific Office", "Year", "Month", "Product Group"]

	if filters.group_by_sc_city == 1:
		gnames.append(gropus[0])
	if filters.group_by_year == 1:
		gnames.append(gropus[1])
	if filters.group_by_month == 1:
		gnames.append(gropus[2])
	if filters.group_by_item_group == 1:
		gnames.append(gropus[3])

	if len(gnames) > 0: 
		df = df.groupby(gnames).agg({"Target":'sum',"Target Price" : 'sum',"Target Value" : 'sum'}).reset_index()
		df['Percentage'] = 100 * df['Target']  / df['Target'].sum()


	return df.columns.tolist(), df.values.tolist()   

def get_target_samples(filters=None):

	data = frappe.db.sql(
		"""
		select distinct plan.sc_city as 'Sceintific Office', plan.year as 'Year',
		item.month as 'Month', item.product_group as 'Product Group',
		item.product as 'Product', 
		item.composition,item.package,item.sample as 'Sample',
		item.sample_price as 'Sample Price', item.sample_value as 'Sample Value'
		from `tabOffice Plan` plan, `tabOffice Plan Sample` item
		where plan.name = item.parent 
		""",
		as_dict=True,
		)

	return get_samples_plan(data, filters)


def get_samples_plan(data, filters=None):

	gnames = []

	df = pd.DataFrame.from_records(data)

	if filters.sc_city:
		df = df[df["Sceintific Office"]== filters.sc_city]
	if filters.product_group:
		df = df[df["Product Group"]== filters.product_group]
	if filters.year:
		df = df[df["Year"]==cint(filters.year)]


	gropus = ["Sceintific Office", "Year", "Month", "Product Group"]

	if filters.group_by_sc_city == 1:
		gnames.append(gropus[0])
	if filters.group_by_year == 1:
		gnames.append(gropus[1])
	if filters.group_by_month == 1:
		gnames.append(gropus[2])
	if filters.group_by_item_group == 1:
		gnames.append(gropus[3])

	if len(gnames) > 0: 
		df = df.groupby(gnames).agg({"SAmple":'sum',"Sample Price" : 'sum',"Sample Value" : 'sum'}).reset_index()
		df['Percentage'] = 100 * df['Sample']  / df['Sample'].sum()


	return df.columns.tolist(), df.values.tolist()   
