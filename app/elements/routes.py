from flask import flash, redirect, render_template, url_for
from sqlalchemy import and_
from . import elements
from . forms import ElementForm
from .. import db
from .. eventFrames . forms import EventFrameForm
from .. models import AttributeTemplate, Element, ElementAttribute, ElementTemplate, Enterprise, EventFrame, EventFrameTemplate, Site

modelName = "Element"

@elements.route("/elements", methods = ["GET", "POST"])
# @login_required
def listElements():
	# check_admin()
	elements = Element.query.all()
	return render_template("elements/elements.html", elements = elements)

@elements.route("/elements/dashboard/<int:elementId>", methods = ["GET", "POST"])
# @login_required
def dashboard(elementId):
	# check_admin()
	element = Element.query.get_or_404(elementId)
	elementAttributes = ElementAttribute.query.filter_by(ElementId = elementId)
	eventFrameTemplates = EventFrameTemplate.query. \
		join(ElementTemplate, Element). \
		outerjoin(EventFrame, and_(Element.ElementId == EventFrame.ElementId, EventFrameTemplate.EventFrameTemplateId == EventFrame.EventFrameTemplateId)). \
		filter(Element.ElementId == elementId)
	return render_template("elements/elementDashboard.html", elementAttributes = elementAttributes, element = element,
		eventFrameTemplates = eventFrameTemplates)

@elements.route("/elements/deleteEventFrame/<int:eventFrameId>", methods = ["GET", "POST"])
def deleteEventFrame(eventFrameId):
	eventFrame = EventFrame.query.get_or_404(eventFrameId)
	elementId = eventFrame.ElementId
	elementName = eventFrame.Element.Name
	eventFrameTemplateName = eventFrame.EventFrameTemplate.Name
	db.session.delete(eventFrame)
	db.session.commit()
	flash("You have successfully deleted a \"" + eventFrameTemplateName + "\" from element \"" + elementName + "\".", "alert alert-success")
	return redirect(url_for("elements.dashboard", elementId = elementId))

@elements.route("/elements/add", methods = ["GET", "POST"])
# @login_required
def addElement():
	# check_admin()
	operation = "Add"
	form = ElementForm()

	# Add a new element.
	if form.validate_on_submit():
		element = Element(Description = form.description.data, ElementTemplate = form.elementTemplate.data, Name = form.name.data)
		db.session.add(element)
		db.session.commit()
		flash("You have successfully added the new element \"" + element.Name + "\".", "alert alert-success")
		return redirect(url_for("elements.listElements"))

	# Present a form to add a new element.
	return render_template("addEditModel.html", form = form, modelName = modelName, operation = operation)

@elements.route("/elements/delete/<int:elementId>", methods = ["GET", "POST"])
# @login_required
def deleteElement(elementId):
	# check_admin()
	element = Element.query.get_or_404(elementId)
	db.session.delete(element)
	db.session.commit()
	flash("You have successfully deleted the element \"" + element.Name + "\".", "alert alert-success")
	return redirect(url_for("elements.listElements"))

@elements.route("/elements/edit/<int:elementId>", methods = ["GET", "POST"])
# @login_required
def editElement(elementId):
	# check_admin()
	operation = "Edit"
	element = Element.query.get_or_404(elementId)
	form = ElementForm(obj = element)

	# Edit an existing element.
	if form.validate_on_submit():
		element.Description = form.description.data
		element.ElementTemplate = form.elementTemplate.data
		element.Name = form.name.data

		db.session.commit()
		flash("You have successfully edited the element \"" + element.Name + "\".", "alert alert-success")
		return redirect(url_for("elements.listElements"))

	# Present a form to edit an existing element.
	form.description.data = element.Description
	form.elementTemplate.data = element.ElementTemplate
	form.name.data = element.Name
	return render_template("addEditModel.html", form = form, modelName = modelName, operation = operation)

@elements.route("/selectElement", methods = ["GET", "POST"])
@elements.route("/selectElement/<string:className>", methods = ["GET", "POST"])
@elements.route("/selectElement/<string:className>/<int:id>", methods = ["GET", "POST"])
# @login_required
def selectElement(className = None, id = None):
	# check_admin()
	elements = None
	elementTemplates = None
	enterprises = None
	site = None
	sites = None

	# Default case.
	if className == None:
		site = Site.query.join(Enterprise).order_by(Enterprise.Name, Site.Name).first()
		if site:
			className = site.__class__.__name__
	# Top level case.
	elif className == "root":
		enterprises = Enterprise.query.all()
	elif className == "Enterprise":
		sites = Site.query.filter_by(EnterpriseId = id)
		if sites:
			className = sites[0].__class__.__name__
	elif className == "Site":
		elementTemplates = ElementTemplate.query.filter_by(SiteId = id)
		if elementTemplates:
			className = elementTemplates[0].__class__.__name__
	elif className == "ElementTemplate":
		elements = Element.query.filter_by(ElementTemplateId = id)
		if elements:
			className = elements[0].__class__.__name__
	elif className == "Element":
		return redirect(url_for("elements.dashboard", elementId = id))

	# Present navigation for elements.
	return render_template("elements/selectElement.html", className = className, elements = elements, elementTemplates = elementTemplates,
		enterprises = enterprises, site = site, sites = sites)
