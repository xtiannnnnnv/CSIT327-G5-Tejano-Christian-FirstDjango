from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class ProfileUpdateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="student",
            password="SecurePassword-328!",
            course="Computing",
        )

    def test_profile_requires_login(self):
        response = self.client.get(reverse("profile"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('profile')}",
        )

    def test_user_can_update_profile_without_changing_role(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("profile"),
            {
                "username": "updated-student",
                "email": "student@example.com",
                "first_name": "Updated",
                "last_name": "Student",
                "course": "Software Engineering",
                "role": get_user_model().Role.ADMIN,
            },
        )

        self.assertRedirects(response, reverse("profile"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updated-student")
        self.assertEqual(self.user.course, "Software Engineering")
        self.assertEqual(self.user.role, get_user_model().Role.STUDENT)


class SignUpFeedbackTests(TestCase):
    def test_successful_signup_adds_success_message(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "new-student",
                "email": "new-student@example.com",
                "first_name": "New",
                "last_name": "Student",
                "course": "Computing",
                "password1": "SecurePassword-328!",
                "password2": "SecurePassword-328!",
            },
        )

        self.assertRedirects(
            response,
            reverse("login"),
            fetch_redirect_response=False,
        )
        messages = list(response.wsgi_request._messages)
        self.assertEqual(
            str(messages[0]),
            "Your account was created successfully. You can now log in.",
        )
