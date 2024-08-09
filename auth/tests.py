#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contains tests for `parse` module checking."""
import pytest
from fastapi.testclient import TestClient

from conftest import TestAuthSetup


@pytest.mark.usefixtures('client', 'get_db')
class TestAuth(TestAuthSetup):
    """
    Test cases for user authentication, including registration,
    login, checking user status, and logout.
    """

    cookie: str = ''

    def test_user_register_correct(self, client: TestClient) -> None:
        """
        Test case for successfully registering a new user.

        Sends a POST request to the /api/v1/register endpoint with
        valid user data. Asserts that the response status code is 201.
        """
        response = client.post('/api/v1/register', json={
            'name': 'test_user',
            'password': 'test_password',
            'email': 'test@gmail.com',
            'is_active': True,
            'is_stuff': False
        })
        assert response.status_code == 201

    def test_user_register_error_doubling(self, client: TestClient) -> None:
        """
        Test case for handling duplicate user registration.

        Sends a POST request to the /api/v1/register endpoint with
        an email that already exists. Asserts that the response status
        code is 409, indicating a conflict.
        """
        response = client.post('/api/v1/register', json={
            'name': 'new_user',
            'password': 'new_pass',
            'email': 'test@gmail.com',
            'is_active': False,
            'is_stuff': False
        })
        assert response.status_code == 409

    def test_login_user_correct(self, client: TestClient) -> None:
        """
        Test case for successfully logging in a user.

        Sends a POST request to the /api/v1/login endpoint with
        valid user credentials. Stores the received authentication
        token in the cookie and asserts that the response status code
        is 200.
        """
        response = client.post('/api/v1/login', json={
            'name': 'test_user',
            'password': 'test_password'
        })

        received_cookie = response.headers.get('set-cookie')
        TestAuth.cookie = received_cookie.replace('auth_token=', '')
        assert response.status_code == 200

    def test_login_user_error_creds(self, client: TestClient) -> None:
        """
        Test case for handling incorrect login credentials.

        Sends a POST request to the /api/v1/login endpoint with
        an incorrect password. Asserts that the response status code
        is 401, indicating unauthorized access.
        """
        response = client.post('/api/v1/login', json={
            'name': 'test_user',
            'password': 'test_pass'
        })
        assert response.status_code == 401

    def test_check_user_correct(self, client: TestClient) -> None:
        """
        Test case for verifying the user authentication status.

        Sends a POST request to the /api/v1/check_user endpoint
        with a valid authentication token in cookies. Asserts that
        the response status code is 200, indicating that the user is
        authenticated.
        """
        # pylint: disable=W0511
        # TODO: Need rework logic according to `AuthHandler.check_auth`
        #  method adjusted logic.
        client.cookies.set('auth_token', self.cookie)
        response = client.post('/api/v1/check_user')
        assert response.status_code == 200

    def test_check_user_error_creds(self, client: TestClient) -> None:
        """
        Test case for handling an invalid authentication token.

        Sends a POST request to the /api/v1/check_user endpoint
        with an invalid authentication token in cookies. Asserts
        that the response status code is 401, indicating unauthorized
        access.
        """
        # pylint: disable=W0511
        # TODO: Need rework logic according to `AuthHandler.check_auth`
        #  method adjusted logic.
        client.cookies.set('auth_token', 'invalid_cookie_file')
        response = client.post('/api/v1/check_user')
        assert response.status_code == 401

    def test_logout_user_correct(self, client: TestClient) -> None:
        """
        Test case for successfully logging out a user.

        Sends a POST request to the /api/v1/logout endpoint with
        a valid authentication token in cookies. Asserts that the
        response status code is 200, indicating a successful logout.
        """
        client.cookies.set('auth_token', self.cookie)
        response = client.post('/api/v1/logout')
        assert response.status_code == 200

    def test_logout_user_incorrect(self, client: TestClient) -> None:
        """
        Test case for handling an invalid logout request.

        Sends a POST request to the /api/v1/logout endpoint with
        a revoked or invalid authentication token in cookies. Asserts
        that the response status code is 204, indicating that the logout
        operation did not require any further action.
        """
        client.cookies.set('auth_token', 'revoked')
        response = client.post('/api/v1/logout')
        assert response.status_code == 204
