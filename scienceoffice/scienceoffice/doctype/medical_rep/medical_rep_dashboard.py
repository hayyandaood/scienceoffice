from frappe import _


def get_data():
	return {
		"heatmap": True,
		"heatmap_message": _(
			"This is based on transactions against this Medical Represnatative. See timeline below for details"
		),
	}
