# -*- coding: utf-8 -*-
from django import forms
from . import models as mall_models


class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = mall_models.OrderReview
        fields = ('serve_score', 'deliver_score', 'process_score')


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = mall_models.ProductReview
        fields = ('product_score', 'review_detail', )


class ProductReviewPictureForm(forms.ModelForm):
    class Meta:
        model = mall_models.ProductReviewPicture
