import pandas as pd
import xml.etree.ElementTree as ET
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from .models import Nomenclature, LSI
from .forms import NomenclatureForm, LSIForm

# Аутентификация и регистрация
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# Главная страница
@login_required
def home(request):
    nomenclature_count = Nomenclature.objects.count()
    lsi_count = LSI.objects.count()
    
    context = {
        'nomenclature_count': nomenclature_count,
        'lsi_count': lsi_count
    }
    
    return render(request, 'accounts/home.html', context)

# Работа с номенклатурой
@login_required
def nomenclature_list(request):
    nomenclatures = Nomenclature.objects.all()
    return render(request, 'accounts/nomenclature_list.html', {'nomenclatures': nomenclatures})

@login_required
def create_nomenclature(request):
    if request.method == 'POST':
        form = NomenclatureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nomenclature_list')
    else:
        form = NomenclatureForm()
    return render(request, 'accounts/create_nomenclature.html', {'form': form})

@login_required
def edit_nomenclature(request, pk):
    nomenclature = Nomenclature.objects.get(pk=pk)
    if request.method == 'POST':
        form = NomenclatureForm(request.POST, instance=nomenclature)
        if form.is_valid():
            form.save()
            return redirect('nomenclature_list')
    else:
        form = NomenclatureForm(instance=nomenclature)
    return render(request, 'accounts/edit_nomenclature.html', {'form': form})

@login_required
def delete_nomenclature(request, pk):
    nomenclature = Nomenclature.objects.get(pk=pk)
    nomenclature.delete()
    return redirect('nomenclature_list')

# Работа с ЛСИ
@login_required
def lsi_list(request):
    lsi_items = LSI.objects.all()
    return render(request, 'accounts/lsi_list.html', {'lsi_items': lsi_items})

@login_required
def create_lsi(request):
    if request.method == 'POST':
        form = LSIForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lsi_list')
    else:
        form = LSIForm()
    return render(request, 'accounts/create_lsi.html', {'form': form})

@login_required
def edit_lsi(request, pk):
    # Получаем объект ЛСИ или возвращаем 404, если не найден
    lsi = get_object_or_404(LSI, pk=pk)
    
    if request.method == 'POST':
        # Создаем форму с переданными данными и текущим экземпляром
        form = LSIForm(request.POST, instance=lsi)
        
        if form.is_valid():
            # Сохраняем изменения
            form.save()
            messages.success(request, 'ЛСИ успешно обновлен')
            return redirect('lsi_list')  # Перенаправление после успешного редактирования
    else:
        # Создаем форму с текущими данными объекта
        form = LSIForm(instance=lsi)
    
    # Передаем форму и объект в шаблон
    context = {
        'form': form,
        'lsi': lsi
    }
    
    return render(request, 'accounts/edit_lsi.html', context)

def delete_lsi(request, pk):
    # Получаем объект ЛСИ или возвращаем 404, если не найден
    lsi = get_object_or_404(LSI, pk=pk)
    
    if request.method == 'POST':
        # Подтверждение удаления
        try:
            lsi.delete()
            messages.success(request, f'ЛСИ "{lsi.name}" успешно удален.')
            return redirect('lsi_list')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении: {str(e)}')
            return redirect('lsi_list')
    
    # Отображение страницы подтверждения удаления
    context = {
        'lsi': lsi
    }
    
    return render(request, 'accounts/delete_lsi.html', context)

