import base64

from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.core.files.base import ContentFile
from django.utils import timezone
from .forms import CreateProjectForm, CreateSwappableGroupForm, CreateMaterialForm, \
    CreatePrefixesForm, CreateModelFileForm, CreateDeployForm, CreatePauseForm
from .models import Project, SwappableGroup, Material, MaterialPrefix, ModelFile
from .tasks import bundle
import base64

"""
def create_project(request):
    if request.method == 'POST':
        form = CreateProjectForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            project = Project()

            project.title = data['title']
            file_name = "Bundle-"+data["title"].strip()+"-"+str(timezone.now().timestamp()).replace(".","")
            raw_file, project.asset_name = bundle(request.FILES['bundle'])
            project.bundle.save(file_name, ContentFile(raw_file))
            project.description = data['description']

            project.save()

            return HttpResponseRedirect('/bundler/success/')
    else:
        form = CreateProjectForm(initial={'x': 0, 'y': 0, 'z': 0, 'r': 0})
    return render(request, 'createProject.html', {'form': form})

"""

redirect = '/add_content'


def create_group(group_form):
    data = group_form.cleaned_data
    group = SwappableGroup()
    group.name = data['name']

    group.save()

    return HttpResponseRedirect(redirect)


def create_material(material_form):
    data = material_form.cleaned_data
    mat = Material()
    mat.hex_color = data['hex_color']

    mat.save()

    return HttpResponseRedirect(redirect)


def create_prefix(prefix_form):
    data = prefix_form.cleaned_data
    prefix = MaterialPrefix()
    prefix.prefix = data['prefix']
    prefix.save()
    prefix.materials.set(data['materials'])

    return HttpResponseRedirect(redirect)


def create_model_file(model_form, files):
    data = model_form.cleaned_data
    model_file = ModelFile()

    model_file.presentable_name = data['presentable_name']
    # Making slightly safer name for file management purposes
    # TODO: Add regex checks to clean methods and html templates (for all text inputs)
    model_file.hidden_name = ''.join(model_file.presentable_name.split()).lower()

    model_file.model_base = base64.b64encode(b''.join([i for i in files['model_base'].chunks()]))
    model_file.placeable = data['placeable']
    model_file.save()

    # Save many-to-many relations
    if len(data['prefixes']) > 0:
        model_file.prefixes.set(data['prefixes'])
    if data['group']:
        model_file.group.set([data['group']])
    return HttpResponseRedirect('/')


def create_page(request):
    prefix_form = CreatePrefixesForm()
    group_form = CreateSwappableGroupForm()
    material_form = CreateMaterialForm()
    model_form = CreateModelFileForm()
    if request.method == 'POST':

        if 'group_submit' in request.POST:
            gform = CreateSwappableGroupForm(request.POST)
            if gform.is_valid():
                return create_group(gform)
            group_form = gform

        if 'material_submit' in request.POST:
            mform = CreateMaterialForm(request.POST)
            if mform.is_valid():
                return create_material(mform)
            material_form = mform

        if 'prefix_submit' in request.POST:
            pform = CreatePrefixesForm(request.POST)
            if pform.is_valid():
                return create_prefix(pform)
            prefix_form = pform

        if 'model_submit' in request.POST:
            modform = CreateModelFileForm(request.POST, request.FILES)
            if modform.is_valid():
                return create_model_file(modform, request.FILES)
            model_form = modform

    return render(request, 'addContent.html', {'group_form': group_form,
                                               'prefix_form': prefix_form,
                                               'material_form': material_form,
                                               'model_form': model_form})


def create_project(request):
    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            project = Project()

            project.title = data['title']
            project.description = data['description']

            project.save()

            project.model_files.set(data['model_files'])

            return HttpResponseRedirect('/')
    else:
        form = CreateProjectForm()
    return render(request, 'createProject.html', {'form': form})


def model_success(request):
    return project_success(request)


def deploy_project(request):
    deploy_form = CreateDeployForm()
    pause_form = CreatePauseForm()
    if request.method == 'POST':

        if 'deploy_submit' in request.POST:
            dform = CreateDeployForm(request.POST)
            if dform.is_valid():
                project_data = dform.cleaned_data['selected_project']
                title = project_data.title
                model_items = project_data.model_files.all()
                names = [i.hidden_name for i in model_items]
                files = [f.model_base for f in model_items]
                bundle.delay(names, files, title)
                messages.success(request, 'Assets for ' + title + ' are being deployed....')

                return HttpResponseRedirect('/deploy_project')
            deploy_form = dform

        if 'pause_submit' in request.POST:
            pform = CreatePauseForm(request.POST)
            if pform.is_valid():
                data = pform.cleaned_data
                project = data['selected_project']
                proj = Project.objects.get(title=project.title)
                proj.status = "Not deployed"
                proj.save()

                return HttpResponseRedirect('/deploy_project')
            pause_form = pform

    return render(request, 'deployProjects.html', {'deploy_form': deploy_form, 'pause_form': pause_form})


def project_success(request):
    return render(request, 'landingPage.html')


