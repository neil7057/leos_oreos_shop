from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time
from django.contrib.auth.models import User

from products.models import Product, Category
from reviews.models import Review


@freeze_time("2022-08-15")
class TestReviewsViews(TestCase):
    """
    Review Views Tests
    """

    def setUp(self):
        """
        Creates test objects for Reviews app
        """

        userTest = User.objects.create_user(
            username="user1",
            password="password1",
            email='testuseremail@email.com',
        )
        userTest.save()

        superuserTest = User.objects.create_superuser(
            username="superuser1",
            password="super_password1",
            email='testsuperuseremail@email.com',
        )
        superuserTest.save()

        self.categoryTest = Category.objects.create(
            name="Starwars",
            friendly_name="starwars",
        )

        self.productTest = Product.objects.create(
            category=self.categoryTest,
            name="16 pack",
            description="16 pack of cookies",
            price=13.99,
            has_sizes=False,
            image='image-file'
        )

        self.reviewTest = Review.objects.create(
            product=self.productTest,
            user=userTest,
            title="My review",
            content="My review content",
            rating=4.5,
            created_on=timezone.now(),
        )

        self.reviewTest2 = Review.objects.create(
            product=self.productTest,
            user=superuserTest,
            title="review title 2",
            content="content  x 2",
            rating=5,
            created_on=timezone.now(),
        )

    def test_add_review_page_for_authorized_user(self):
        """ Test add_review view for logged in user"""

        logged_in = self.client.login(
            username='user1', password='password1')
        self.assertTrue(logged_in)

        response = self.client.get('/reviews/add_review/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/add_review.html')

    def test_add_review_page_for_logged_out_user(self):
        """
        Checks add_review redirects to login
        if user is not logged in
        """

        response = self.client.get('/reviews/add_review/1')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/accounts/login/?next=/reviews/add_review/1')

    def test_edit_review_page_for_authorized_user(self):
        """ Test edit_review view for logged in user"""

        logged_in = self.client.login(
            username='user1', password='password1')
        self.assertTrue(logged_in)

        response = self.client.get('/reviews/edit_review/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/edit_review.html')

    def test_edit_review_page_for_unauthorized_user(self):
        """
        Checks edit_review redirects to product_details
        if user is not author of review
        """

        logged_in = self.client.login(
            username='user1', password='password1')
        self.assertTrue(logged_in)

        response = self.client.get('/reviews/edit_review/2/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/products/1/')

    def test_edit_other_user_review_page_for_superuser(self):
        """
        Checks edit_review redirects to product_details
        if superuser is not author of review
        """

        logged_in = self.client.login(
            username='superuser1', password='super_password1')
        self.assertTrue(logged_in)

        response = self.client.get('/reviews/edit_review/1/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/products/1/')

    def test_delete_review_page_for_unauthorized_user(self):
        """
        Checks delete_review redirects to product_details
        if user is not author of review
        """

        logged_in = self.client.login(
            username='user1', password='password1')
        self.assertTrue(logged_in)

        response = self.client.get('/reviews/delete_review/2/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '/products/1/')
