import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import io
import os
from django.conf import settings


file_path = os.path.join(settings.STATICFILES_DIRS[0], 'yamnew.csv')
df = pd.read_csv(file_path)
df = df.set_index('Month')

def columnplot(column_name,colour):
    if column_name not in df.columns:
        return None 
    data = df[column_name]
    plt.figure(figsize=(10, 6))
    plt.bar(data.index, data, color=colour)
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


def compare_month_element(row1, row2, column):
    data1 = df.loc[row1, column]
    data2 = df.loc[row2, column]
    plt.figure(figsize=(5, 5))
    plt.bar([row1, row2], [data1, data2], color=['skyblue', 'orange'], width=0.4)
    plt.xlabel('Month', fontsize=12, fontweight='bold')
    plt.ylabel('Value', fontsize=12, fontweight='bold')
    plt.title(f'{column} in {row1} & {row2}', fontsize=14, fontweight='bold')
    plt.yticks(fontsize=10, fontweight='bold')
    plt.xticks(fontsize=10, fontweight='bold')
    plt.grid(axis='y')
    plt.tight_layout()
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()
    image_stream.seek(0)
    return image_stream
