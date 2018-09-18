from veggienet import email, create_app

app = create_app(testing=True)


def test_email_token():
    secret_key = "sdfjksfd;lasdf"
    token = email.generate_email_confirmation_token(
        "user4321234@gmail.com", secret_key)
    assert token != "user4321234@gmail.com"

    email_address = email.confirm_email_confirmation_token(token, secret_key)
    assert email_address == "user4321234@gmail.com"


def test_invalid_token():
    token = "invalid token"

    result = email.confirm_email_confirmation_token(token, "asdf")
    assert not result


def test_send_email():
    with app.app_context():
        with app.test_request_context():
            with email.mail.record_messages() as outbox:
                email.send_email("test", "test@gmail.com",
                                 "<p>Hello</p>")

                assert len(outbox) == 1
                assert outbox[0].subject == 'test'
                assert outbox[0].sender == app.config['MAIL_DEFAULT_SENDER']