# Импорт и экспорт
@login_required
def export_to_xml(request):
    nomenclatures = Nomenclature.objects.all()
    
    root = ET.Element('nomenclatures')
    
    for nomenclature in nomenclatures:
        nomenclature_elem = ET.SubElement(root, 'nomenclature')
        
        ET.SubElement(nomenclature_elem, 'abbreviation').text = nomenclature.abbreviation
        ET.SubElement(nomenclature_elem, 'short_name').text = nomenclature.short_name
        # Добавьте остальные поля
    
    tree = ET.ElementTree(root)
    response = HttpResponse(content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename=nomenclatures.xml'
    
    tree.write(response, encoding='unicode', method='xml')
    return response

@login_required
def import_from_xml(request):
    if request.method == 'POST' and request.FILES.get('xml_file'):
        xml_file = request.FILES['xml_file']
        
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            Nomenclature.objects.all().delete()
            
            for nomenclature_elem in root.findall('nomenclature'):
                Nomenclature.objects.create(
                    abbreviation=nomenclature_elem.find('abbreviation').text or '',
                    # Добавьте остальные поля
                )
            
            return redirect('nomenclature_list')
        
        except Exception as e:
            return render(request, 'accounts/error.html', {'error': str(e)})
    
    return redirect('nomenclature_list')

@login_required
def export_to_excel(request):
    model_type = request.GET.get('model_type')
    
    if not model_type:
        messages.error(request, 'Не указан тип модели для экспорта')
        return redirect('home')

    try:
        if model_type == 'lsi':
            queryset = LSI.objects.all()
            filename = 'lsi_export.xlsx'
            
            data = list(queryset.values(
                'id', 
                'name', 
                'description'
            ))
            
            df = pd.DataFrame(data)
            
        elif model_type == 'nomenclature':
            queryset = Nomenclature.objects.all()
            filename = 'nomenclature_export.xlsx'
            
            data = list(queryset.values(
                'id', 
                'abbreviation', 
                'short_name', 
                'full_name',
                'internal_code',
                'cipher',
                'ekps_code',
                'kvt_code',
                'drawing_number',
                'type_of_nomenclature'
            ))
            
            df = pd.DataFrame(data)
        
        else:
            messages.error(request, 'Неверный тип модели')
            return redirect('home')
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Данные')
            
            worksheet = writer.sheets['Данные']
            for col in worksheet.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = (max_length + 2)
                worksheet.column_dimensions[column].width = adjusted_width
        
        return response
    
    except Exception as e:
        messages.error(request, f'Ошибка экспорта: {str(e)}')
        return redirect('home')

@login_required
def import_from_excel(request):
    """
    Импорт данных из Excel файла
    """
    if request.method == 'POST':
        try:
            excel_file = request.FILES.get('excel_file')
            model_type = request.POST.get('model_type')
            
            if not excel_file:
                messages.error(request, 'Файл не загружен')
                return redirect('home')
            
            # Чтение Excel-файла
            df = pd.read_excel(excel_file)
            
            # Импорт для ЛСИ
            if model_type == 'lsi':
                # Очистка существующих данных (опционально)
                LSI.objects.all().delete()
                
                # Создание новых объектов
                lsi_objects = []
                for _, row in df.iterrows():
                    lsi_objects.append(LSI(
                        code=row.get('code', ''),
                        name=row.get('name', ''),
                        description=row.get('description', '')
                    ))
                
                # Bulk create для эффективности
                LSI.objects.bulk_create(lsi_objects)
                
                messages.success(request, f'Импортировано {len(lsi_objects)} записей ЛСИ')
            
            # Импорт для Номенклатуры
            elif model_type == 'nomenclature':
                # Очистка существующих данных (опционально)
                Nomenclature.objects.all().delete()
                
                # Создание новых объектов
                nomenclature_objects = []
                for _, row in df.iterrows():
                    nomenclature_objects.append(Nomenclature(
                        abbreviation=row.get('abbreviation', ''),
                        short_name=row.get('short_name', ''),
                        full_name=row.get('full_name', '')
                    ))
                
                # Bulk create для эффективности
                Nomenclature.objects.bulk_create(nomenclature_objects)
                
                messages.success(request, f'Импортировано {len(nomenclature_objects)} записей Номенклатуры')
            
            else:
                messages.error(request, 'Неверный тип модели')
            
            return redirect('home')
        
        except Exception as e:
            messages.error(request, f'Ошибка импорта: {str(e)}')
            return redirect('home')
    
    # GET-запрос
    return render(request, 'accounts/import_excel.html')

# Обработка ошибок
def error_view(request, error):
    return render(request, 'accounts/error.html', {'error': error})