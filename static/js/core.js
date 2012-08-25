			function editToggle(obj){
				$(obj).toggle().next().toggle()
			}
			$(document).ready(function() {
				$(".date_change_field").datepicker({dateFormat: "yy-mm-dd"})
			})
			function saveField(obj, id, project_name, model_name, field_name){
				$.post('/request/save_field/',
					{id: id, project_name: project_name, model_name:
						model_name, field_name: field_name, field_value: $(obj).prev().val()},
				     	function(data){
						if(parseInt(data) != 1){
							$(".alert-error").html("<strong>Ошибка!</strong> " + data).show()	
							setTimeout(function(){ $(".alert-error").hide() }, 5000)
							return;
						}
						$(".alert-success").html("<strong>Ура!</strong> Изменение сохранено.").show()	
						setTimeout(function(){ $(".alert-success").hide() }, 5000)
						$(obj).parent().prev().html($(obj).prev().val());
						editToggle($(obj).parent().prev())
			       		})	
			}
			function getAllModelRow(project_name, model_name){
				$.post('/request/get_all_model_row/', 
					{project_name: project_name, model_name: model_name},
					function(data) {
						dataRes = data
						table = $($("table.table")[1])
						table.children().remove()
						tr = $("<tr>")	
						for(var i = 0; i < dataRes[0].fields_name.length; i++)
						     tr.append("<th>" + dataRes[0].fields_name[i] + "</th>")	
						table.append(tr)
						for (var i = 0; i < dataRes.length; i++) {
						     tr = $("<tr>");
						     for(var j = 0; j < dataRes[0].tables_name.length; j++){	
						     	for(var f in dataRes[i].fields){
								if (dataRes[0].tables_name[j] != f)
								   continue	
						     		td = $("<td>")
								span = $("<span>");
								span.html(dataRes[i].fields[f]);
								(function(span){
						     			span.click(function(){ editToggle(span); return false })
						     		})(span)
								span2 = $("<span>").hide()
								input = $("<input />").val(dataRes[i].fields[f])	
								if (dataRes[0].fields_internal_type[j].search("Date") != -1)
									input.addClass("date_change_field").attr({maxlength:10,size:10})
								if (dataRes[0].fields_internal_type[j].search("Char") != -1)
									input.addClass("input-xlarge")
								else
									input.addClass("input-small")
								button = $("<button>").addClass("btn").html("сохранить");
								(function(button, val, project, model, field){
									button.click(function(){
										saveField(button, val, project, model, field)
									})	
								})(button, dataRes[i].pk, dataRes[i].model.split(/\./)[0], dataRes[i].model.split(/\./)[1].replace(/^./,dataRes[i].model.split(/\./)[1][0].toUpperCase()), f)
								span2.append(input).append(button)
						     		td.append(span).append(span2)
								tr.append(td)
					     	     	}	     
					     	     }
						     table.append(tr)
						}
						$(".date_change_field").datepicker({dateFormat: "yy-mm-dd"})
				})
			}
