from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from .funs import compare_month, compare_material, columnplot

materiallist = ['steel', 'oil', 'corn', 'grain', 'gasoline', 'lumber', 'wood', 'rubber',
                'hydrogen', 'oxygen', 'bauxite', 'iron', 'magnesium', 'manganese', 
                'cobalt', 'nickle', 'silver']
monthslist = ['January', 'February', 'March', 'April', 'May', 'June', 
            'July', 'August', 'September', 'October', 'November', 'December']


def home(request):
    """Handles requests for the home page, including plotting single materials, comparing two materials, or comparing two months."""
    image_url = None
    error_message = None 
    material2 = None
    month2 = None
    if request.method == 'POST':
        material1 = request.POST.get('colname1')
        colour = request.POST.get('colour')
        image_stream = columnplot(material1,colour)
        file_name = f'plot_{material1}.png'
        file_path = default_storage.save(file_name, image_stream)
        image_url = default_storage.url(file_path)  
    return render(request, 'home.html', {'image_url': image_url,
                                         'material2': material2,
                                         'month2': month2,
                                         "materials":materiallist,
                                         "months":monthslist})

def home2(request):
    """Handles requests for the home page, including plotting single materials, comparing two materials, or comparing two months."""
    image_url = None
    material2 = None
    month2 = None
    if request.method == 'POST':
        material1 = request.POST.get('colname1')
        material2 = request.POST.get('colname2')
        image_stream = compare_material(material1, material2) if material2 else columnplot(material1)
        file_name = f'plot_{material1}vs{material2}.png' if material2 else f'plot_{material1}.png'
        file_path = default_storage.save(file_name, image_stream)
        image_url = default_storage.url(file_path)
    return render(request, 'home.html', {'image_url': image_url,
                                         'material2': material2,
                                         'month2': month2,
                                         "materials":materiallist,
                                         "months":monthslist})

def home3(request):
    """Handles requests for the home page, including plotting single materials, comparing two materials, or comparing two months."""
    image_url = None
    material2 = None
    month2 = None
    if request.method == 'POST':
        month1 = request.POST.get('monthname1')
        month2 = request.POST.get('monthname2')
        image_stream = compare_month(month1, month2)
        file_name = f'compare_{month1}vs{month2}.png'
        file_path = default_storage.save(file_name, image_stream)
        image_url = default_storage.url(file_path)
    return render(request, 'home.html', {'image_url': image_url,
                                         'material2': material2,
                                         'month2': month2,
                                         "materials":materiallist,
                                         "months":monthslist})
