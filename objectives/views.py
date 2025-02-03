from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import SkiObjective, InterestedParty
from django.db.models import Q

class ObjectiveListView(ListView):
    model = SkiObjective
    template_name = 'objectives/objective_list.html'
    context_object_name = 'objectives'
    paginate_by = 50

    def get_queryset(self):
        queryset = SkiObjective.objects.all()
        
        # Filter by search query
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(area__icontains=q) |
                Q(type__icontains=q)
            )
        
        # Filter by interest level
        interest = self.request.GET.get('interest')
        if interest:
            queryset = queryset.filter(interest_level=interest)
            
        # Filter by season
        season = self.request.GET.get('season')
        if season:
            queryset = queryset.filter(best_season__icontains=season)
            
        # Sort
        sort = self.request.GET.get('sort')
        if sort == 'distance':
            queryset = queryset.order_by('distance')
        elif sort == 'vert':
            queryset = queryset.order_by('vertical_gain')
        elif sort == 'name':
            queryset = queryset.order_by('name')
        else:
            queryset = queryset.order_by('-interest_level', 'name')
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interest_choices'] = SkiObjective.INTEREST_CHOICES
        return context 

class ObjectiveDetailView(DetailView):
    model = SkiObjective
    template_name = 'objectives/objective_detail.html'
    context_object_name = 'objective'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ObjectiveCreateView(CreateView):
    model = SkiObjective
    template_name = 'objectives/objective_form.html'
    fields = ['name', 'distance', 'vertical_gain', 'area', 'aspect', 'trip_report_link',
              'interest_level', 'type', 'skill_level', 'strenuous_level', 'lowest_elevation',
              'highest_elevation', 'best_season', 'notes']

class ObjectiveUpdateView(UpdateView):
    model = SkiObjective
    template_name = 'objectives/objective_form.html'
    fields = ['name', 'distance', 'vertical_gain', 'area', 'aspect', 'trip_report_link',
              'interest_level', 'type', 'skill_level', 'strenuous_level', 'lowest_elevation',
              'highest_elevation', 'best_season', 'notes']

def register_interest(request, pk):
    objective = get_object_or_404(SkiObjective, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('comment', '')
        
        if name and email:
            InterestedParty.objects.create(
                objective=objective,
                name=name,
                email=email,
                comment=comment
            )
            messages.success(request, 'Successfully registered interest!')
        else:
            messages.error(request, 'Please provide both name and email.')
    
    return redirect('objective-detail', pk=pk) 