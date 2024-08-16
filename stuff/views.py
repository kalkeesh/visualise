from django.shortcuts import render
import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import io
from django.core.files.storage import default_storage
import os
from django.conf import settings

# Load the CSV file into a DataFrame and set the index to 'Month'
file_path = os.path.join(settings.STATICFILES_DIRS[0], 'yamnew.csv')
df = pd.read_csv(file_path)
df = df.set_index('Month')

def columnplot(column_name):
    """Generates a bar chart for a single column in the DataFrame."""
    if column_name not in df.columns:
        return None 
    data = df[column_name]
    plt.figure(figsize=(10, 6))
    plt.bar(data.index, data, color='red')
    plt.xlabel('Month')
    plt.ylabel('Value')
    plt.title(f'Bar Chart for {column_name}')
    plt.xticks(rotation=45)
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()
    image_stream.seek(0)
    return image_stream

def compare_material(col1, col2):
    """Generates a comparison bar chart for two columns in the DataFrame."""
    if col1 not in df.columns or col2 not in df.columns:
        return None

    data1 = df[col1]
    data2 = df[col2]

    x = range(len(data1))

    plt.figure(figsize=(12, 7))
    plt.bar(x, data1, width=0.4, label=col1, align='center')
    plt.bar([i + 0.4 for i in x], data2, width=0.4, label=col2, align='center')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.title(f'Comparison of {col1} and {col2}')
    plt.xticks([i + 0.2 for i in x], df.index, rotation=45)
    plt.legend()
    plt.tight_layout()
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()
    image_stream.seek(0)
    return image_stream

def compare_month(row1, row2):
    """Generates a comparison plot for two rows in the DataFrame."""
    if row1 not in df.index or row2 not in df.index:
        return None

    data1 = df.loc[row1]
    data2 = df.loc[row2]
    columns = df.columns
    plt.figure(figsize=(12, 7))
    plt.plot(columns, data1, marker='o', label=row1, linestyle='-', color='skyblue')
    plt.plot(columns, data2, marker='o', label=row2, linestyle='--', color='orange')
    plt.xlabel('Materials')
    plt.ylabel('Value')
    plt.title(f'Comparison of {row1} and {row2}')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()
    image_stream.seek(0)
    return image_stream

def home(request):
    """Handles requests for the home page, including plotting single materials, comparing two materials, or comparing two months."""
    image_url = None
    error_message = None 
    material2 = None
    month2 = None
    
    if request.method == 'POST':
        material1 = request.POST.get('colname1')
        material2 = request.POST.get('colname2')
        month1 = request.POST.get('monthname1')
        month2 = request.POST.get('monthname2')

        if month2:  # If month comparison is requested
            image_stream = compare_month(month1, month2)
        elif material2:  # If material comparison is requested
            image_stream = compare_material(material1, material2)
        else:  # Otherwise, plot the single material
            image_stream = columnplot(material1)

        if image_stream:
            if month2:
                file_name = f'compare_{month1}vs{month2}.png'
            elif material2:
                file_name = f'plot_{material1}vs{material2}.png'
            else:
                file_name = f'plot_{material1}.png'
                
            file_path = default_storage.save(file_name, image_stream)
            image_url = default_storage.url(file_path)
        else:
            if month2:
                error_message = f"One or both rows '{month1}' and '{month2}' do not exist. Please enter valid month names."
            else:
                error_message = f"One or both columns '{material1}' and '{material2}' do not exist. Please enter valid material names."
        
    return render(request, 'home.html', {'image_url': image_url, 'error_message': error_message, 'material2': material2, 'month2': month2})
