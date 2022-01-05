from django.shortcuts import render, redirect, get_object_or_404

from caseapplication.decorators import allowed_users
from caseapplication.models import Case, Batch, Product, CustomBatch
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import CaseForm, BatchForm, CustomBatchForm


@login_required
def home(request):
    # cases_created = Case.objects.myCases(request.user).order_by('-id')
    cases_created = None
    case = Case(add_user_id=request.user, status="N")
    form = CaseForm(instance=case, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('casemanager_home')
    else:
        form = CaseForm()
    # return render(request, 'casemanager/new_case_form.html', {'form': form})
    return render(request, 'casemanager/home.html', {'cases': cases_created, 'form': form})


@login_required
def new_case(request):
    if request.method == "POST":
        print(request.POST)
        products = request.POST.getlist('product')
        print(products)
        periods = request.POST.getlist('period')
        print(periods)
        case_types = request.POST.getlist('case_type')
        for p in products:
            for period in periods:
                for case_type in case_types:
                    print("period :", period)
                    case = Case(product=Product.objects.filter(id=p)[0], period=period, case_type=case_type,
                                add_user_id=request.user, status="N")
                    case.save()

        return redirect('casemanager_home')
    else:
        form = CaseForm()
    return render(request, 'casemanager/new_case_form.html', {'form': form})


@login_required
def new_batch(request):
    if request.method == "POST":
        batch = Batch(add_user_id=request.user, status="N")
        form = BatchForm(instance=batch, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('casemanager_new_batch')
    else:
        form = BatchForm()
    return render(request, 'casemanager/batch_home.html', {'form': form})


@login_required
@allowed_users(['admin', 'IT'])
def new_custom_batch(request):
    if request.method == "POST":
        batch = CustomBatch(add_user_id=request.user, status="N")
        form = CustomBatchForm(instance=batch, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('casemanager_new_custom_batch')
    else:
        form = CustomBatchForm()
    return render(request, 'casemanager/custom_batch_home.html', {'form': form})


@login_required
@allowed_users(['admin', 'IT'])
def delete_case_request_vw(request, id):
    case = get_object_or_404(Case, pk=id)
    if not request.user.is_superuser:
        if not request.user == case.add_user_id:
            raise PermissionDenied
    print(case.id)

    if request.method == "POST":
        if "Accept" in request.POST:
            case.delete()
        return redirect('casemanager_home')
    else:
        return render(request, 'casemanager/delete_case_request_form.html', {'case': case})


@login_required
def delete_batch_request_vw(request, id):
    batch = get_object_or_404(Batch, pk=id)
    if not request.user.is_superuser:
        if not request.user == batch.add_user_id:
            raise PermissionDenied
    print(batch.id)

    if request.method == "POST":
        if "Accept" in request.POST:
            batch.delete()
        return redirect('casemanager_new_batch')
    else:
        return render(request, 'casemanager/delete_batch_request_form.html', {'batch': batch})


@login_required
@allowed_users(['admin'])
def delete_custom_batch_request_vw(request, id):
    batch = get_object_or_404(CustomBatch, pk=id)
    if not request.user.is_superuser:
        if not request.user == batch.add_user_id:
            raise PermissionDenied
    print(batch.id)

    if request.method == "POST":
        if "Accept" in request.POST:
            batch.delete()
        return redirect('casemanager_new_custom_batch')
    else:
        return render(request, 'casemanager/delete_custom_batch_request_form.html', {'batch': batch})


def usageStats(request):
    result = dict()
    # resultdict = {i.add_user_id.username: result.get(i.id, 0) + 1 for i in Case.objects.all()}
    for i in Case.objects.all():
        if result.get(i.add_user_id.username):
            result[i.add_user_id.username] += 1
        else:
            result[i.add_user_id.username] = 1

    print(result)
    return render(request, 'casemanager/usagestats.html', {'data': result})
