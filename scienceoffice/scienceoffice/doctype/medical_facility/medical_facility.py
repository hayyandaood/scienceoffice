# Copyright (c) 2022, Diamond pharma and contributors
# For license information, please see license.txt


import frappe
from frappe import _

from frappe.model.document import Document


class MedicalFacility(Document):
	pass

@frappe.whitelist()
def	get_classification(speciality, no_of_patients):

	classification_docType = frappe.qb.DocType('Classification Type')

	classfication_value = (
		frappe.qb.from_(classification_docType)
	 	.select('classification_number')
	 	.where(classification_docType.speciality == speciality)
	 	.where(no_of_patients >= classification_docType.from_number)
	 	.where(no_of_patients <= classification_docType.to_number )
	).run(as_dict=1)

	
	return classfication_value



 
