# forms.py
from django import forms
from .models import Product, TypesOfCategory, Category

from django import forms
from .models import Product, Category, TypesOfCategory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'  # Specify fields if you need to exclude any

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Check if an instance exists (editing an existing product)
        if self.instance and self.instance.pk:
            # Filter categorytype based on the category of the existing product
            self.fields['categorytype'].queryset = TypesOfCategory.objects.filter(category=self.instance.category)
        elif 'category' in self.data:
            try:
                # Filter categorytype based on the posted category data (when creating a new product)
                selected_category = Category.objects.get(id=self.data.get('category'))
                self.fields['categorytype'].queryset = TypesOfCategory.objects.filter(category=selected_category)
            except (Category.DoesNotExist, ValueError):
                # If category is invalid or missing, use an empty queryset
                self.fields['categorytype'].queryset = TypesOfCategory.objects.none()
        else:
            # Default to an empty queryset when no category is selected
            self.fields['categorytype'].queryset = TypesOfCategory.objects.none()