#!/usr/bin/python
# Copyright (c) Facebook, Inc. and its affiliates.
"""Add Adobe products to user on-demand."""

import sys

import adobe_api
import adobe_tools

target_product = sys.argv[1]

me = ldap_lookup()  # Replace this with your own user lookup method
email = me.email
firstname = me.first_name
lastname = me.last_name
country = 'US'


def log(message):
try:
    # Do I exist as a user?
    if not adobe_tools.user_exists(email):
        log(f"Creating account for {email}")
        # Add the user
        success = adobe_tools.add_federated_user(
            email,
            email,
            firstname,
            lastname,
            country
        )
        if not success:
            log(f"Failed to create account for {email}")
            sys.exit(1)

    # Does the user already have the product?
    log(f"Checking to see if {email} already has {target_product}")
    if already_have := adobe_tools.does_user_have_product(
        email, target_product
    ):
        log(f"User {email} already has product {target_product}")
        sys.exit(0)

    # Add desired product
    log(f"Adding {target_product} entitlement to {email}")
    result = adobe_tools.add_products([target_product], email)
    if not result:
        log(f"Failed to add product {target_product} to {email}")
        sys.exit(1)

    log("Done.")
except adobe_api.AdobeAPIBadStatusException as e:
    log(f"Encountered exception: {e}")
    log(
        "You were most likely rate limited - "
        "this will automatically try again later. "
        "Alternatively, please contact Help Desk."
    )
    exit(1)
