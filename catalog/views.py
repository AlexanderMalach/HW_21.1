from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from catalog.forms import ContactForm
from catalog.models import Product, ContactInfo, Blog


def render_home(request):
    return render(request, "home.html")


def render_contacts(request):
    latest_products = Product.objects.order_by("-created_at")[:5]
    for product in latest_products:
        print(product)
    return render(request, "contacts.html", {"latest_products": latest_products})


def contact_page(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Сохранение данных в базу данных
            return redirect("contact_page")  # Перенаправление после сохранения
    else:
        form = ContactForm()

    contacts = ContactInfo.objects.all()
    return render(
        request, "contacts/contact_page.html", {"form": form, "contacts": contacts}
    )


# def render_base(request):
#     return render(request, 'base.html')


# def render_base(request):
#     products = Product.objects.all()
#     context = {'products': products}
#     return render(request, 'product_list.html', context)

# def product_ditail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     context1 = {'product': product}
#     return render(request, 'product_detail.html', context1)


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class ProductCreateView(CreateView):
    model = Product
    fields = (
        "name",
        "description",
        "photo",
        "category",
        "price",
        "created_at",
        "updated_at",
    )
    success_url = reverse_lazy("catalog:catalog_list")


class ProductUpdateView(UpdateView):
    model = Product
    fields = (
        "name",
        "description",
        "photo",
        "category",
        "price",
        "created_at",
        "updated_at",
    )
    success_url = reverse_lazy("catalog:catalog_list")

    def get_success_url(self):
        return reverse_lazy("catalog:product_detail", args=[self.kwargs.get("pk")])


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:catalog_list")


class BlogListView(ListView):
    model = Blog

    def get_queryset(self):
        return Blog.objects.filter(publication_sign=True)


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    model = Blog
    fields = (
        "title",
        "content",
        "preview",
        "date_creation",
        "publication_sign",
    )
    success_url = reverse_lazy("catalog:blog_list")

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = (
        "title",
        "slug",
        "content",
        "preview",
        "date_creation",
        "publication_sign",
    )
    success_url = reverse_lazy("catalog:blog_list")

    def get_success_url(self):
        return reverse('catalog:blog_detail', kwargs={'pk': self.object.pk, 'slug': self.object.slug})


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy("catalog:blog_list")
