
from Branch.models import Branch
from Product.models import Category, Product, Product_Type

def context_processor(request):
    branches = Branch.objects.all()
    categories = Category.objects.all()
    
    unsorted_categories = []
    # get published categories
    suits = Category.objects.filter(category__suit_product_type__publish = True)
    if suits:
        unsorted_categories.append(suits)
    tops = Category.objects.filter(category__top_product_type__publish = True)
    if tops:
        unsorted_categories.append(tops)
    foot_wear = Category.objects.filter(category__foot_wear_product_type__publish = True)
    if foot_wear:
        unsorted_categories.append(foot_wear)
    products = Category.objects.filter(category__product_type__publish = True)
    if products:
        unsorted_categories.append(products)
    # filter categories
    sorted_categories = []
    
    for pgroups in unsorted_categories:
        for category in pgroups:
            if category not in sorted_categories:
                sorted_categories.append(category)
    return {"branches": branches, "categories":categories,
            "sorted_categories":sorted_categories,
            'product_groups':Product_Type.P_GROUP.keys(),
            'age_groups': Product.AGE_GROUP,
            'genders':Product.GENDER}