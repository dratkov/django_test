# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from test_task.forms import GeneralForm
from django.db import models
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json


def hello(request):
    model_res = None
    office_models_arr = []
    for m in models.get_models():
        if 'office.models' in str(m):
            office_models_arr.append(m)
            if model_res == None:
                model_res = m
    model_list_res = model_res.objects.all()
    #print user_model._meta.__dict__['_field_name_cache'][1].__dict__['verbose_name']
    return render_to_response('main.html', {'office_models_arr': office_models_arr, 'user_list': model_list_res, 'fields_name': model_res._meta.__dict__['_field_name_cache'], 'fields': model_res._meta.fields})


@csrf_exempt
def save_model_field(request):
    project_name = request.POST.get("project_name")
    model_name = request.POST.get("model_name")
    ID = request.POST.get("id")
    field_name = request.POST.get("field_name")
    field_value = request.POST.get("field_value")
    for m in models.get_models():
        if 'office.models' in str(m) and project_name == m._meta.app_label and m.__name__ == model_name:
            model_res = m.objects.get(id=ID)
            for f in model_res._meta.fields:
                if f.name == field_name:
                    setattr(model_res, f.name, field_value)
                    h = {}
                    if "Char" in f.get_internal_type():
                        h['char_field'] = field_value
                    elif "Integer" in f.get_internal_type():
                        h['integer_field'] = field_value
                    else:
                        h['date_field'] = field_value
                    form = GeneralForm(h)
                    form.is_valid()
                    errors_messages = []
                    print 111
                    for k in form.errors.keys():
                        if ('Char' in f.get_internal_type() and k == 'char_field') or ('Date' in f.get_internal_type() and k == 'date_field') or ('Integer' in f.get_internal_type() and k == 'integer_field'):
                            for e in form.errors[k]:
                                errors_messages.append(e)
                    if len(errors_messages) > 0:
                        return HttpResponse('[{"error": "1", "errors_messages": "' + errors_messages[0].encode("utf-8") + '", "field_name": "' + f.verbose_name + '"}]', mimetype="application/json")

                    model_res.save()
                    return HttpResponse('[{"error": "0", "field_name": "' + f.verbose_name + '"}]', mimetype="application/json")


@csrf_exempt
def get_all_model_row(request):
    project_name = request.POST.get("project_name")
    model_name = request.POST.get("model_name")
    model_res = None
    for m in models.get_models():
        if 'office.models' in str(m) and project_name == m._meta.app_label and m.__name__ == model_name:
            model_res = m
    json_string = serializers.serialize("json", model_res.objects.all())
    json_data = json.loads(json_string)
    if len(json_data) == 0:
        json_data = [{}]
    json_data[0]['fields_name'] = []
    json_data[0]['fields_internal_type'] = []
    json_data[0]['tables_name'] = []
    for f in model_res._meta.fields:
        if f.name == "id":
            continue
        json_data[0]['fields_name'].append(f.verbose_name)
        json_data[0]['tables_name'].append(f.name)
        json_data[0]['fields_internal_type'].append(f.get_internal_type())
    json_string = json.dumps(json_data)
    return HttpResponse(json_string, mimetype="application/json")
