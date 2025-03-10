from django.test import TestCase
from datetime import date
from django.utils import timezone
from freezegun import freeze_time

from products.models import Product, Category
from django.contrib.auth.models import User
from reviews.models import Review


@freeze_time("2022-08-15")
class TestReviewModels(TestCase):
    """
    Reviews Model Tests
    """

    def setUp(self):
        """
        Creates test objects for Reviews app
        """

        self.categoryTest = Category.objects.create(
            name="Deals",
            friendly_name="deals",
        )

        self.productTest = Product.objects.create(
            category=self.categoryTest,
            name="oreo hoodie - white",
            description="Oreo themed hoodie in white",
            price=23.99,
            has_sizes=True,
        )

        self.userTest = User.objects.create(
            username="user1",
            password="password1",
            email='testuseremail@email.com',
        )

        self.reviewTest = Review.objects.create(
            product=self.productTest,
            user=self.userTest,
            title="review title",
            content="review content",
            rating=3,
            created_on=timezone.now(),
        )

    def test_review_string_method(self):
        """ Tests the string method on the review model """
        review = Review(title='review title')
        self.assertEqual(str(review), review.title)

    def test_review_title(self):
        """ Test the review title """
        self.assertEqual(self.reviewTest.title, 'review title')

    def test_review_content(self):
        """ Test the review content """
        self.assertEqual(self.reviewTest.content, 'review content')

    def test_review_rating(self):
        """ Test the review rating """
        self.assertEqual(self.reviewTest.rating, 3)

    def test_review_created_on(self):
        """ Test the review content """
        self.assertEqual(self.reviewTest.created_on, date(2022, 8, 15))

    def test_review_product_name(self):
        """ Test the review product """
        self.assertEqual(self.reviewTest.product.name, 'oreo hoodie - white')

    def test_review_product_category(self):
        """ Test the review product category """
        self.assertEqual(self.reviewTest.product.category.name, 'Deals')
