import pandas as pd
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin


# Create your views here.
@xframe_options_sameorigin
def home(request):
    template_name = 'datosaccion/home.html'
    path = 'static/data/datosaccion/artesanos_por_pueblo.csv'
    df = pd.read_csv(path)
    context = dict(pueblos_data=df.to_dict('records'))
    return render(request, template_name, context)