import json
from unittest.mock import patch

from django.core import mail
from django.test import Client


def test_send_email_should_succeed(mailoutbox, settings) -> None:
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    assert len(mailoutbox) == 0
    mail.send_mail(
        subject="Test Subject",
        message="This is a test message.",
        from_email="from@example.com",
        recipient_list=["to@example.com"],
        fail_silently=False,
    )
    assert len(mailoutbox) == 1
    sent_email = mailoutbox[0]
    assert sent_email.subject == "Test Subject"
    assert sent_email.body == "This is a test message."
    assert sent_email.from_email == "from@example.com"
    assert sent_email.to == ["to@example.com"]


def test_send_email_without_argument_should_send_empty_email(client: Client):
    with patch("companies.views.send_mail") as mock_send_mail_function:
        response = client.post(
            path="/send-email/",
        )
        response_content = json.loads(response.content)
        assert response.status_code == 200
        assert response_content["status"] == "success"
        assert response_content["info"] == "email sent successfully"
        mock_send_mail_function.assert_called_with(
            subject=None,
            message=None,
            from_email="golestan1369@gmail.com",
            recipient_list=["golestan1369@gmail.com"],
        )


def test_send_email_with_get_should_fail(client: Client):
    response = client.get(
        path="/send-email/",
    )
    assert response.status_code == 405
    assert json.loads(response.content) == {"detail": 'Method "GET" not allowed.'}
