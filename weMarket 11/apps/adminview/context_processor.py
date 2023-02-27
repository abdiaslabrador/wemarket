from apps.adminview.models import enterprisedata, Templates

def enterprise_processor(request):
 	enterprise = enterprisedata.objects.get(id=0)  
 	templates = Templates.objects.get(isSelected=True)      
 	return {'enterprise': enterprise, 'templates':templates}