# Copyright (c) 2022, Diamond pharma and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now , getdate





class MedicalPractitioner(Document):

	@frappe.whitelist()
	def update_facilities(self):
		for d in self.get("practitioner_schedule"):	
			doc = frappe.get_doc('Medical Facility',d.medical_facility)
			if (doc):
				l = len(doc.medical_practitioners)+1
				c = frappe.get_doc(
					{
						"doctype" : "Medical Facility Practitioner",
						"parent" : d.medical_facility,
						"department": "",
						"section" : "",
						"practitioner" : d.parent,
						"type" : "Specialized",
						"active" : 1,
						"from_date" : getdate(),
						"idx": l
					}
				)
				found = False

				for p in doc.medical_practitioners:
					if p.practitioner == d.parent :
						found = True
						break
				
				if not found:
					doc.append("medical_practitioners",c)
					doc.save()


				# if (doc.medical_practitioners.count(d.parent) == 0):
				# 	print("practioner not found")
				# 	doc.append("medical_practitioners",c)
				# 	doc.save()
				frappe.db.commit()



